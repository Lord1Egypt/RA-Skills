#!/bin/bash
# Pin a local file to IPFS
# Usage: ./pin_files_or_directory.sh FILE_PATH PINNING_API_KEY PINNING_SECRET_KEY

FILE_PATH="$1"
PINNING_API_KEY="$2"
PINNING_SECRET_KEY="$3"

if [ -z "$FILE_PATH" ] || [ -z "$PINNING_API_KEY" ] || [ -z "$PINNING_SECRET_KEY" ]; then
    echo "Usage: $0 FILE_PATH PINNING_API_KEY PINNING_SECRET_KEY"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "Error: file not found: $FILE_PATH"
    exit 1
fi

REQUEST_URL="https://api.aiozpin.network/api/pinning/"

# Print request URL before calling API
echo "Request URL: $REQUEST_URL"

# Send request to pin file
RESPONSE=$(curl -s --location --request POST "$REQUEST_URL" \
  -H "pinning_api_key: $PINNING_API_KEY" \
  -H "pinning_secret_key: $PINNING_SECRET_KEY" \
  --form "file=@$FILE_PATH")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
