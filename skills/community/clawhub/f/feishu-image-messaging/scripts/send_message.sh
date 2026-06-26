#!/bin/bash
# Send image message via Feishu

set -e

# Source configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

# Parse arguments
RECEIVE_ID=""
IMAGE_KEY=""
TEXT=""
TOKEN=""

while getopts "r:k:t:a:" opt; do
  case $opt in
    r) RECEIVE_ID="$OPTARG" ;;
    k) IMAGE_KEY="$OPTARG" ;;
    t) TEXT="$OPTARG" ;;
    a) TOKEN="$OPTARG" ;;
    *) echo "Usage: $0 -r <receive_id> -k <image_key> [-t <text>] -a <token>" >&2; exit 1 ;;
  esac
done

if [[ -z "$RECEIVE_ID" || -z "$IMAGE_KEY" || -z "$TOKEN" ]]; then
  echo "Usage: $0 -r <receive_id> -k <image_key> [-t <text>] -a <token>" >&2
  exit 1
fi

# Build message content (as JSON object)
if [[ -n "$TEXT" ]]; then
  # Message with text and image
  content_obj=$(jq -n \
    --arg text "$TEXT" \
    --arg image_key "$IMAGE_KEY" \
    '{
      "zh_cn": {
        "title": "图片消息",
        "content": [
          [{"tag": "text", "text": $text}],
          [{"tag": "img", "image_key": $image_key}]
        ]
      }
    }')
else
  # Image only
  content_obj=$(jq -n \
    --arg image_key "$IMAGE_KEY" \
    '{
      "zh_cn": {
        "title": "图片",
        "content": [
          [{"tag": "img", "image_key": $image_key}]
        ]
      }
    }')
fi

# Convert content object to JSON string for the API
content_str=$(echo "$content_obj" | jq -c '.')

# Build full request body
request_body=$(jq -n \
  --arg receive_id "$RECEIVE_ID" \
  --arg content "$content_str" \
  '{
    "receive_id": $receive_id,
    "msg_type": "post",
    "content": $content
  }')

# Send message
response=$(curl -s -X POST "${FEISHU_MESSAGE_ENDPOINT}?receive_id_type=open_id" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$request_body")

# Check for errors
if [ "$(echo "$response" | jq -r '.code')" != "0" ]; then
  echo "Error sending message: $(echo "$response" | jq -r '.msg')" >&2
  exit 1
fi

# Return message_id
echo "$response" | jq -r '.data.message_id'
