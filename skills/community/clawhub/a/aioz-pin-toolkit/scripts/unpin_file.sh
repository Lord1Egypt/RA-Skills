#!/bin/bash
# Remove pinned file by pin ID
# Usage: ./unpin_file.sh PIN_ID PINNING_API_KEY PINNING_SECRET_KEY

PIN_ID="$1"
PINNING_API_KEY="$2"
PINNING_SECRET_KEY="$3"

if [ -z "$PIN_ID" ] || [ -z "$PINNING_API_KEY" ] || [ -z "$PINNING_SECRET_KEY" ]; then
    echo "Usage: $0 PIN_ID PINNING_API_KEY PINNING_SECRET_KEY"
    exit 1
fi

REQUEST_URL="https://api.aiozpin.network/api/pinning/unpin/$PIN_ID"

# Print request URL before calling API
echo "Request URL: $REQUEST_URL"

# Send request to unpin file
RESPONSE=$(curl -s --location --request DELETE "$REQUEST_URL" \
  -H "pinning_api_key: $PINNING_API_KEY" \
  -H "pinning_secret_key: $PINNING_SECRET_KEY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
