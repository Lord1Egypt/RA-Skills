#!/bin/bash
# Get aggregate metrics from AIOZ API
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_aggregate_metric.sh TYPE FROM TO
# FROM and TO in dd/mm/yyyy

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"
TYPE="$1"
FROM="$2"
TO="$3"

# Check required arguments
if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$TYPE" ] || [ -z "$FROM" ] || [ -z "$TO" ]; then
    echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0 TYPE(from 'video' or 'audio') FROM(dd/mm/yyyy) TO(dd/mm/yyyy)"
    exit 1
fi

# Validate TYPE
if [ "$TYPE" != "video" ] && [ "$TYPE" != "audio" ]; then
    echo "Error: TYPE must be 'video' or 'audio'"
    exit 1
fi

# Convert dd/mm/yyyy to Unix timestamp
FROM_UNIX=$(date -d "$(echo $FROM | awk -F/ '{print $2"/"$1"/"$3}')" +%s 2>/dev/null)
TO_UNIX=$(date -d "$(echo $TO | awk -F/ '{print $2"/"$1"/"$3}')" +%s 2>/dev/null)

if [ -z "$FROM_UNIX" ] || [ -z "$TO_UNIX" ]; then
    echo "Error: Invalid FROM or TO date format. Use dd/mm/yyyy"
    exit 1
fi

# Send request to get watch time sum metric
WATCH_TIME_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/data/watch_time/sum" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "from": '"$FROM_UNIX"',
    "to": '"$TO_UNIX"',
    "filter_by": {
      "media_type": "'"$TYPE"'"
    }
  }')

# Send request to get view count metric
VIEW_COUNT_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/data/view/count" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "from": '"$FROM_UNIX"',
    "to": '"$TO_UNIX"',
    "filter_by": {
      "media_type": "'"$TYPE"'"
    }
  }')

WATCH_TIME_SUM=$(echo "$WATCH_TIME_RESPONSE" | jq -r '.data.data // empty')
VIEW_COUNT=$(echo "$VIEW_COUNT_RESPONSE" | jq -r '.data.data // empty')

if [ -z "$WATCH_TIME_SUM" ]; then
  echo "Watch Time response:"
  echo "$WATCH_TIME_RESPONSE"
  echo "Error: Could not extract watch_time data"
  exit 1
fi

if [ -z "$VIEW_COUNT" ]; then
  echo "View Count response:"
  echo "$VIEW_COUNT_RESPONSE"
  echo "Error: Could not extract view_count data"
  exit 1
fi

echo "Watch Time Sum Data: $WATCH_TIME_SUM"
echo "View Count Data: $VIEW_COUNT"
echo "Summary: type=$TYPE, from=$FROM, to=$TO"