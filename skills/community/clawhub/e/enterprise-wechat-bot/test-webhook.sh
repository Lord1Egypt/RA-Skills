#!/bin/bash
# 企业微信 Webhook 测试脚本
# 使用方法：./test-webhook.sh YOUR_WEBHOOK_KEY

WEBHOOK_KEY="${1:-YOUR_WEBHOOK_KEY}"
WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=${WEBHOOK_KEY}"

echo "测试企业微信 Webhook..."
echo "URL: $WEBHOOK_URL"
echo ""

# 发送测试消息
RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "🦞 小鸣 AI 测试消息\n\n如果收到这条消息，说明 Webhook 配置成功！\n\n时间: '"$(date)"'\n状态：测试中"
    }
  }')

echo "响应:"
echo "$RESPONSE"
echo ""

# 检查响应
if echo "$RESPONSE" | grep -q '"errcode": 0'; then
  echo "✅ 测试成功！Webhook 配置正确。"
  exit 0
elif echo "$RESPONSE" | grep -q '"errcode": 301001'; then
  echo "❌ Key 无效，请检查 Webhook Key 是否正确。"
  exit 1
elif echo "$RESPONSE" | grep -q '"errcode": 301002'; then
  echo "⚠️ 参数错误，请检查请求格式。"
  exit 1
else
  echo "⚠️ 未知响应，请检查网络或 API 文档。"
  exit 2
fi
