#!/bin/bash
# Get usage data from AIOZ API
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_usage_data.sh FROM TO

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"
FROM="$1"
TO="$2"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$FROM" ] || [ -z "$TO" ]; then
    echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0 FROM(dd/mm/yyyy) TO(dd/mm/yyyy)"
    echo "  FROM, TO: Timestamps or date formats valid for the API"
  
    exit 1
fi

FROM_UNIX=$(date -d "$(echo $FROM | awk -F/ '{print $2"/"$1"/"$3}')" +%s 2>/dev/null)
TO_UNIX=$(date -d "$(echo $TO | awk -F/ '{print $2"/"$1"/"$3}')" +%s 2>/dev/null)

if [ -z "$FROM_UNIX" ] || [ -z "$TO_UNIX" ]; then
    echo "Error: Invalid FROM or TO date format. Use dd/mm/yyyy"
    exit 1
fi

# Build URL with required query parameters
URL="https://api.aiozstream.network/api/analytics/data?from=$FROM_UNIX&to=$TO_UNIX&interval=hour"

# Send request to get usage data
RESPONSE=$(curl -s -X GET "$URL" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
