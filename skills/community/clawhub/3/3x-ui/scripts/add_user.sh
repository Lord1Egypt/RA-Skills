#!/bin/bash
# 添加新用户到3x-ui面板
# 用法: ./add_user.sh <panel_url> <token> <email> <total_GB> <expiry_days> <inbound_ids>
# 示例: ./add_user.sh https://panel.example.com:2053 "Bearer eyJ..." user@example.com 50 30 "[3,5]"

PANEL_URL="$1"
TOKEN="$2"
EMAIL="$3"
TOTAL_GB="${4:-10}"
EXPIRY_DAYS="${5:-30}"
INBOUND_IDS="${6:-[]}"

if [ -z "$PANEL_URL" ] || [ -z "$TOKEN" ] || [ -z "$EMAIL" ]; then
  echo "用法: $0 <panel_url> <token> <email> [total_GB] [expiry_days] [inbound_ids]"
  echo "示例: $0 https://panel.example.com:2053 'Bearer eyJ...' user@example.com 50 30 '[3,5]'"
  exit 1
fi

# 计算过期时间（毫秒时间戳）
EXPIRY_TS=$(( $(date +%s) + EXPIRY_DAYS * 86400 ))
EXPIRY_TS_MS=$(( EXPIRY_TS * 1000 ))

# 计算流量（字节）
TOTAL_BYTES=$(( TOTAL_GB * 1024 * 1024 * 1024 ))

echo "添加用户: $EMAIL"
echo "流量: ${TOTAL_GB}GB"
echo "过期: ${EXPIRY_DAYS}天后 ($(date -r $EXPIRY_TS '+%Y-%m-%d %H:%M:%S'))"
echo "入站: $INBOUND_IDS"
echo ""

RESPONSE=$(curl -s -X POST "${PANEL_URL}/panel/api/clients/add" \
  -H "Authorization: ${TOKEN}" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{
    \"client\": {
      \"email\": \"${EMAIL}\",
      \"totalGB\": ${TOTAL_BYTES},
      \"expiryTime\": ${EXPIRY_TS_MS},
      \"tgId\": 0,
      \"limitIp\": 0,
      \"enable\": true
    },
    \"inboundIds\": ${INBOUND_IDS}
  }")

echo "$RESPONSE" | python3 -m json.tool

# 如果成功，显示订阅链接
if echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('success') else 1)" 2>/dev/null; then
  echo ""
  echo "=== 订阅链接 ==="
  curl -s -X GET "${PANEL_URL}/panel/api/clients/links/${EMAIL}" \
    -H "Authorization: ${TOKEN}" \
    -H "Accept: application/json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('success'):
    for link in data.get('obj', []):
        print(link)
"
fi
