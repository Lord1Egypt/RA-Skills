#!/bin/bash
# Upload image to Feishu and return the image_key
# Usage: ./upload-image.sh <image_path>
#   or set env: FEISHU_IMAGE_PATH, FEISHU_APP_ID, FEISHU_APP_SECRET
set -e

IMAGE_PATH="${1:-${FEISHU_IMAGE_PATH}}"

OPENCLAW_JSON="${OPENCLAW_JSON:-/root/.openclaw/openclaw.json}"

# Read credentials from openclaw.json (required)
get_cred() {
    python3 -c "import json; d=json.load(open('$OPENCLAW_JSON')); print(d['channels']['feishu']['$1'])"
}

APP_ID="${FEISHU_APP_ID:-$(get_cred appId)}"
APP_SECRET="${FEISHU_APP_SECRET:-$(get_cred appSecret)}"
API_BASE="https://open.feishu.cn/open-apis"
TOKEN_CACHE="/tmp/feishu_app_token.cache"

[ -z "$IMAGE_PATH" ] && {
    echo "Usage: $0 <image_path>"
    echo "   or set FEISHU_IMAGE_PATH"
    exit 1
}
[ ! -f "$IMAGE_PATH" ] && { echo "File not found: $IMAGE_PATH"; exit 1; }
[ -z "$APP_ID" ] || [ -z "$APP_SECRET" ] && {
    echo "ERROR: Missing credentials. Set FEISHU_APP_ID and FEISHU_APP_SECRET, or ensure openclaw.json has channels.feishu.appId/appSecret"
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

# ── Upload ───────────────────────────────────────────────────
APP_TOKEN=$(get_app_token) || exit 1

RESP=$(curl -s -X POST "$API_BASE/im/v1/images" \
    -H "Authorization: Bearer $APP_TOKEN" \
    -F "image_type=message" \
    -F "image=@$IMAGE_PATH;type=image/png")

IMAGE_KEY=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('image_key',''))")

if [ -z "$IMAGE_KEY" ]; then
    echo "Upload failed: $RESP" >&2
    exit 1
fi

echo "$IMAGE_KEY"
