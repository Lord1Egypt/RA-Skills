#!/bin/bash
# Get video URL by name via POST /media with only PUBLIC_KEY, SECRET_KEY and video name in body
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_video_url_by_name.sh VIDEO_NAME

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"
VIDEO_NAME="$1"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$VIDEO_NAME" ]; then
    echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0 VIDEO_NAME"
    exit 1
fi

curl -s -X POST 'https://api.aiozstream.network/api/media' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "{\"search\": \"$VIDEO_NAME\"}"