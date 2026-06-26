#!/bin/bash
# Pin content by CID hash
# Usage: ./pin_by_cid.sh CID_HASH PINNING_API_KEY PINNING_SECRET_KEY [METADATA_NAME]

CID_HASH="$1"
PINNING_API_KEY="$2"
PINNING_SECRET_KEY="$3"
METADATA_NAME="$4"

if [ -z "$CID_HASH" ] || [ -z "$PINNING_API_KEY" ] || [ -z "$PINNING_SECRET_KEY" ]; then
    echo "Usage: $0 CID_HASH PINNING_API_KEY PINNING_SECRET_KEY [METADATA_NAME]"
    exit 1
fi

# Build request body
if [ -n "$METADATA_NAME" ]; then
    REQUEST_BODY=$(cat <<EOF
{
  "hash_to_pin": "$CID_HASH",
  "metadata": {
    "name": "$METADATA_NAME"
  }
}
EOF
)
else
    REQUEST_BODY=$(cat <<EOF
{
  "hash_to_pin": "$CID_HASH"
}
EOF
)
fi

REQUEST_URL="https://api.aiozpin.network/api/pinning/pinByHash"

# Print request URL before calling API
echo "Request URL: $REQUEST_URL"

# Send request to pin by CID
RESPONSE=$(curl -s --location --request POST "$REQUEST_URL" \
  -H "pinning_api_key: $PINNING_API_KEY" \
  -H "pinning_secret_key: $PINNING_SECRET_KEY" \
  -H "Content-Type: application/json" \
  --data-raw "$REQUEST_BODY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
