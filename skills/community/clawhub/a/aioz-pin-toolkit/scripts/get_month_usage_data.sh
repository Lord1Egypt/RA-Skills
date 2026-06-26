#!/bin/bash
# Get monthly usage data
# Usage: ./get_month_usage_data.sh PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT]

PINNING_API_KEY="$1"
PINNING_SECRET_KEY="$2"
OFFSET="${3:-0}"
LIMIT="${4:-10}"

if [ -z "$PINNING_API_KEY" ] || [ -z "$PINNING_SECRET_KEY" ]; then
    echo "Usage: $0 PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT]"
    exit 1
fi

# Build query string
QUERY_STRING="offset=$OFFSET&limit=$LIMIT"
REQUEST_URL="https://api.aiozpin.network/api/billing/thisMonthUsage/?$QUERY_STRING"

# Print request URL before calling API
echo "Request URL: $REQUEST_URL"

# Send request to get monthly usage data
RESPONSE=$(curl -s --location --request GET "$REQUEST_URL" \
  -H "pinning_api_key: $PINNING_API_KEY" \
  -H "pinning_secret_key: $PINNING_SECRET_KEY" \
  -H "Content-Type: application/json")

echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
