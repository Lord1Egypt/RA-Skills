#!/usr/bin/env python3
"""
Cloud-Local Bridge 一键安装脚本
自动安装依赖、生成配置、启动服务
"""

import os
import sys
import json
import subprocess
import argparse
import signal
from pathlib import Path

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log(msg, color=Colors.GREEN):
    print(f"{color}{msg}{Colors.ENDC}")

def log_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def log_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def log_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

def check_dependencies():
    """检查并安装依赖"""
    log("检查依赖...", Colors.BLUE)
    
    deps = ['requests', 'psutil']
    for dep in deps:
        try:
            __import__(dep)
            log_success(f"{dep} 已安装")
        except ImportError:
            log_info(f"正在安装 {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
            log_success(f"{dep} 安装完成")

def generate_token():
    """生成安全 token"""
    import hashlib
    import time
    random_str = os.urandom(32)
    return hashlib.sha256(f"{random_str}{time.time()}".encode()).hexdigest()

def create_config(port, token, config_path):
    """创建配置文件"""
    config = {
        "version": "1.0",
        "local": {
            "server": f"http://localhost:{port}",
            "token": token,
            "port": port
        },
        "bridge": {
            "default_timeout": 60,
            "max_file_size": 100  # MB
        }
    }
    
    config_path = Path(config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    log_success(f"配置文件已创建: {config_path}")
    return config_path

def start_server(port, token, script_dir):
    """启动 Bridge 服务"""
    import subprocess
    import time
    import requests
    
    server_script = os.path.join(script_dir, 'bridge_server.py')
    
    log(f"启动 Bridge 服务 (端口: {port})...", Colors.BLUE)
    
    # 启动进程
    process = subprocess.Popen(
        [sys.executable, server_script, '--port', str(port), '--token', token],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        buffufering=1
    )
    
    # 等待服务启动
    max_wait = 10
    for i in range(max_wait):
        try:
            resp = requests.get(f"http://localhost:{port}/health", timeout=1)
            if resp.status_code == 200:
                log_success("Bridge 服务启动成功!")
                return process
        except:
            pass
        time.sleep(1)
    
    log_error("服务启动超时")
    return process

def show_instructions(config_path, port, token):
    """显示使用说明"""
    print()
    log(f"{Colors.HEADER}🎉 安装完成!{Colors.ENDC}", Colors.BOLD)
    print()
    print(f"{Colors.BOLD}📁 配置文件:{Colors.ENDC} {config_path}")
    print()
    print(f"{Colors.BOLD}📌 快速测试:{Colors.ENDC}")
    print(f"   python3 {os.path.dirname(config_path)}/../scripts/bridge_client.py --server http://localhost:{port} --token {token[:8]}... status")
    print()
    print(f"{Colors.BOLD}🔗 云端连接信息:{Colors.ENDC}")
    print(f"   服务器: http://YOUR_LOCAL_IP:{port}")
    print(f"   Token:  {token}")
    print()
    print(f"{Colors.BOLD}📖 完整文档:{Colors.ENDC} 查看 SKILL.md")
    print()

def interactive_install():
    """交互式安装"""
    print()
    log(f"{Colors.HEADER}🚀 Cloud-Local Bridge 安装程序{Colors.ENDC}", Colors.BOLD)
    print()
    
    # 获取安装目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(script_dir)  # 返回到 skills/cloud-local-bridge
    
    # 默认端口
    default_port = 8080
    
    print(f"安装目录: {script_dir}")
    print()
    
    # 1. 检查依赖
    check_dependencies()
    print()
    
    # 2. 获取端口
    port_input = input(f"请输入监听端口 (默认 {default_port}): ").strip()
    port = int(port_input) if port_input else default_port
    print()
    
    # 3. 生成 Token
    token = generate_token()
    log_success(f"Token 已生成: {token[:16]}...")
    print()
    
    # 4. 创建配置
    config_path = os.path.expanduser("~/.openclaw/bridge.json")
    create_config(port, token, config_path)
    print()
    
    # 5. 启动服务
    process = start_server(port, token, script_dir)
    
    # 6. 显示说明
    show_instructions(config_path, port, token)
    
    return process

def main():
    parser = argparse.ArgumentParser(description='Cloud-Local Bridge 安装程序')
    parser.add_argument('--port', type=int, default=8080, help='监听端口')
    parser.add_argument('--token', help='指定 token (可选，默认自动生成)')
    parser.add_argument('--config', default='~/.openclaw/bridge.json', help='配置文件路径')
    parser.add_argument('--daemon', action='store_true', help='后台运行')
    
    args = parser.parse_args()
    
    if not args.token:
        args.token = generate_token()
        log_info(f"自动生成 Token: {args.token[:16]}...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.dirname(script_dir)
    
    check_dependencies()
    config_path = create_config(args.port, args.token, args.config)
    
    if not args.daemon:
        process = start_server(args.port, args.token, script_dir)
        show_instructions(config_path, args.port, args.token)
        
        # 等待中断
        try:
            process.wait()
        except KeyboardInterrupt:
            log("\n🛑 正在停止服务...")
            process.terminate()
            process.wait()
            log_success("服务已停止")
    else:
        import time
        process = start_server(args.port, args.token, script_dir)
        time.sleep(2)
        show_instructions(config_path, args.port, args.token)
        log_info(f"服务已在后台运行 (PID: {process.pid})")

if __name__ == '__main__':
    interactive_install()
