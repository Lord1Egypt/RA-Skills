#!/bin/bash
# Create livestream key with default configuration
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./create_livestream_key.sh KEY_NAME

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"
KEY_NAME="$1"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$KEY_NAME" ]; then
    echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0 KEY_NAME"
    exit 1
fi

curl -s -X POST 'https://api.aiozstream.network/api/live_streams' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "save": true,
    "type": "video",
    "name": "'"$KEY_NAME"'"
  }'