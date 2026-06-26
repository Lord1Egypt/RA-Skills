#!/bin/bash
# Get aggregate and breakdown metrics from AIOZ API
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./analytic_data.sh TYPE FROM TO
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

# Prepare payload
PAYLOAD='{
  "from": '"$FROM_UNIX"',
  "to": '"$TO_UNIX"',
  "filter_by": {
    "media_type": "'"$TYPE"'"
  }
}'

echo "==========================="
echo "    AGGREGATE METRICS      "
echo "==========================="

# Watch time sum
WATCH_TIME_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/data/watch_time/sum" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

# View count
VIEW_COUNT_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/data/view/count" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

WATCH_TIME_SUM=$(echo "$WATCH_TIME_RESPONSE" | jq -r '.data.data // empty')
VIEW_COUNT=$(echo "$VIEW_COUNT_RESPONSE" | jq -r '.data.data // empty')

if [ -z "$WATCH_TIME_SUM" ]; then
  echo "Error: Could not extract watch_time data"
else
  echo "Watch Time Sum Data: $WATCH_TIME_SUM"
fi

if [ -z "$VIEW_COUNT" ]; then
  echo "Error: Could not extract view_count data"
else
  echo "View Count Data: $VIEW_COUNT"
fi

echo ""
echo "==========================="
echo "    BREAKDOWN METRICS      "
echo "==========================="

# Device type
DEVICE_TYPE_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/device-type" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

# Operating system
OPERATING_SYSTEM_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/operator-system" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

# Country
COUNTRY_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/country" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

# Browser
BROWSER_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/browser" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$PAYLOAD")

DEVICE_TYPE_RESULT=$(echo "$DEVICE_TYPE_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')
OPERATING_SYSTEM_RESULT=$(echo "$OPERATING_SYSTEM_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')
COUNTRY_RESULT=$(echo "$COUNTRY_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')
BROWSER_RESULT=$(echo "$BROWSER_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')

echo "--- View By Device type ---"
echo "$DEVICE_TYPE_RESULT" | jq '.'
echo ""

echo "--- View By Operating system ---"
echo "$OPERATING_SYSTEM_RESULT" | jq '.'
echo ""

echo "--- View By Country ---"
echo "$COUNTRY_RESULT" | jq '.'
echo ""

echo "--- View By Browser ---"
echo "$BROWSER_RESULT" | jq '.'

echo ""
echo "Summary: action=analytic_data, type=$TYPE, from=$FROM, to=$TO"
