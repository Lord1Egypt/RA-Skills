#!/bin/bash
# Send a Feishu IM message as the app (bot identity)
# Usage: ./send-message.sh <receive_id> <msg_type> <content_json_string> [open_id|chat_id]
set -e

RECEIVE_ID="${1:-${FEISHU_RECEIVE_ID}}"
MSG_TYPE="${2:-${FEISHU_MSG_TYPE:-text}}"
CONTENT="${3:-${FEISHU_CONTENT}}"
RECEIVE_ID_TYPE="${4:-open_id}"

OPENCLAW_JSON="${OPENCLAW_JSON:-/root/.openclaw/openclaw.json}"

get_cred() {
    python3 -c "import json; d=json.load(open('$OPENCLAW_JSON')); print(d['channels']['feishu']['$1'])"
}

APP_ID=$(get_cred appId)
APP_SECRET=$(get_cred appSecret)
API_BASE="https://open.feishu.cn/open-apis"
TOKEN_CACHE="/tmp/feishu_app_token.cache"

[ -z "$RECEIVE_ID" ] || [ -z "$CONTENT" ] && {
    echo "Usage: $0 <receive_id> <msg_type> <content_json_string> [open_id|chat_id]"
    echo ""
    echo "Examples:"
    echo "  text:  '{\"text\":\"Hello\"}'"
    echo "  image: '{\"image_key\":\"img_v3_xxx\"}'"
    exit 1
}

# ── Get App Token (cached) ───────────────────────────────────
get_app_token() {
    local NOW=$(date +%s)
    
    if [ -f "$TOKEN_CACHE" ]; then
        local EXPIRES_AT=$(cat "$TOKEN_CACHE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expires_at',0))" 2>/dev/null)
        local TOKEN=$(cat "$TOKEN_CACHE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))" 2>/dev/null)
        if [ -n "$TOKEN" ] && [ "$NOW" -lt "$((EXPIRES_AT - 300))" ]; then
            echo "$TOKEN"
            return 0
        fi
    fi
    
    local RESP=$(curl -s -X POST "$API_BASE/auth/v3/app_access_token/internal" \
        -H "Content-Type: application/json" \
        -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")
    
    local TOKEN=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('app_access_token',''))" 2>/dev/null)
    local EXPIRES_IN=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expire',7200))" 2>/dev/null)
    
    if [ -z "$TOKEN" ]; then
        echo "Failed to get App Token: $RESP" >&2
        return 1
    fi
    
    echo "{\"token\":\"$TOKEN\",\"expires_at\":$((NOW + EXPIRES_IN - 300))}" > "$TOKEN_CACHE"
    echo "$TOKEN"
}

# ── Send via python (avoids bash quoting hell) ────────────────
APP_TOKEN=$(get_app_token) || exit 1

python3 - "$APP_TOKEN" "$RECEIVE_ID" "$MSG_TYPE" "$CONTENT" "$RECEIVE_ID_TYPE" << 'EOF'
import sys, json, subprocess

token = sys.argv[1]
receive_id = sys.argv[2]
msg_type = sys.argv[3]
content = sys.argv[4]
receive_id_type = sys.argv[5] if len(sys.argv) > 5 else "open_id"

payload = {
    "receive_id": receive_id,
    "msg_type": msg_type,
    "content": content
}

result = subprocess.run([
    "curl", "-s", "-X", "POST",
    f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
    "-H", f"Authorization: Bearer {token}",
    "-H", "Content-Type: application/json",
    "-d", json.dumps(payload)
], capture_output=True, text=True)

resp = json.loads(result.stdout)
msg_id = resp.get("data", {}).get("message_id", "")
if not msg_id:
    print("Send failed:", result.stdout, file=sys.stderr)
    sys.exit(1)
print("message_id:", msg_id)
EOF
