#!/usr/bin/env python3
"""
Agent P2P Portal 自动化部署脚本

职责：
1. SSH 连接到用户 VPS
2. 安装所有依赖
3. 部署 Portal 代码
4. 配置 Nginx + SSL
5. 启动服务
6. 生成默认 API Key

避坑清单（来自实际部署经验）：
- Ubuntu 22.04 默认 Python 3.10，需要安装 python3-venv
- Nginx 配置要注意 WebSocket 支持（Upgrade 头）
- Certbot 需要先停止 Nginx 才能申请证书（端口冲突）
- 防火墙需要开放 80/443/22
- 服务要用 systemd 管理，确保开机自启
- SQLite 数据库目录需要正确权限
"""

import os
import sys
import json
import time
import argparse
import secrets
from pathlib import Path
from typing import Optional, Tuple

# 尝试导入 paramiko
try:
    import paramiko
except ImportError:
    print("❌ 缺少 paramiko 依赖")
    print("请运行: pip install paramiko")
    sys.exit(1)


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def log_info(msg: str):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")


def log_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")


def log_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")


def log_warn(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")


class PortalDeployer:
    """Portal 部署器"""
    
    def __init__(self, host: str, ssh_key_path: str, domain: str, email: str):
        self.host = host
        self.ssh_key_path = Path(ssh_key_path).expanduser()
        self.domain = domain
        self.email = email
        
        self.ssh: Optional[paramiko.SSHClient] = None
        self.sftp: Optional[paramiko.SFTPClient] = None
        
        # 部署路径
        self.remote_path = "/opt/agent-p2p"
        self.venv_path = f"{self.remote_path}/venv"
        
        # 本地 skill 路径
        self.local_skill_path = Path(__file__).parent.parent.absolute()
        
        # 生成的 API Key
        self.api_key: Optional[str] = None
        
    def connect(self) -> bool:
        """建立 SSH 连接"""
        log_info(f"连接到 {self.host}...")
        
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 加载私钥
            private_key = paramiko.RSAKey.from_private_key_file(str(self.ssh_key_path))
            
            # 尝试 ubuntu 用户，失败则尝试 root
            for username in ["ubuntu", "root"]:
                try:
                    self.ssh.connect(
                        hostname=self.host,
                        username=username,
                        pkey=private_key,
                        timeout=10
                    )
                    self.username = username
                    log_info(f"使用用户 {username} 连接成功")
                    break
                except paramiko.AuthenticationException:
                    if username == "root":
                        raise
                    continue
            
            self.sftp = self.ssh.open_sftp()
            log_success("SSH 连接成功")
            return True
            
        except Exception as e:
            log_error(f"SSH 连接失败: {e}")
            return False
    
    def run_command(self, command: str, timeout: int = 60, sudo: bool = False) -> Tuple[int, str, str]:
        """在远程执行命令"""
        if sudo and self.username != "root":
            command = f"sudo -n {command}"
        stdin, stdout, stderr = self.ssh.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        return exit_code, out, err
    
    def check_system(self) -> bool:
        """检查系统环境"""
        log_info("检查系统环境...")
        
        # 检查 Ubuntu 版本
        exit_code, out, _ = self.run_command("lsb_release -rs")
        if exit_code != 0 or "22.04" not in out:
            log_warn(f"检测到非 Ubuntu 22.04 系统: {out.strip()}")
            log_warn("脚本可能无法正常工作，建议升级")
        else:
            log_success("Ubuntu 22.04 检测通过")
        
        # 检查内存
        exit_code, out, _ = self.run_command("free -h | grep Mem | awk '{print $2}'")
        if exit_code == 0:
            log_info(f"内存: {out.strip()}")
        
        # 检查磁盘
        exit_code, out, _ = self.run_command("df -h / | tail -1 | awk '{print $4}'")
        if exit_code == 0:
            log_info(f"可用磁盘: {out.strip()}")
        
        return True
    
    def install_dependencies(self) -> bool:
        """安装系统依赖"""
        log_info("安装系统依赖（可能需要几分钟）...")
        
        commands = [
            # 更新包列表
            "apt-get update -qq",
            
            # 安装基础工具
            "apt-get install -y -qq software-properties-common curl wget git",
            
            # 安装 Python 3.10 + venv
            "apt-get install -y -qq python3.10 python3.10-venv python3-pip",
            
            # 安装 Nginx
            "apt-get install -y -qq nginx",
            
            # 安装 Certbot
            "apt-get install -y -qq certbot python3-certbot-nginx",
            
            # 安装防火墙工具
            "apt-get install -y -qq ufw",
        ]
        
        for cmd in commands:
            log_info(f"执行: {cmd[:50]}...")
            exit_code, out, err = self.run_command(cmd, timeout=300, sudo=True)
            if exit_code != 0:
                log_error(f"命令失败: {cmd}")
                log_error(f"错误: {err}")
                return False
        
        log_success("系统依赖安装完成")
        return True
    
    def configure_firewall(self) -> bool:
        """配置防火墙"""
        log_info("配置防火墙...")
        
        commands = [
            "ufw default deny incoming",
            "ufw default allow outgoing",
            "ufw allow 22/tcp",    # SSH
            "ufw allow 80/tcp",    # HTTP
            "ufw allow 443/tcp",   # HTTPS
            "ufw --force enable",
        ]
        
        for cmd in commands:
            exit_code, _, _ = self.run_command(cmd, sudo=True)
        
        log_success("防火墙配置完成")
        return True
    
    def upload_code(self) -> bool:
        """从 GitHub 拉取最新代码"""
        log_info("从 GitHub 拉取最新代码...")
        
        # 创建远程目录（使用 sudo）
        self.run_command(f"mkdir -p {self.remote_path}", sudo=True)
        self.run_command(f"chown -R $(whoami):$(whoami) {self.remote_path}", sudo=True)
        
        # 从 GitHub 克隆最新代码
        github_url = "https://github.com/yananli199307-dev/AgentPortal-p2p-skill.git"
        
        # 如果目录已存在，先删除
        self.run_command(f"rm -rf {self.remote_path}")
        
        # 克隆代码
        exit_code, _, err = self.run_command(
            f"cd /opt && git clone --depth 1 {github_url} agent-p2p",
            timeout=60
        )
        if exit_code != 0:
            log_error(f"克隆代码失败: {err}")
            return False
        
        log_success("最新代码拉取完成")
        return True
    
    def install_python_deps(self) -> bool:
        """安装 Python 依赖"""
        log_info("安装 Python 依赖...")
        
        # 创建虚拟环境
        exit_code, _, err = self.run_command(
            f"cd {self.remote_path} && python3 -m venv venv"
        )
        if exit_code != 0:
            log_error(f"创建虚拟环境失败: {err}")
            return False
        
        # 安装依赖
        exit_code, _, err = self.run_command(
            f"cd {self.remote_path} && venv/bin/pip install -q fastapi uvicorn python-jose[cryptography] python-multipart websockets pytz",
            timeout=180
        )
        if exit_code != 0:
            log_error(f"安装依赖失败: {err}")
            return False
        
        log_success("Python 依赖安装完成")
        return True
    
    def configure_nginx(self) -> bool:
        """配置 Nginx"""
        log_info("配置 Nginx...")
        
        # 创建管理后台密码文件
        log_info("创建管理后台密码保护...")
        self.run_command("apt-get install -y apache2-utils", sudo=True)
        self.run_command("htpasswd -cb /etc/nginx/.htpasswd admin AgentP2P2024", sudo=True)
        
        config = f'''server {{
    listen 80;
    server_name {self.domain};
    
    # 管理后台 - 需要密码验证
    location = /static/admin.html {{
        auth_basic "Agent P2P Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    # 管理后台静态资源 - 也需要密码
    location /static/ {{
        auth_basic "Agent P2P Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    # API 和 WebSocket - 公开访问
    location / {{
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}'''
        # 写入配置
        config_path = f"/etc/nginx/sites-available/agent-p2p"
        # 先写入临时文件，再 sudo mv
        temp_config = "/tmp/agent-p2p-nginx.conf"
        with open(temp_config, 'w') as f:
            f.write(config)
        self.sftp.put(temp_config, temp_config)
        self.run_command(f"mv {temp_config} {config_path}", sudo=True)
        
        # 启用站点
        self.run_command(
            f"ln -sf {config_path} /etc/nginx/sites-enabled/agent-p2p", sudo=True
        )
        self.run_command("rm -f /etc/nginx/sites-enabled/default", sudo=True)
        
        # 测试配置
        exit_code, _, err = self.run_command("nginx -t", sudo=True)
        if exit_code != 0:
            log_error(f"Nginx 配置测试失败: {err}")
            return False
        
        # 重启 Nginx
        self.run_command("systemctl restart nginx", sudo=True)
        
        log_success("Nginx 配置完成（管理后台已加密）")
        return True
    
    def setup_ssl(self) -> bool:
        """配置 SSL 证书"""
        log_info("申请 SSL 证书（需要域名已解析到本机）...")
        
        # 检查域名解析
        log_info(f"检查域名 {self.domain} 解析...")
        exit_code, out, _ = self.run_command(f"dig +short {self.domain}")
        if self.host not in out:
            log_warn(f"域名 {self.domain} 可能未解析到 {self.host}")
            log_warn("请确认 DNS A 记录已设置，按回车继续或 Ctrl+C 取消")
            input()
        
        # 申请证书
        exit_code, out, err = self.run_command(
            f"certbot --nginx -d {self.domain} --non-interactive --agree-tos -m {self.email}",
            timeout=120, sudo=True
        )
        
        if exit_code != 0:
            log_error(f"SSL 证书申请失败: {err}")
            log_error("可能原因：域名未解析、80端口被占用、邮箱无效")
            return False
        
        # 设置自动续期
        self.run_command("systemctl enable certbot.timer", sudo=True)
        
        log_success("SSL 证书配置完成")
        return True
    
    def generate_api_key(self) -> bool:
        """生成默认 API Key"""
        log_info("生成默认 API Key...")
        
        # 生成 API Key
        self.api_key = "ap2p_" + secrets.token_urlsafe(32)
        portal_url = f"https://{self.domain}"
        
        # 创建数据目录
        self.run_command(f"mkdir -p {self.remote_path}/data", sudo=True)
        
        # 使用 Python 在远程服务器上初始化数据库并插入 API Key
        init_script = f'''
import sqlite3
import os

db_path = "{self.remote_path}/data/portal.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建 api_keys 表
cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        key_id TEXT PRIMARY KEY,
        portal_url TEXT NOT NULL,
        agent_name TEXT,
        user_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    )
""")

# 插入默认 API Key
cursor.execute("""
    INSERT OR IGNORE INTO api_keys (key_id, portal_url, agent_name, user_name, created_at, is_active)
    VALUES (?, ?, ?, ?, datetime('now'), TRUE)
""", ("{self.api_key}", "{portal_url}", "default_agent", "admin"))

conn.commit()
conn.close()
print("API Key created successfully")
'''
        
        # 写入并执行初始化脚本
        init_script_path = f"{self.remote_path}/init_api_key.py"
        with open("/tmp/init_api_key.py", 'w') as f:
            f.write(init_script)
        self.sftp.put("/tmp/init_api_key.py", init_script_path)
        
        exit_code, out, err = self.run_command(
            f"cd {self.remote_path} && python3 init_api_key.py"
        )
        
        if exit_code != 0:
            log_error(f"生成 API Key 失败: {err}")
            return False
        
        log_success("默认 API Key 已生成")
        return True
    
    def create_systemd_service(self) -> bool:
        """创建 systemd 服务"""
        log_info("创建 systemd 服务...")
        
        service_content = f'''[Unit]
Description=Agent P2P Portal
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory={self.remote_path}
Environment=PATH={self.venv_path}/bin
Environment=PORTAL_URL=https://{self.domain}
ExecStart={self.venv_path}/bin/uvicorn src.main:app --host 127.0.0.1 --port 8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
'''
        
        service_path = "/etc/systemd/system/agent-p2p.service"
        self.run_command(f"cat > {service_path} << 'EOF'\n{service_content}\nEOF", sudo=True)
        
        # 重载 systemd
        self.run_command("systemctl daemon-reload", sudo=True)
        
        # 启动服务
        self.run_command("systemctl enable agent-p2p", sudo=True)
        self.run_command("systemctl start agent-p2p", sudo=True)
        
        # 检查状态
        time.sleep(2)
        exit_code, out, _ = self.run_command("systemctl is-active agent-p2p")
        if "active" not in out:
            log_error("服务启动失败")
            self.run_command("journalctl -u agent-p2p -n 20 --no-pager")
            return False
        
        log_success("systemd 服务创建完成")
        return True
    
    def verify_deployment(self) -> bool:
        """验证部署"""
        log_info("验证部署...")
        
        # 检查服务状态
        exit_code, out, _ = self.run_command("systemctl is-active agent-p2p")
        if "active" in out:
            log_success("Agent P2P 服务运行中")
        else:
            log_error("Agent P2P 服务未运行")
            return False
        
        # 检查 Nginx
        exit_code, out, _ = self.run_command("systemctl is-active nginx")
        if "active" in out:
            log_success("Nginx 运行中")
        else:
            log_error("Nginx 未运行")
            return False
        
        # 检查端口
        exit_code, out, _ = self.run_command("ss -tlnp | grep :443")
        if ":443" in out:
            log_success("HTTPS 端口正常")
        else:
            log_warn("HTTPS 端口未监听")
        
        # 测试 HTTP 访问
        exit_code, out, _ = self.run_command(
            f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8080/ || echo '000'"
        )
        if out.strip() == "200":
            log_success("本地服务响应正常")
        else:
            log_warn("本地服务可能未就绪")
        
        return True
    
    def deploy(self) -> bool:
        """执行完整部署"""
        print(f"\n{'='*50}")
        print(f"Agent P2P Portal 部署")
        print(f"服务器: {self.host}")
        print(f"域名: {self.domain}")
        print(f"{'='*50}\n")
        
        steps = [
            ("连接服务器", self.connect),
            ("检查系统", self.check_system),
            ("安装依赖", self.install_dependencies),
            ("配置防火墙", self.configure_firewall),
            ("上传代码", self.upload_code),
            ("安装 Python 包", self.install_python_deps),
            ("配置 Nginx", self.configure_nginx),
            ("配置 SSL", self.setup_ssl),
            ("生成 API Key", self.generate_api_key),
            ("创建服务", self.create_systemd_service),
            ("验证部署", self.verify_deployment),
        ]
        
        for name, step_func in steps:
            print(f"\n{'─'*50}")
            print(f"步骤: {name}")
            print(f"{'─'*50}")
            
            if not step_func():
                log_error(f"部署失败于步骤: {name}")
                return False
        
        print(f"\n{'='*50}")
        log_success("部署完成！")
        print(f"{'='*50}")
        print(f"\n访问地址:")
        print(f"  Portal: https://{self.domain}")
        print(f"  管理后台: https://{self.domain}/static/admin.html")
        print(f"\nAPI Key:")
        print(f"  {self.api_key}")
        print(f"\n⚠️  请妥善保存此 API Key，它不会再次显示！")
        print(f"\n管理命令:")
        print(f"  查看状态: systemctl status agent-p2p")
        print(f"  查看日志: journalctl -u agent-p2p -f")
        print(f"  重启服务: systemctl restart agent-p2p")
        print(f"\n")
        
        return True
    
    def close(self):
        """关闭连接"""
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()


def main():
    parser = argparse.ArgumentParser(description="部署 Agent P2P Portal")
    parser.add_argument("--host", required=True, help="VPS IP 地址")
    parser.add_argument("--ssh-key", required=True, help="SSH 私钥路径")
    parser.add_argument("--domain", required=True, help="域名")
    parser.add_argument("--email", required=True, help="SSL 证书邮箱")
    
    args = parser.parse_args()
    
    deployer = PortalDeployer(
        host=args.host,
        ssh_key_path=args.ssh_key,
        domain=args.domain,
        email=args.email
    )
    
    try:
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    finally:
        deployer.close()


if __name__ == "__main__":
    main()
