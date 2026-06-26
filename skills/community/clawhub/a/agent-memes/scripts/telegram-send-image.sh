#!/bin/bash
# Usage: telegram-send-image.sh <chat_id> <image_path> [caption]
# Fast Telegram image send via curl.
#
# Env vars (all optional):
#   TELEGRAM_BOT_TOKEN - bot token (preferred, avoids reading openclaw.json)
#   TELEGRAM_PROXY     - proxy URL for curl (default: none)

set -euo pipefail

CHAT_ID="${1:?Usage: telegram-send-image.sh <chat_id> <image_path> [caption]}"
IMAGE_PATH="${2:?Missing image path}"
CAPTION="${3:-}"

if [ -n "${TELEGRAM_BOT_TOKEN:-}" ]; then
  TOKEN="$TELEGRAM_BOT_TOKEN"
else
  CREDENTIAL_HELPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" )" && pwd)/get-credential.sh"
  TOKEN=$(bash "$CREDENTIAL_HELPER" telegram)
fi

# Detect if GIF → use sendAnimation, otherwise sendPhoto
EXT="${IMAGE_PATH##*.}"
if [[ "${EXT,,}" == "gif" ]]; then
  API_METHOD="sendAnimation"
  FILE_FIELD="animation"
else
  API_METHOD="sendPhoto"
  FILE_FIELD="photo"
fi

CURL_ARGS=(
  -s
  --max-time 30
  -F "chat_id=${CHAT_ID}"
  -F "${FILE_FIELD}=@${IMAGE_PATH}"
)

if [ -n "$CAPTION" ]; then
  CURL_ARGS+=(-F "caption=${CAPTION}")
fi

PROXY="${TELEGRAM_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
if [ -n "$PROXY" ]; then
  CURL_ARGS+=(-x "$PROXY")
fi

RESULT=$(curl "${CURL_ARGS[@]}" "https://api.telegram.org/bot${TOKEN}/${API_METHOD}")

echo "$RESULT" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);if(r.ok)console.log('Sent! Message ID: '+r.result.message_id);else{console.error(r.description||JSON.stringify(r));process.exit(1)}}catch{console.error(d);process.exit(1)}})"
