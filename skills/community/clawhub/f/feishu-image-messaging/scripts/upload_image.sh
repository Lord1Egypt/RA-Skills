#!/bin/bash
# Upload image to Feishu and get image_key

set -e

# Source configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

# Parse arguments
IMAGE_FILE=""
TOKEN=""

while getopts "f:t:" opt; do
  case $opt in
    f) IMAGE_FILE="$OPTARG" ;;
    t) TOKEN="$OPTARG" ;;
    *) echo "Usage: $0 -f <image_file> -t <token>" >&2; exit 1 ;;
  esac
done

if [[ -z "$IMAGE_FILE" || -z "$TOKEN" ]]; then
  echo "Usage: $0 -f <image_file> -t <token>" >&2
  exit 1
fi

# Check if file exists
if [[ ! -f "$IMAGE_FILE" ]]; then
  echo "Error: File not found: $IMAGE_FILE" >&2
  exit 1
fi

# Upload image
response=$(curl -s -X POST "${FEISHU_IMAGE_UPLOAD_ENDPOINT}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "image=@${IMAGE_FILE}" \
  -F "image_type=message")

# Check for errors
if [ "$(echo "$response" | jq -r '.code')" != "0" ]; then
  echo "Error uploading image: $(echo "$response" | jq -r '.msg')" >&2
  exit 1
fi

# Return image_key
echo "$response" | jq -r '.data.image_key'
