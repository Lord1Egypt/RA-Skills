#!/bin/bash
# Usage: discord-send-image.sh <channel_id> <image_path> [caption]
# Fast Discord image send via curl, bypassing OpenClaw CLI startup overhead.
#
# Env vars (all optional):
#   DISCORD_BOT_TOKEN - bot token (preferred, avoids reading openclaw.json)
#   DISCORD_ACCOUNT  - account name in openclaw.json (fallback if no DISCORD_BOT_TOKEN)
#   DISCORD_PROXY    - proxy URL for curl, e.g. socks5h://127.0.0.1:1080 (default: none)

set -euo pipefail

CHANNEL_ID="${1:?Usage: discord-send-image.sh <channel_id> <image_path> [caption]}"
IMAGE_PATH="${2:?Missing image path}"
CAPTION="${3:-}"

ACCOUNT="${DISCORD_ACCOUNT:-}"

# Read bot token via centralized credential helper
CREDENTIAL_HELPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" )" && pwd)/get-credential.sh"
export DISCORD_ACCOUNT="$ACCOUNT"
TOKEN=$(bash "$CREDENTIAL_HELPER" discord)

CURL_ARGS=(
  -s
  --max-time 15
  -H "Authorization: Bot $TOKEN"
  -F "files[0]=@${IMAGE_PATH}"
)

# Add proxy if configured
PROXY="${DISCORD_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
if [ -n "$PROXY" ]; then
  CURL_ARGS+=(-x "$PROXY")
fi

if [ -n "$CAPTION" ]; then
  CURL_ARGS+=(-F "payload_json={\"content\":\"${CAPTION}\"}")
fi

RESULT=$(curl "${CURL_ARGS[@]}" "https://discord.com/api/v10/channels/${CHANNEL_ID}/messages")

MSG_ID=$(echo "$RESULT" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);if(r.id)console.log('Sent! Message ID: '+r.id);else{console.error(JSON.stringify(r));process.exit(1)}}catch{console.error(d);process.exit(1)}})")

echo "$MSG_ID"
