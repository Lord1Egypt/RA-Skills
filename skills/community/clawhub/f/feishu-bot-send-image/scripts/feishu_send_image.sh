#!/bin/bash
# Send an image to a Feishu user/chat via Feishu Bot API
# Usage: feishu_send_image.sh <image_path> <receive_id> <app_id> <app_secret> [receive_id_type]
#
# Arguments:
#   image_path       - Local path to the image file (png/jpg/gif/webp)
#   receive_id       - Feishu open_id (user) or chat_id (group)
#   app_id           - Feishu app ID
#   app_secret       - Feishu app secret
#   receive_id_type  - "open_id" (default) or "chat_id"

set -euo pipefail

IMAGE_PATH="${1:?Usage: feishu_send_image.sh <image_path> <receive_id> <app_id> <app_secret> [receive_id_type]}"
RECEIVE_ID="${2:?Missing receive_id}"
APP_ID="${3:?Missing app_id}"
APP_SECRET="${4:?Missing app_secret}"
RECEIVE_ID_TYPE="${5:-open_id}"

# Step 1: Get tenant_access_token
TOKEN_RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

TOKEN=$(echo "$TOKEN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])" 2>/dev/null)
if [ -z "$TOKEN" ]; then
  echo "ERROR: Failed to get access token" >&2
  echo "$TOKEN_RESP" >&2
  exit 1
fi

# Step 2: Upload image to get image_key
UPLOAD_RESP=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/images' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'image_type=message' \
  -F "image=@$IMAGE_PATH")

IMAGE_KEY=$(echo "$UPLOAD_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['image_key'])" 2>/dev/null)
if [ -z "$IMAGE_KEY" ]; then
  echo "ERROR: Failed to upload image" >&2
  echo "$UPLOAD_RESP" >&2
  exit 1
fi

# Step 3: Send image message
SEND_RESP=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}")

CODE=$(echo "$SEND_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',1))" 2>/dev/null)
if [ "$CODE" = "0" ]; then
  MSG_ID=$(echo "$SEND_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['message_id'])" 2>/dev/null)
  echo "OK: image_key=$IMAGE_KEY message_id=$MSG_ID"
else
  echo "ERROR: Failed to send message" >&2
  echo "$SEND_RESP" >&2
  exit 1
fi
