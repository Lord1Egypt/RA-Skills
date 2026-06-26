#!/bin/bash
# send-message.sh - 通用飞书消息发送脚本
# 用法：./send-message.sh {agent} {target} {msg_type} {message}
#   agent: ass 或 ops
#   target: open_id (私聊) 或 chat_id (群聊)
#   msg_type: open_id (私聊) 或 chat_id (群聊)
#   message: 消息内容

set -e

AGENT=$1
TARGET=$2
MSG_TYPE=$3
MESSAGE=$4

if [ -z "$AGENT" ] || [ -z "$TARGET" ] || [ -z "$MSG_TYPE" ] || [ -z "$MESSAGE" ]; then
    echo "用法：$0 {agent} {target} {msg_type} {message}"
    echo "示例:"
    echo "  $0 ass ou_afa28cfc5689f929f1b1d8f3b09b9408 open_id \"私聊消息\""
    echo "  $0 ass oc_88fbbe55e37eca3c3339b2f4bae1a8a9 chat_id \"群聊消息\""
    echo "  $0 ops ou_xxxxxxxxxxxxxxxxxxxxxxxxxxx open_id \"运维消息\""
    exit 1
fi

# 配置文件路径
CONFIG_FILE="$HOME/.openclaw/openclaw-${AGENT}.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误：配置文件不存在：$CONFIG_FILE"
    exit 1
fi

# 读取配置
APP_ID=$(jq -r '.channels.feishu.appId' "$CONFIG_FILE")
APP_SECRET=$(jq -r '.channels.feishu.appSecret' "$CONFIG_FILE")

if [ -z "$APP_ID" ] || [ -z "$APP_SECRET" ] || [ "$APP_ID" == "null" ] || [ "$APP_SECRET" == "null" ]; then
    echo "错误：无法从配置文件中读取飞书凭证"
    exit 1
fi

echo "=== 使用 $AGENT Agent 发送消息 ==="
echo "App ID: $APP_ID"
echo "目标：$TARGET ($MSG_TYPE)"
echo "消息：$MESSAGE"
echo ""

# 获取 token
echo "获取 token..."
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/ \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | jq -r '.tenant_access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
    echo "错误：无法获取 token"
    exit 1
fi

# 发送消息
echo "发送消息..."
RESULT=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${MSG_TYPE}" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"$TARGET\",\"msg_type\":\"text\",\"content\":\"{\\\"text\\\":\\\"$MESSAGE\\\"}\"}")

CODE=$(echo "$RESULT" | jq -r '.code')
MSG_ID=$(echo "$RESULT" | jq -r '.data.message_id // empty')

if [ "$CODE" == "0" ]; then
    echo "✅ 发送成功！"
    echo "消息 ID: $MSG_ID"
else
    echo "❌ 发送失败！"
    echo "错误码：$CODE"
    echo "错误信息：$(echo "$RESULT" | jq -r '.msg')"
    exit 1
fi
