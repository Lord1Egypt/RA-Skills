#!/bin/bash
# Usage: wechat-send-image.sh <target> <image_path> [caption]
# 企业微信 (WeCom) image send via curl (two-step: upload media, then send).
# <target> is a userid or @all.
#
# Env vars (all optional):
#   WECHAT_CORP_ID     - corp ID (preferred)
#   WECHAT_CORP_SECRET - corp secret (preferred)
#   WECHAT_AGENT_ID    - agent ID (preferred, or reads from openclaw.json)
#   WECHAT_PROXY       - proxy URL for curl (default: none)

set -euo pipefail

TARGET="${1:?Usage: wechat-send-image.sh <target> <image_path> [caption]}"
IMAGE_PATH="${2:?Missing image path}"
CAPTION="${3:-}"

if [ -n "${WECHAT_CORP_ID:-}" ] && [ -n "${WECHAT_CORP_SECRET:-}" ]; then
  CORP_ID="$WECHAT_CORP_ID"
  CORP_SECRET="$WECHAT_CORP_SECRET"
  AGENT_ID="${WECHAT_AGENT_ID:-}"
else
  CREDENTIAL_HELPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" )" && pwd)/get-credential.sh"
  read -r CORP_ID CORP_SECRET AGENT_ID < <(bash "$CREDENTIAL_HELPER" wechat)
fi

PROXY="${WECHAT_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
PROXY_ARGS=()
if [ -n "$PROXY" ]; then
  PROXY_ARGS=(-x "$PROXY")
fi

# Step 1: Get access token
TOKEN_RESULT=$(curl -s --max-time 10 "${PROXY_ARGS[@]}" \
  "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=${CORP_ID}&corpsecret=${CORP_SECRET}")

ACCESS_TOKEN=$(echo "$TOKEN_RESULT" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);if(r.errcode!==0){console.error(r.errmsg||JSON.stringify(r));process.exit(1)}console.log(r.access_token)})")

# Step 2: Upload media
UPLOAD=$(curl -s --max-time 30 "${PROXY_ARGS[@]}" \
  -F "media=@${IMAGE_PATH}" \
  "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=${ACCESS_TOKEN}&type=image")

MEDIA_ID=$(echo "$UPLOAD" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);if(r.errcode!==0){console.error(r.errmsg||JSON.stringify(r));process.exit(1)}console.log(r.media_id)})")

# Step 3: Send image message
BODY="{\"touser\":\"${TARGET}\",\"msgtype\":\"image\",\"image\":{\"media_id\":\"${MEDIA_ID}\"}}"
if [ -n "$AGENT_ID" ]; then
  BODY=$(echo "$BODY" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);r.agentid=Number('${AGENT_ID}');console.log(JSON.stringify(r))})")
fi

RESULT=$(curl -s --max-time 15 "${PROXY_ARGS[@]}" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${ACCESS_TOKEN}")

echo "$RESULT" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);if(r.errcode===0)console.log('Sent! msgid: '+r.msgid);else{console.error(r.errmsg||JSON.stringify(r));process.exit(1)}}catch{console.error(d);process.exit(1)}})"

# Note: WeCom doesn't support captions on image messages natively.
# If caption is provided, send a follow-up text message.
if [ -n "$CAPTION" ]; then
  TEXT_BODY="{\"touser\":\"${TARGET}\",\"msgtype\":\"text\",\"text\":{\"content\":\"${CAPTION}\"}}"
  if [ -n "$AGENT_ID" ]; then
    TEXT_BODY=$(echo "$TEXT_BODY" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);r.agentid=Number('${AGENT_ID}');console.log(JSON.stringify(r))})")
  fi
  curl -s --max-time 15 "${PROXY_ARGS[@]}" \
    -H "Content-Type: application/json" \
    -d "$TEXT_BODY" \
    "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=${ACCESS_TOKEN}" > /dev/null
fi
