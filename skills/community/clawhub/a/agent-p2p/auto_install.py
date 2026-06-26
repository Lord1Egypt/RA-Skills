#!/usr/bin/env python3
"""
Agent P2P 自动安装脚本

一键完成：
1. 检查前置条件（DNS、防火墙、SSH）
2. 部署 Portal 到 VPS
3. 获取 API Key
4. 配置并启动 Bridge
5. 测试连接

用法：
python3 auto_install.py \
  --domain agent.example.com \
  --vps-ip 43.x.x.x \
  --ssh-key ~/.ssh/agent-p2p \
  --email user@example.com \
  --gateway-url http://127.0.0.1:18789 \
  --hooks-token xxx
"""

import os
import sys
import time
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def get_hooks_token():
    """自动获取 OpenClaw hooks token"""
    # 1. 先从 openclaw.json 读取
    openclaw_config = Path.home() / ".openclaw" / "openclaw.json"
    if openclaw_config.exists():
        try:
            config = json.loads(openclaw_config.read_text())
            token = config.get("hooks", {}).get("token")
            if token:
                return token
        except Exception as e:
            print(f"  ⚠️ 读取 openclaw.json 失败: {e}")
    
    # 2. 再从 gateway.env 读取
    gateway_env = Path.home() / ".openclaw" / "gateway.env"
    if gateway_env.exists():
        try:
            env_content = gateway_env.read_text()
            for line in env_content.splitlines():
                if line.startswith("OPENCLAW_HOOKS_TOKEN="):
                    return line.split("=", 1)[1].strip()
        except Exception as e:
            print(f"  ⚠️ 读取 gateway.env 失败: {e}")
    
    return None


def run(cmd, check=True):
    """运行命令"""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"错误: {result.stderr}")
        sys.exit(1)
    return result


def check_dns(domain, vps_ip):
    """检查域名解析"""
    print(f"\n[1/6] 检查域名解析: {domain}")
    
    for i in range(30):  # 最多等待 5 分钟
        result = subprocess.run(
            f"nslookup {domain}",
            shell=True, capture_output=True, text=True
        )
        
        # 检查是否包含期望的 IP
        if vps_ip in result.stdout:
            print(f"  ✅ 域名解析正确: {domain} -> {vps_ip}")
            return True
        
        print(f"  ⏳ 等待 DNS 生效... ({i+1}/30)")
        time.sleep(10)
    
    print(f"  ❌ DNS 未生效，请检查域名解析设置")
    print(f"  期望: {domain} -> {vps_ip}")
    print(f"  实际: {result.stdout}")
    sys.exit(1)


def check_ssh(vps_ip, ssh_key):
    """检查 SSH 连接"""
    print(f"\n[2/6] 检查 SSH 连接: {vps_ip}")
    
    # 检查密钥权限
    key_path = Path(ssh_key)
    if key_path.stat().st_mode & 0o077:
        print(f"  修复密钥权限: {ssh_key}")
        os.chmod(ssh_key, 0o600)
    
    # 测试连接
    result = subprocess.run(
        f"ssh -i {ssh_key} -o StrictHostKeyChecking=no -o BatchMode=yes ubuntu@{vps_ip} 'echo OK'",
        shell=True, capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"  ✅ SSH 连接成功")
        return True
    
    print(f"  ❌ SSH 连接失败")
    print(f"  请确保已复制公钥到 VPS:")
    print(f"  ssh-copy-id -i {ssh_key}.pub ubuntu@{vps_ip}")
    sys.exit(1)


def deploy_portal(vps_ip, ssh_key, domain, email):
    """部署 Portal"""
    print(f"\n[3/6] 部署 Portal 到 VPS")
    
    script = f"""
set -e
cd /opt
sudo rm -rf agent-p2p
sudo git clone https://github.com/yananli199307-dev/AgentPortal-p2p-skill.git agent-p2p
sudo chown -R ubuntu:ubuntu agent-p2p
cd agent-p2p

# 安装依赖
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# 安装 Python 依赖
pip3 install -r requirements.txt

# 配置环境变量
export PORTAL_URL="https://{domain}"
export DATABASE_PATH="./data/portal.db"

# 创建数据目录
mkdir -p data

# 初始化数据库（如果不存在）
if [ ! -f "data/portal.db" ]; then
    echo "初始化数据库..."
    python3 -c "from vps.main import init_db; init_db()"
else
    echo "数据库已存在，跳过初始化"
fi

# 生成随机密码
ADMIN_USER="admin"
ADMIN_PASS=$(openssl rand -base64 12)
echo "ADMIN_USER=$ADMIN_USER" | sudo tee /opt/agent-p2p/.env
echo "ADMIN_PASS=$ADMIN_PASS" | sudo tee -a /opt/agent-p2p/.env
sudo chmod 600 /opt/agent-p2p/.env

# 创建 Nginx 密码文件
sudo apt-get install -y apache2-utils
sudo htpasswd -cb /etc/nginx/.htpasswd "$ADMIN_USER" "$ADMIN_PASS"

# 配置 Nginx
sudo tee /etc/nginx/sites-available/agent-p2p > /dev/null << 'EOF'
server {{
    listen 80;
    server_name {domain};
    
    # API - 公开访问
    location /api/ {{
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
    
    # WebSocket
    location /ws/ {{
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
    }}
    
    # 管理后台 - 需要密码
    location /static/admin.html {{
        auth_basic "Agent P2P Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $proxy_add_x_forwarded_for;
    }}
    
    # 静态资源 - 公开访问
    location / {{
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}
}}
EOF

sudo ln -sf /etc/nginx/sites-available/agent-p2p /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 申请 SSL
certbot --nginx -d {domain} --non-interactive --agree-tos --email {email}

# 确保 Nginx 正确重启以应用 SSL 配置
sudo systemctl restart nginx

# 创建 systemd 服务
sudo tee /etc/systemd/system/agent-p2p.service > /dev/null << 'EOF'
[Unit]
Description=Agent P2P Portal
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/agent-p2p
Environment=PORTAL_URL=https://{domain}
Environment=DATABASE_PATH=/opt/agent-p2p/data/portal.db
ExecStart=/usr/bin/python3 -m uvicorn vps.main:app --host 127.0.0.1 --port 8080
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable agent-p2p
sudo systemctl start agent-p2p

# 输出管理员密码（用于本地保存）
echo "ADMIN_CREDENTIALS: $ADMIN_USER:$ADMIN_PASS"

echo "部署完成"
"""
    
    result = subprocess.run(
        f"ssh -i {ssh_key} ubuntu@{vps_ip} '{script}'",
        shell=True, capture_output=True, text=True
    )
    
    if result.returncode == 0:
        print(f"  ✅ Portal 部署成功")
        # 提取管理员密码
        for line in result.stdout.split('\n'):
            if line.startswith('ADMIN_CREDENTIALS:'):
                admin_creds = line.replace('ADMIN_CREDENTIALS:', '').strip()
                print(f"  🔐 管理后台密码已生成")
                # 保存到类变量供后续使用
                deploy_portal.admin_creds = admin_creds
                break
        return True
    
    print(f"  ❌ 部署失败")
    print(result.stderr)
    sys.exit(1)


def get_api_key(vps_ip, ssh_key):
    """获取 API Key"""
    print(f"\n[4/6] 获取 API Key")
    
    result = subprocess.run(
        f"ssh -i {ssh_key} ubuntu@{vps_ip} 'python3 -c \"import sqlite3; conn = sqlite3.connect(\\\"/opt/agent-p2p/data/portal.db\\\"); cur = conn.cursor(); cur.execute(\\\"SELECT key_id FROM api_keys LIMIT 1\\\"); print(cur.fetchone()[0])\"'",
        shell=True, capture_output=True, text=True
    )
    
    api_key = result.stdout.strip()
    if api_key:
        print(f"  ✅ 获取 API Key: {api_key[:20]}...")
        return api_key
    
    print(f"  ❌ 未找到 API Key")
    sys.exit(1)


def setup_bridge(domain, api_key, gateway_url, hooks_token):
    """配置并启动 Bridge"""
    print(f"\n[5/6] 配置 Bridge")
    
    # 写入环境变量
    env_file = Path.home() / ".openclaw" / "gateway.env"
    env_file.parent.mkdir(parents=True, exist_ok=True)
    
    env_content = f"""# Agent P2P 配置
AGENTP2P_API_KEY={api_key}
AGENTP2P_HUB_URL=https://{domain}
OPENCLAW_GATEWAY_URL={gateway_url}
OPENCLAW_HOOKS_TOKEN={hooks_token}
"""
    
    env_file.write_text(env_content)
    print(f"  ✅ 写入配置: {env_file}")
    
    # 启动 Bridge
    skill_dir = Path.home() / ".openclaw" / "workspace" / "skills" / "agent-p2p"
    if skill_dir.exists():
        subprocess.run(
            f"cd {skill_dir} && python3 local/start.py restart",
            shell=True
        )
        print(f"  ✅ Bridge 启动成功")
    else:
        print(f"  ⚠️ Skill 未安装，跳过启动 Bridge")


def test_connection(domain, api_key, gateway_url, hooks_token):
    """测试连接"""
    print(f"\n[6/6] 测试连接")
    
    # 测试 Portal
    result = subprocess.run(
        f"curl -sk https://{domain}/api/portal/info",
        shell=True, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✅ Portal 可访问")
    else:
        print(f"  ❌ Portal 访问失败")
        return False
    
    # 测试 OpenClaw
    result = subprocess.run(
        f"curl -s -X POST {gateway_url}/hooks/wake -H 'Authorization: Bearer {hooks_token}' -H 'Content-Type: application/json' -d '{{\"text\":\"测试\"}}'",
        shell=True, capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✅ OpenClaw 可唤醒")
    else:
        print(f"  ❌ OpenClaw 唤醒失败")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Agent P2P 自动安装')
    parser.add_argument('--domain', required=True, help='域名')
    parser.add_argument('--vps-ip', required=True, help='VPS IP')
    parser.add_argument('--ssh-key', required=True, help='SSH 私钥路径')
    parser.add_argument('--email', required=True, help='邮箱')
    parser.add_argument('--gateway-url', default='http://127.0.0.1:18789', help='Gateway URL')
    parser.add_argument('--hooks-token', default=None, help='Hooks Token（可选，不填则自动读取）')
    
    args = parser.parse_args()
    
    # 自动获取 hooks token
    hooks_token = args.hooks_token
    if not hooks_token:
        print("\n🔍 正在自动获取 hooks token...")
        hooks_token = get_hooks_token()
        if hooks_token:
            print(f"  ✅ 从配置文件读取: {hooks_token[:20]}...")
        else:
            print("  ❌ 无法自动获取 hooks token，请通过 --hooks-token 参数传入")
            print("  获取方式：cat ~/.openclaw/openclaw.json | grep token")
            sys.exit(1)
    
    print("=" * 60)
    print("Agent P2P 自动安装")
    print("=" * 60)
    
    # 执行安装步骤
    check_dns(args.domain, args.vps_ip)
    check_ssh(args.vps_ip, args.ssh_key)
    deploy_portal(args.vps_ip, args.ssh_key, args.domain, args.email)
    api_key = get_api_key(args.vps_ip, args.ssh_key)
    setup_bridge(args.domain, api_key, args.gateway_url, args.hooks_token)
    
    if test_connection(args.domain, api_key, args.gateway_url, args.hooks_token):
        print("\n" + "=" * 60)
        print("✅ 安装完成！")
        print("=" * 60)
        print(f"\nPortal: https://{args.domain}")
        print(f"管理后台: https://{args.domain}/static/admin.html")
        print(f"API Key: {api_key[:20]}...")
        
        # 获取并显示管理员密码
        admin_creds = getattr(deploy_portal, 'admin_creds', 'admin:unknown')
        admin_user, admin_pass = admin_creds.split(':') if ':' in admin_creds else ('admin', 'unknown')
        
        print("\n🔐 管理后台登录信息：")
        print(f"  用户名: {admin_user}")
        print(f"  初始密码: {admin_pass}")
        
        # 询问是否修改密码
        change_pass = input("\n是否修改管理后台密码? [y/N]: ").strip().lower()
        if change_pass in ('y', 'yes'):
            new_pass = input("请输入新密码: ").strip()
            if new_pass:
                # 更新 VPS 上的密码
                update_cmd = f"ssh -i {args.ssh_key} ubuntu@{args.vps_ip} 'sudo htpasswd -cb /etc/nginx/.htpasswd {admin_user} \"{new_pass}\" && echo 密码已更新'"
                result = subprocess.run(update_cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    admin_pass = new_pass
                    print("✅ 密码已更新")
                else:
                    print(f"⚠️ 密码更新失败: {result.stderr}")
        
        print(f"  当前密码: {admin_pass}")
        print(f"  请妥善保管")
        
        # 保存密码到本地文件
        admin_file = Path.home() / ".openclaw" / "agent-p2p-admin.txt"
        admin_file.parent.mkdir(parents=True, exist_ok=True)
        admin_file.write_text(f"Portal: https://{args.domain}\n用户名: {admin_user}\n密码: {admin_pass}\n")
        
        # 保存部署信息（VPS IP、SSH 密钥等）
        deploy_info_file = Path.home() / ".openclaw" / "agent-p2p-deploy.txt"
        deploy_info_file.write_text(f"""# Agent P2P 部署信息
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

VPS_IP={args.vps_ip}
SSH_KEY={args.ssh_key}
DOMAIN={args.domain}
EMAIL={args.email}
API_KEY={api_key}

# 使用方式:
# SSH 到 VPS: ssh -i {args.ssh_key} ubuntu@{args.vps_ip}
# 查看状态: ssh -i {args.ssh_key} ubuntu@{args.vps_ip} "sudo systemctl status agent-p2p"
""")
        print(f"  📄 部署信息已保存: {deploy_info_file}")
        
        # 最后一步：配置 OpenClaw Hooks
        print("\n" + "=" * 60)
        print("🔧 最后一步：配置 OpenClaw Hooks")
        print("=" * 60)
        
        setup_script = Path(__file__).parent / "scripts" / "setup_openclaw_hooks.py"
        if setup_script.exists():
            run_setup = input("\n是否配置 OpenClaw Hooks（推荐）? [Y/n]: ").strip().lower()
            if not run_setup or run_setup in ('y', 'yes'):
                subprocess.run([sys.executable, str(setup_script)])
        else:
            print("⚠️ 未找到配置脚本，请手动配置:")
            print("  python3 scripts/setup_openclaw_hooks.py")
        
        print(f"\n✅ 所有组件已连接并测试通过！")
    else:
        print("\n⚠️ 安装完成，但连接测试未通过，请检查日志")
        sys.exit(1)


if __name__ == '__main__':
    main()
