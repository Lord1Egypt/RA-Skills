#!/bin/bash
# Send image to Feishu chat in one command
# Usage: send_image.sh -r <receive_id> -i <image_path_or_url> [-t <text>]

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source config
source "${SCRIPT_DIR}/config.sh"

# Show usage
usage() {
  echo "Usage: $0 -r <receive_id> -i <image_path_or_url> [-t <text>]"
  echo ""
  echo "Options:"
  echo "  -r    Receiver ID (open_id, user_id, or chat_id)"
  echo "  -i    Image path (local file) or URL (remote image)"
  echo "  -t    Optional text to accompany the image"
  echo ""
  echo "Examples:"
  echo "  $0 -r \"ou_xxx\" -i \"/path/to/image.jpg\""
  echo "  $0 -r \"oc_xxx\" -i \"https://example.com/image.png\" -t \"Check this out!\""
  exit 1
}

# Parse arguments
RECEIVE_ID=""
IMAGE_INPUT=""
TEXT=""

while getopts "r:i:t:h" opt; do
  case $opt in
    r) RECEIVE_ID="$OPTARG" ;;
    i) IMAGE_INPUT="$OPTARG" ;;
    t) TEXT="$OPTARG" ;;
    h) usage ;;
    *) usage ;;
  esac
done

# Validate required arguments
if [[ -z "$RECEIVE_ID" || -z "$IMAGE_INPUT" ]]; then
  echo "Error: Missing required arguments" >&2
  usage
fi

# Step 1: Get access token
echo "Step 1: Getting access token..." >&2
TOKEN=$("${SCRIPT_DIR}/get_token.sh")
echo "Token obtained successfully" >&2

# Step 2: Prepare image file
if [[ "$IMAGE_INPUT" =~ ^https?:// ]]; then
  # Download remote image
  echo "Step 2: Downloading remote image..." >&2
  TEMP_FILE=$(mktemp /tmp/feishu_image.XXXXXX)
  curl -s -o "$TEMP_FILE" "$IMAGE_INPUT"
  if [[ ! -s "$TEMP_FILE" ]]; then
    echo "Error: Failed to download image from URL" >&2
    rm -f "$TEMP_FILE"
    exit 1
  fi
  IMAGE_FILE="$TEMP_FILE"
  echo "Image downloaded to: $IMAGE_FILE" >&2
else
  # Use local file
  IMAGE_FILE="$IMAGE_INPUT"
  if [[ ! -f "$IMAGE_FILE" ]]; then
    echo "Error: Image file not found: $IMAGE_FILE" >&2
    exit 1
  fi
  echo "Step 2: Using local image file" >&2
fi

# Step 3: Upload image
echo "Step 3: Uploading image to Feishu..." >&2
IMAGE_KEY=$("${SCRIPT_DIR}/upload_image.sh" -f "$IMAGE_FILE" -t "$TOKEN")
echo "Image uploaded, key: $IMAGE_KEY" >&2

# Cleanup temp file if we downloaded one
if [[ -n "${TEMP_FILE:-}" && -f "$TEMP_FILE" ]]; then
  rm -f "$TEMP_FILE"
fi

# Step 4: Send message
echo "Step 4: Sending message..." >&2
MESSAGE_ID=$("${SCRIPT_DIR}/send_message.sh" -r "$RECEIVE_ID" -k "$IMAGE_KEY" -t "$TEXT" -a "$TOKEN")

echo ""
echo "✅ Image sent successfully!"
echo "Message ID: $MESSAGE_ID"
