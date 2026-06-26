#!/usr/bin/env bash
# 用 refresh_token 刷新 access_token
# 用法: bash refresh-token.sh
# 前提: ~/.caremax/credentials.json 存在且有 refresh_token
# 输出: 成功返回 {"status":"refreshed","access_token":"..."}, 失败返回 {"status":"refresh_failed",...}

set -euo pipefail

CREDS_FILE="$HOME/.caremax/credentials.json"
BASE_URL=$(python3 -c "import json; print(json.load(open('$CREDS_FILE')).get('base_url','https://api.caremax.ai'))")
REFRESH_TOKEN=$(python3 -c "import json; print(json.load(open('$CREDS_FILE'))['refresh_token'])")

RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/device/refresh" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\":\"$REFRESH_TOKEN\",\"grant_type\":\"refresh_token\"}")

# 检查是否成功
if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'access_token' in d" 2>/dev/null; then
  python3 -c "
import json
from datetime import datetime, timedelta

resp = json.loads('''$RESPONSE''')
creds = json.load(open('$CREDS_FILE'))
creds['access_token'] = resp['access_token']
creds['expires_at'] = (datetime.utcnow() + timedelta(seconds=resp['expires_in'])).isoformat() + 'Z'
json.dump(creds, open('$CREDS_FILE', 'w'), indent=2)

print(json.dumps({
    'status': 'refreshed',
    'access_token': resp['access_token'],
    'base_url': creds.get('base_url', 'https://api.caremax.ai')
}))
"
else
  echo "{\"status\":\"refresh_failed\",\"error\":$RESPONSE}"
fi
