#!/bin/bash
# Usage: slack-send-image.sh <channel_id> <image_path> [caption]
# Slack image send via files.upload v2 API (curl).
#
# Env vars (all optional):
#   SLACK_BOT_TOKEN - bot token (preferred, avoids reading openclaw.json)
#   SLACK_PROXY     - proxy URL for curl (default: none)

set -euo pipefail

CHANNEL_ID="${1:?Usage: slack-send-image.sh <channel_id> <image_path> [caption]}"
IMAGE_PATH="${2:?Missing image path}"
CAPTION="${3:-}"

if [ -n "${SLACK_BOT_TOKEN:-}" ]; then
  TOKEN="$SLACK_BOT_TOKEN"
else
  CREDENTIAL_HELPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" )" && pwd)/get-credential.sh"
  TOKEN=$(bash "$CREDENTIAL_HELPER" slack)
fi

PROXY="${SLACK_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
PROXY_ARGS=()
if [ -n "$PROXY" ]; then
  PROXY_ARGS=(-x "$PROXY")
fi

FILENAME=$(basename "$IMAGE_PATH")
FILESIZE=$(stat -c%s "$IMAGE_PATH" 2>/dev/null || stat -f%z "$IMAGE_PATH")

# Step 1: Get upload URL
UPLOAD=$(curl -s --max-time 15 "${PROXY_ARGS[@]}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"filename\":\"${FILENAME}\",\"length\":${FILESIZE}}" \
  "https://slack.com/api/files.getUploadURLExternal")

UPLOAD_URL=$(echo "$UPLOAD" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);if(!r.ok){console.error(r.error||JSON.stringify(r));process.exit(1)}console.log(r.upload_url)})")
FILE_ID=$(echo "$UPLOAD" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const r=JSON.parse(d);console.log(r.file_id)})")

# Step 2: Upload file content
curl -s --max-time 30 "${PROXY_ARGS[@]}" \
  -F "file=@${IMAGE_PATH}" \
  "$UPLOAD_URL" > /dev/null

# Step 3: Complete upload and share to channel
CHANNEL_JSON="{\"id\":\"${CHANNEL_ID}\"}"
COMPLETE=$(curl -s --max-time 15 "${PROXY_ARGS[@]}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"files\":[{\"id\":\"${FILE_ID}\",\"title\":\"${CAPTION:-${FILENAME}}\"}],\"channel_id\":\"${CHANNEL_ID}\",\"initial_comment\":\"${CAPTION:-}\"}" \
  "https://slack.com/api/files.completeUploadExternal")

echo "$COMPLETE" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const r=JSON.parse(d);if(r.ok)console.log('Sent! File ID: ${FILE_ID}');else{console.error(r.error||JSON.stringify(r));process.exit(1)}}catch{console.error(d);process.exit(1)}})"
