#!/bin/bash
# Get list of all AIOZ Pin API keys
# Usage: ./get_list_api_keys.sh JWT_TOKEN

JWT_TOKEN="$1"

if [ -z "$JWT_TOKEN" ]; then
    echo "Usage: $0 JWT_TOKEN"
    exit 1
fi

# Send request to get list of API keys
RESPONSE=$(curl -s -X GET "https://api.aiozpin.network/api/apiKeys/list" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
