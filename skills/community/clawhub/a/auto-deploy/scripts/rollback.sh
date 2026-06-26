#!/bin/bash
# 部署回滚脚本
# 用法：./rollback.sh [备份版本名称]

set -e

CONFIG_FILE="$(dirname "$0")/deploy-config.json"
SSH_KEY="$HOME/.ssh/server_deploy"

# 读取配置
SERVER_HOST=$(jq -r '.server.host' "$CONFIG_FILE")
SERVER_PORT=$(jq -r '.server.port' "$CONFIG_FILE")
SERVER_USER=$(jq -r '.server.user' "$CONFIG_FILE")
DEPLOY_PATH=$(jq -r '.server.deployPath' "$CONFIG_FILE")
BACKUP_PATH=$(jq -r '.server.backupPath' "$CONFIG_FILE")

echo "========================================"
echo "  部署回滚脚本"
echo "========================================"

# 获取可用备份列表
echo "可用备份版本："
ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" "ls -lt $BACKUP_PATH | head -10"

if [ -z "$1" ]; then
    # 使用最新备份
    BACKUP_NAME=$(ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" "ls -t $BACKUP_PATH | head -1")
    echo "未指定版本，使用最新备份：$BACKUP_NAME"
else
    BACKUP_NAME="$1"
fi

echo ""
read -p "确认回滚到 $BACKUP_NAME？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 回滚取消"
    exit 1
fi

echo "开始回滚..."

ssh -i "$SSH_KEY" -p "$SERVER_PORT" "$SERVER_USER@$SERVER_HOST" << EOF
  echo "停止服务..."
  pm2 stop points 2>/dev/null || systemctl stop points-service 2>/dev/null || true
  
  echo "恢复备份..."
  rm -rf $DEPLOY_PATH/*
  cp -r $BACKUP_PATH/$BACKUP_NAME/* $DEPLOY_PATH/
  
  echo "启动服务..."
  pm2 start points 2>/dev/null || systemctl start points-service 2>/dev/null || true
  
  echo "✅ 回滚完成！"
EOF

echo "========================================"
echo "✅ 回滚成功完成！"
echo "========================================"
