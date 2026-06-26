#!/bin/bash
# Get breakdown metrics from AIOZ API
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./get_breakdown_metric.sh TYPE FROM TO
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

# {"status":"success","data":{"context":{"metric":"view","time_frame":{"from":"2024-12-31T17:00:00Z","to":"2026-03-24T17:00:00Z"},"breakdown":"device_type","filter":{"media_type":"video"}},"total":2,"data":[{"metric_value":229,"dimension_value":"computer","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":41,"dimension_value":"phone","emitted_at":"0001-01-01T00:00:00Z"}]}}{"status":"success","data":{"context":{"metric":"view","time_frame":{"from":"2024-12-31T17:00:00Z","to":"2026-03-24T17:00:00Z"},"breakdown":"device_type","filter":{"media_type":"video"}},"total":2,"data":[{"metric_value":229,"dimension_value":"computer","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":41,"dimension_value":"phone","emitted_at":"0001-01-01T00:00:00Z"}]}}
# Send request to get device type breakdown
DEVICE_TYPE_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/device-type" \
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

# {"status":"success","data":{"context":{"metric":"view","time_frame":{"from":"2024-12-31T17:00:00Z","to":"2026-03-24T17:00:00Z"},"breakdown":"operator_system","filter":{"media_type":"video"}},"total":6,"data":[{"metric_value":111,"dimension_value":"windows","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":98,"dimension_value":"linux","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":23,"dimension_value":"android","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":19,"dimension_value":"macintosh","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":18,"dimension_value":"ios","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"emitted_at":"0001-01-01T00:00:00Z"}]}}
# Send request to get operating system breakdown
OPERATING_SYSTEM_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/operator-system" \
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

# {"status":"success","data":{"context":{"metric":"view","time_frame":{"from":"2024-12-31T17:00:00Z","to":"2026-03-24T17:00:00Z"},"breakdown":"country","filter":{"media_type":"video"}},"total":30,"data":[{"metric_value":195,"dimension_value":"VN","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":16,"dimension_value":"US","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":5,"dimension_value":"GB","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":5,"dimension_value":"HK","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":4,"dimension_value":"DE","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":4,"dimension_value":"IT","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":4,"dimension_value":"FR","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":3,"dimension_value":"NL","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":3,"dimension_value":"TH","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":3,"dimension_value":"ES","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"JP","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"BR","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"ID","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"IN","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"LU","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"PK","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"SG","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":2,"dimension_value":"UG","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"MX","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"NG","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"GR","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"CN","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"PL","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"PT","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"CO","emitted_at":"0001-01-01T00:00:00Z"}]}}
# Send request to get country breakdown
COUNTRY_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/country" \
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


# {"status":"success","data":{"context":{"metric":"view","time_frame":{"from":"2024-12-31T17:00:00Z","to":"2026-03-24T17:00:00Z"},"breakdown":"browser","filter":{"media_type":"video"}},"total":6,"data":[{"metric_value":237,"dimension_value":"chrome","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":19,"dimension_value":"safari","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":6,"dimension_value":"firefox","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":4,"dimension_value":"edg","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":3,"dimension_value":"unknown","emitted_at":"0001-01-01T00:00:00Z"},{"metric_value":1,"dimension_value":"opr","emitted_at":"0001-01-01T00:00:00Z"}]}}
# Send request to get browser breakdown
BROWSER_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/analytics/metrics/bucket/view/browser" \
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

DEVICE_TYPE_RESULT=$(echo "$DEVICE_TYPE_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')
OPERATING_SYSTEM_RESULT=$(echo "$OPERATING_SYSTEM_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')
COUNTRY_RESULT=$(echo "$COUNTRY_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')
BROWSER_RESULT=$(echo "$BROWSER_RESPONSE" | jq -c '{total: (.data.total // 0), data: (.data.data // [])}')

if [ -z "$DEVICE_TYPE_RESULT" ] || [ -z "$OPERATING_SYSTEM_RESULT" ] || [ -z "$COUNTRY_RESULT" ] || [ -z "$BROWSER_RESULT" ]; then
  echo "Error: Could not extract one or more total/data results"
  exit 1
fi

echo "=== View By Device type ==="
echo "$DEVICE_TYPE_RESULT" | jq '.'
echo ""

echo "=== View By Operating system ==="
echo "$OPERATING_SYSTEM_RESULT" | jq '.'
echo ""

echo "=== View By Country ==="
echo "$COUNTRY_RESULT" | jq '.'
echo ""

echo "=== View By Browser ==="
echo "$BROWSER_RESULT" | jq '.'