#!/usr/bin/env bash
# 一键完成完整 Device Flow: 申请码 → 打开浏览器 → 自动轮询 → 保存 token
# 用法: bash auth-flow.sh [base_url]
# 全自动，无需人工干预（除了在浏览器里点允许）

set -euo pipefail

BASE_URL="${1:-https://api.caremax.ai}"
CREDS_FILE="$HOME/.caremax/credentials.json"

# Step 1: 申请设备码
DEVICE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/device" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"caremax-agent","scope":"read:indicators read:records read:members write:upload write:ocr search:records"}')

DEVICE_CODE=$(echo "$DEVICE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['device_code'])" 2>/dev/null) || {
  echo "{\"status\":\"error\",\"message\":\"Failed to get device code\"}"
  exit 1
}
VERIFY_URL=$(echo "$DEVICE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['verification_uri_complete'])")
INTERVAL=$(echo "$DEVICE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('interval',5))")

# Step 2: 打开浏览器
if command -v open &>/dev/null; then
  open "$VERIFY_URL"
elif command -v xdg-open &>/dev/null; then
  xdg-open "$VERIFY_URL"
fi

echo "Authorization page opened: $VERIFY_URL"
echo "Waiting for user to approve..."

# Step 3: 自动轮询（最多等 15 分钟）
MAX_ATTEMPTS=$(( 900 / INTERVAL ))
for i in $(seq 1 $MAX_ATTEMPTS); do
  sleep "$INTERVAL"

  TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/device/token" \
    -H "Content-Type: application/json" \
    -d "{\"device_code\":\"$DEVICE_CODE\",\"grant_type\":\"device_code\"}")

  # 检查是否拿到 token
  if echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'access_token' in d" 2>/dev/null; then
    # 保存 credentials
    mkdir -p "$HOME/.caremax"
    python3 -c "
import json
from datetime import datetime, timedelta
resp = json.loads('''$TOKEN_RESPONSE''')
creds = {
    'access_token': resp['access_token'],
    'refresh_token': resp['refresh_token'],
    'expires_at': (datetime.utcnow() + timedelta(seconds=resp['expires_in'])).isoformat() + 'Z',
    'scope': resp['scope'],
    'base_url': '$BASE_URL'
}
json.dump(creds, open('$CREDS_FILE', 'w'), indent=2)
print(json.dumps({'status': 'authorized', 'access_token': resp['access_token'], 'base_url': '$BASE_URL'}))
"
    exit 0
  fi

  # 检查错误类型
  ERROR=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('error','unknown'))" 2>/dev/null || echo "unknown")

  if [ "$ERROR" = "authorization_pending" ]; then
    continue
  elif [ "$ERROR" = "access_denied" ]; then
    echo "{\"status\":\"denied\",\"message\":\"User denied authorization\"}"
    exit 1
  elif [ "$ERROR" = "expired_token" ]; then
    echo "{\"status\":\"expired\",\"message\":\"Authorization code expired\"}"
    exit 1
  else
    echo "{\"status\":\"error\",\"message\":\"Unexpected error: $ERROR\"}"
    exit 1
  fi
done

echo "{\"status\":\"timeout\",\"message\":\"Authorization timed out after 15 minutes\"}"
exit 1
