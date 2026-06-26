#!/bin/bash
# Get media list via GET /media with optional search and page filters
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_media_list.sh [SEARCH] [PAGE]

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"
SEARCH="$1"
PAGE="$2"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ]; then
  echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0 [SEARCH] [PAGE]"
    exit 1
fi

if [ -n "$PAGE" ] && ! [[ "$PAGE" =~ ^[0-9]+$ ]]; then
  echo "Error: PAGE must be a non-negative integer"
  exit 1
fi

QUERY=""

if [ -n "$SEARCH" ]; then
  ENCODED_SEARCH="${SEARCH// /%20}"
  QUERY="?search=$ENCODED_SEARCH"
fi

if [ -n "$PAGE" ]; then
  if [ -n "$QUERY" ]; then
    QUERY="$QUERY&page=$PAGE"
  else
    QUERY="?page=$PAGE"
  fi
fi

curl -s -X GET "https://api.aiozstream.network/api/media$QUERY" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY"