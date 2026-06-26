#!/bin/bash
# Get media list via POST /media with only PUBLIC_KEY and SECRET_KEY
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_video_list.sh

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] ; then
  echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0"
    exit 1
fi

curl -s -X POST 'https://api.aiozstream.network/api/media' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "{}"