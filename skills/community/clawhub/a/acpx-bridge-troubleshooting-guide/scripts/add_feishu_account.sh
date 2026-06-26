#!/bin/bash
# add_feishu_account.sh - 添加飞书多账户配置
# 使用 openclaw config set 命令而非直接修改 JSON

set -e

if [ $# -lt 3 ]; then
    echo "用法：$0 <account_name> <app_id> <app_secret>"
    echo "示例：$0 claude cli_a944379913b85ccb your_app_secret"
    exit 1
fi

ACCOUNT_NAME=$1
APP_ID=$2
APP_SECRET=$3

echo "🦞 添加飞书账户：$ACCOUNT_NAME"

# 使用 openclaw config set 命令添加账户
openclaw config set "channels.feishu.accounts.$ACCOUNT_NAME" "{\"appId\":\"$APP_ID\",\"appSecret\":\"$APP_SECRET\",\"domain\":\"feishu\",\"connectionMode\":\"websocket\"}"

echo "✅ 账户配置已添加"

# 验证配置
echo "🔍 验证配置..."
openclaw config validate

# 重启 Gateway
echo "🔄 重启 Gateway..."
openclaw gateway restart

echo ""
echo "✅ 完成！新飞书账户 $ACCOUNT_NAME 已配置并生效"
