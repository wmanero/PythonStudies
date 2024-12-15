# Programa: Calculadora de máscara de redes
# Autor: Welton Silva
# Data Criação: 15/12/2024
# Versão: 1.0
# Nota: Criado com Framework Flask, Python e HTML

from flask import Flask, render_template, request  # Importa as bibliotecas Flask e request
import ipaddress  # Importa a biblioteca ipaddress para manipulação de endereços IP
import webbrowser
import threading

app = Flask(__name__)  # Cria uma instância do aplicativo Flask

def calculate_subnet_info(ip, prefix):
    """
    Calcula a máscara de rede, o endereço da rede e a quantidade de hosts utilizáveis
    a partir de um endereço IP e prefixo CIDR.
    """
    network = ipaddress.ip_network(f'{ip}/{prefix}', strict=False)
    subnet_mask = network.netmask
    network_address = network.network_address
    total_hosts = network.num_addresses
    broadcast_address = network.broadcast_address
    usable_hosts = total_hosts - 2 if total_hosts > 2 else 0  # Subtrai 2 para o endereço de rede e broadcast
    return subnet_mask, network_address, broadcast_address, usable_hosts

@app.route('/')
def home():
    """
    Rota principal que renderiza o template index.html com o formulário.
    """
    return render_template('index.html')

def open_browser():
    """
    Abre o navegador no endereço e porta especificados.
    """
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Rota para calcular a máscara de rede, o endereço da rede e a quantidade de hosts utilizáveis.
    Recebe os dados do formulário, calcula as informações e renderiza o template result.html com os resultados.
    """
    ip = request.form['ip']  # Recebe o endereço IP do formulário
    prefix = request.form['prefix']  # Recebe o prefixo CIDR do formulário
    subnet_mask, network_address, broadcast_address,  usable_hosts = calculate_subnet_info(ip, prefix)
    return render_template('result.html', ip=ip, prefix=prefix, subnet_mask=subnet_mask, network_address=network_address, broadcast_address=broadcast_address, usable_hosts=usable_hosts)

if __name__ == '__main__':
    # Abre o navegador após um pequeno atraso para garantir que o servidor Flask esteja ativo.
    threading.Timer(1.25, open_browser).start()
    app.run(debug=False)

'''
if __name__ == '__main__':
    #Criar um thread que abrirá o navegador após um pequeno atraso para garantir que o servidor Flask esteja ativo.
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)  # Inicia o servidor Flask no modo de depuração
'''