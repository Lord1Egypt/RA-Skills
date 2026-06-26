#!/bin/bash
# Delete an AIOZ Pin API key
# Usage: ./delete_api_key.sh JWT_TOKEN KEY_ID

JWT_TOKEN="$1"
KEY_ID="$2"

if [ -z "$JWT_TOKEN" ] || [ -z "$KEY_ID" ]; then
    echo "Usage: $0 JWT_TOKEN KEY_ID"
    exit 1
fi

# Send request to delete API key
RESPONSE=$(curl -s -X DELETE "https://api.aiozpin.network/api/apikeys/$KEY_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
