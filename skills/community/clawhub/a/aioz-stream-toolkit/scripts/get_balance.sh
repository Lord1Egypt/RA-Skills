#!/bin/bash
# Get user balance/info from AIOZ API
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_balance.sh

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ]; then
    echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0"
    exit 1
fi

# Send request to get user info / balance
RESPONSE=$(curl -s -X GET "https://api.aiozstream.network/api/user/me" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
