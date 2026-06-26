#!/bin/bash
# Usage: whatsapp-send-image.sh <recipient_phone> <image_path> [caption]
# WhatsApp Cloud API image send via curl (two-step: upload media, then send).
#
# Env vars (all optional):
#   WHATSAPP_TOKEN    - access token (preferred)
#   WHATSAPP_PHONE_ID - phone number ID (preferred)
#   WHATSAPP_PROXY    - proxy URL for curl (default: none)

set -euo pipefail

RECIPIENT="${1:?Usage: whatsapp-send-image.sh <recipient_phone> <image_path> [caption]}"
IMAGE_PATH="${2:?Missing image path}"
CAPTION="${3:-}"

if [ -n "${WHATSAPP_TOKEN:-}" ]; then
  TOKEN="$WHATSAPP_TOKEN"
  PHONE_ID="${WHATSAPP_PHONE_ID:?WHATSAPP_PHONE_ID is required when using WHATSAPP_TOKEN}"
else
  CREDENTIAL_HELPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" )" && pwd)/get-credential.sh"
  read -r TOKEN PHONE_ID < <(bash "$CREDENTIAL_HELPER" whatsapp)
fi

PROXY="${WHATSAPP_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
PROXY_ARGS=()
if [ -n "$PROXY" ]; then
  PROXY_ARGS=(-x "$PROXY")
fi

MIME=$(file -b --mime-type "$IMAGE_PATH")

# Step 1: Upload media
UPLOAD=$(curl -s --max-time 30 "${PROXY_ARGS[@]}" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@${IMAGE_PATH};type=${MIME}" \
  -F "messaging_product=whatsapp" \
  -F "type=image" \
  "https://graph.facebook.com/v21.0/${PHONE_ID}/media")

MEDIA_ID=$(echo "$UPLOAD" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);if(r.id)console.log(r.id);else{console.error(r.error?.message||JSON.stringify(r));process.exit(1)}})")

# Step 2: Send message
BODY="{\"messaging_product\":\"whatsapp\",\"to\":\"${RECIPIENT}\",\"type\":\"image\",\"image\":{\"id\":\"${MEDIA_ID}\""
if [ -n "$CAPTION" ]; then
  BODY+=",\"caption\":\"${CAPTION}\""
fi
BODY+="}}"

RESULT=$(curl -s --max-time 15 "${PROXY_ARGS[@]}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  "https://graph.facebook.com/v21.0/${PHONE_ID}/messages")

echo "$RESULT" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);if(r.messages?.[0]?.id)console.log('Sent! Message ID: '+r.messages[0].id);else{console.error(r.error?.message||JSON.stringify(r));process.exit(1)}}catch{console.error(d);process.exit(1)}})"
