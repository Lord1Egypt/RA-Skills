#!/bin/bash
# 自动化部署 - 快速配置脚本
# 用法：./setup.sh

set -e

echo "========================================"
echo "  自动化部署 - 快速配置向导"
echo "========================================"
echo ""

SCRIPT_DIR="$(dirname "$0")"
CONFIG_FILE="$SCRIPT_DIR/deploy-config.json"

# 步骤 1：生成 SSH Key
echo "📌 步骤 1/4: 生成 SSH Key"
echo ""

if [ -f ~/.ssh/server_deploy ]; then
    echo "⚠️  SSH Key 已存在，是否重新生成？(y/n)"
    read regenerate
    if [ "$regenerate" = "y" ]; then
        ssh-keygen -t ed25519 -C "openclaw-server" -f ~/.ssh/server_deploy -N ""
    else
        echo "✅ 使用现有 SSH Key"
    fi
else
    echo "生成新的 SSH Key..."
    ssh-keygen -t ed25519 -C "openclaw-server" -f ~/.ssh/server_deploy -N ""
fi

echo ""
echo "📋 公钥内容（复制添加到服务器）："
echo "----------------------------------------"
cat ~/.ssh/server_deploy.pub
echo "----------------------------------------"
echo ""
echo "请登录服务器执行："
echo "  mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
echo "  然后粘贴上面的公钥内容，按 Ctrl+D 结束"
echo ""
read -p "按回车继续..."

# 步骤 2：配置服务器信息
echo ""
echo "📌 步骤 2/4: 配置服务器信息"
echo ""

read -p "服务器 IP 地址： " SERVER_IP
read -p "SSH 端口（默认 22）： " SERVER_PORT
SERVER_PORT=${SERVER_PORT:-22}
read -p "SSH 用户（默认 root）： " SERVER_USER
SERVER_USER=${SERVER_USER:-root}
read -p "部署路径（默认 /www/wwwroot/points）： " DEPLOY_PATH
DEPLOY_PATH=${DEPLOY_PATH:-/www/wwwroot/points}
read -p "备份路径（默认 /www/backup/points）： " BACKUP_PATH
BACKUP_PATH=${BACKUP_PATH:-/www/backup/points}

# 步骤 3：验证 SSH 连接
echo ""
echo "📌 步骤 3/4: 验证 SSH 连接"
echo ""

echo "尝试连接服务器..."
if ssh -i ~/.ssh/server_deploy -p "$SERVER_PORT" -o ConnectTimeout=5 -o StrictHostKeyChecking=no "$SERVER_USER@$SERVER_IP" "echo 连接成功" 2>/dev/null; then
    echo "✅ SSH 连接成功！"
else
    echo "❌ SSH 连接失败，请检查："
    echo "  1. 服务器 IP 是否正确"
    echo "  2. SSH 端口是否开放"
    echo "  3. 公钥是否已添加到服务器"
    echo ""
    read -p "是否继续配置？(y/n): " continue_config
    if [ "$continue_config" != "y" ]; then
        exit 1
    fi
fi

# 步骤 4：更新配置文件
echo ""
echo "📌 步骤 4/4: 更新配置文件"
echo ""

# 备份原配置
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.bak.$(date +%Y%m%d%H%M%S)"
fi

# 使用 jq 更新配置（如果 jq 不存在则用 sed）
if command -v jq &> /dev/null; then
    jq --arg host "$SERVER_IP" \
       --argjson port "$SERVER_PORT" \
       --arg user "$SERVER_USER" \
       --arg deploy "$DEPLOY_PATH" \
       --arg backup "$BACKUP_PATH" \
       '.server.host = $host | .server.port = $port | .server.user = $user | .server.deployPath = $deploy | .server.backupPath = $backup' \
       "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    echo "✅ 配置文件已更新"
else
    echo "⚠️  jq 未安装，使用 sed 更新..."
    sed -i "s/\"host\": \"\${SERVER_HOST}\"/\"host\": \"$SERVER_IP\"/" "$CONFIG_FILE"
    sed -i "s/\"port\": 22/\"port\": $SERVER_PORT/" "$CONFIG_FILE"
    sed -i "s/\"user\": \"root\"/\"user\": \"$SERVER_USER\"/" "$CONFIG_FILE"
    sed -i "s|\"deployPath\": \"/www/wwwroot/points\"|\"deployPath\": \"$DEPLOY_PATH\"|" "$CONFIG_FILE"
    sed -i "s|\"backupPath\": \"/www/backup/points\"|\"backupPath\": \"$BACKUP_PATH\"|" "$CONFIG_FILE"
    echo "✅ 配置文件已更新"
fi

echo ""
echo "========================================"
echo "  ✅ 配置完成！"
echo "========================================"
echo ""
echo "📋 配置摘要："
echo "  - 服务器：$SERVER_USER@$SERVER_IP:$SERVER_PORT"
echo "  - 部署路径：$DEPLOY_PATH"
echo "  - 备份路径：$BACKUP_PATH"
echo "  - 配置文件：$CONFIG_FILE"
echo ""
echo "📝 下一步："
echo "  1. 编辑 $CONFIG_FILE 填写 Git 认证信息"
echo "  2. 运行 ./scripts/deploy.sh 测试部署"
echo ""
echo "或者对我说：'配置完成了，测试一下部署'"
echo "========================================"
