#!/bin/bash
# 查看当前在线用户
# 用法: ./online_users.sh <panel_url> <token>

PANEL_URL="$1"
TOKEN="$2"

if [ -z "$PANEL_URL" ] || [ -z "$TOKEN" ]; then
  echo "用法: $0 <panel_url> <token>"
  exit 1
fi

echo "=== 在线用户 ==="
curl -s -X POST "${PANEL_URL}/panel/api/clients/onlines" \
  -H "Authorization: ${TOKEN}" \
  -H "Accept: application/json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('success'):
    users = data.get('obj', [])
    print(f'在线人数: {len(users)}')
    for u in users:
        print(f'  - {u}')
else:
    print(f'错误: {data.get(\"msg\", \"未知\")}')
"
