#!/bin/bash
# List pins with pagination and sorting options
# Usage: ./list_pins.sh PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT] [PINNED] [SORT_BY] [SORT_ORDER]

PINNING_API_KEY="$1"
PINNING_SECRET_KEY="$2"
OFFSET="${3:-0}"
LIMIT="${4:-10}"
PINNED="${5:-true}"
SORT_BY="${6:-name}"
SORT_ORDER="${7:-ASC}"

if [ -z "$PINNING_API_KEY" ] || [ -z "$PINNING_SECRET_KEY" ]; then
    echo "Usage: $0 PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT] [PINNED] [SORT_BY] [SORT_ORDER]"
    exit 1
fi

# Build query string
QUERY_STRING="offset=$OFFSET&limit=$LIMIT&pinned=$PINNED&sortBy=$SORT_BY&sortOrder=$SORT_ORDER"
REQUEST_URL="https://api.aiozpin.network/api/pinning/pins/?$QUERY_STRING"

# Print request URL before calling API
echo "Request URL: $REQUEST_URL"

# Send request to list pins
RESPONSE=$(curl -s --location --request GET "$REQUEST_URL" \
  -H "pinning_api_key: $PINNING_API_KEY" \
  -H "pinning_secret_key: $PINNING_SECRET_KEY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
