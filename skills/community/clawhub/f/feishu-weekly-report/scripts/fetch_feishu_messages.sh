#!/bin/bash
# Fetch Feishu chat messages for a given chat_id and time range
# Usage: fetch_feishu_messages.sh <app_id> <app_secret> <chat_id> <start_ts_seconds> <end_ts_seconds>
# Output: one JSON per message line (sender_type, sender_id, msg_type, content, create_time)
# Note: timestamps are in SECONDS (not milliseconds)

set -euo pipefail

APP_ID="${1:?Usage: $0 <app_id> <app_secret> <chat_id> <start_ts_s> <end_ts_s>}"
APP_SECRET="${2:?}"
CHAT_ID="${3:?}"
START_TS="${4:?}"
END_TS="${5:?}"

TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"${APP_ID}\",\"app_secret\":\"${APP_SECRET}\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

[ -z "$TOKEN" ] && { echo "ERROR: Failed to get token" >&2; exit 1; }

PAGE_TOKEN=""
HAS_MORE=true

while [ "$HAS_MORE" = "true" ]; do
  URL="https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id=${CHAT_ID}&start_time=${START_TS}&end_time=${END_TS}&sort_type=ByCreateTimeAsc&page_size=50"
  [ -n "$PAGE_TOKEN" ] && URL="${URL}&page_token=${PAGE_TOKEN}"

  RESP=$(curl -s "$URL" -H "Authorization: Bearer $TOKEN")
  CODE=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code','-1'))" 2>/dev/null || echo "-1")
  [ "$CODE" != "0" ] && { echo "ERROR: API code $CODE" >&2; exit 1; }

  echo "$RESP" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('data', {}).get('items', []):
    sender = item.get('sender', {})
    content = item.get('body', {}).get('content', '')
    try:
        c = json.loads(content)
        if isinstance(c, dict) and 'text' in c:
            content = c['text']
    except: pass
    print(json.dumps({
        'sender_type': sender.get('sender_type', ''),
        'sender_id': sender.get('id', ''),
        'msg_type': item.get('msg_type', ''),
        'content': content,
        'create_time': item.get('create_time', ''),
    }, ensure_ascii=False))
" 2>/dev/null

  HAS_MORE=$(echo "$RESP" | python3 -c "import sys,json; print(str(json.load(sys.stdin).get('data',{}).get('has_more',False)).lower())" 2>/dev/null || echo "false")
  PAGE_TOKEN=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('page_token',''))" 2>/dev/null || echo "")
  [ -z "$PAGE_TOKEN" ] && HAS_MORE=false
done
