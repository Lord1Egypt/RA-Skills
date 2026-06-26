#!/bin/bash
# Usage: line-send-image.sh <user_or_group_id> <image_path_or_url> [caption]
# Send an image via LINE Messaging API (push message).
#
# Accepts both local file paths and public URLs.
# Local files are auto-uploaded to catbox.moe (free, no auth, 200MB max).
#
# Env vars (all optional):
#   LINE_CHANNEL_ACCESS_TOKEN - channel access token (preferred)
#   LINE_ACCOUNT              - account name in openclaw.json (fallback)
#   LINE_PROXY                - proxy URL for curl (default: none)

set -euo pipefail

TARGET_ID="${1:?Usage: line-send-image.sh <user_or_group_id> <image_path_or_url> [caption]}"
IMAGE_INPUT="${2:?Missing image path or URL}"
CAPTION="${3:-}"

# If local file, upload to catbox.moe to get a public URL
if [[ ! "$IMAGE_INPUT" =~ ^https?:// ]]; then
  if [[ ! -f "$IMAGE_INPUT" ]]; then
    echo "Error: File not found: $IMAGE_INPUT" >&2
    exit 1
  fi
  PROXY="${LINE_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
  UPLOAD_ARGS=(-s --max-time 30 -F "reqtype=fileupload" -F "time=24h" -F "fileToUpload=@$IMAGE_INPUT")
  [[ -n "${PROXY:-}" ]] && UPLOAD_ARGS+=(-x "$PROXY")
  IMAGE_URL=$(curl "${UPLOAD_ARGS[@]}" "https://litterbox.catbox.moe/resources/internals/api.php")
  if [[ ! "$IMAGE_URL" =~ ^https:// ]]; then
    echo "Error: Upload failed: $IMAGE_URL" >&2
    exit 1
  fi
  echo "Uploaded: $IMAGE_URL" >&2
else
  IMAGE_URL="$IMAGE_INPUT"
fi

ACCOUNT="${LINE_ACCOUNT:-}"

# Read token: env var preferred, fallback to openclaw config
if [ -n "${LINE_CHANNEL_ACCESS_TOKEN:-}" ]; then
  TOKEN="$LINE_CHANNEL_ACCESS_TOKEN"
else
  CREDENTIAL_HELPER="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" )" && pwd)/get-credential.sh"
  export LINE_ACCOUNT="$ACCOUNT"
  TOKEN=$(bash "$CREDENTIAL_HELPER" line)
fi

# Build messages array
MESSAGES='[{"type":"image","originalContentUrl":"'"$IMAGE_URL"'","previewImageUrl":"'"$IMAGE_URL"'"}]'
if [ -n "$CAPTION" ]; then
  MESSAGES='[{"type":"text","text":"'"$(echo "$CAPTION" | sed 's/"/\\"/g')"'"},{"type":"image","originalContentUrl":"'"$IMAGE_URL"'","previewImageUrl":"'"$IMAGE_URL"'"}]'
fi

PAYLOAD=$(cat <<EOF
{"to":"${TARGET_ID}","messages":${MESSAGES}}
EOF
)

CURL_ARGS=(
  -s
  --max-time 15
  -H "Content-Type: application/json"
  -H "Authorization: Bearer $TOKEN"
  -d "$PAYLOAD"
)

# Add proxy if configured
PROXY="${LINE_PROXY:-${https_proxy:-${HTTPS_PROXY:-}}}"
if [ -n "$PROXY" ]; then
  CURL_ARGS+=(-x "$PROXY")
fi

RESULT=$(curl "${CURL_ARGS[@]}" "https://api.line.me/v2/bot/message/push")

# LINE returns {} on success, or {"message":"error..."} on failure
if echo "$RESULT" | grep -q '"message"'; then
  echo "Error: $RESULT" >&2
  exit 1
fi

echo "Sent!"
