#!/bin/bash
# 使用 SSH 密码连接并配置公钥

SERVER_IP="192.168.1.168"
SERVER_USER="root"
SERVER_PASSWORD="zhangjiamin"
SSH_KEY_PUB="/home/node/.ssh/server_deploy.pub"

# 读取公钥
PUBLIC_KEY=$(cat $SSH_KEY_PUB)

echo "🔑 正在配置 SSH Key 到服务器..."
echo ""

# 使用 ssh 命令配合密码输入
ssh ${SERVER_USER}@${SERVER_IP} << EOF
yes
$SERVER_PASSWORD
mkdir -p ~/.ssh
echo "$PUBLIC_KEY" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
echo "✅ SSH Key 配置完成"
exit
EOF
