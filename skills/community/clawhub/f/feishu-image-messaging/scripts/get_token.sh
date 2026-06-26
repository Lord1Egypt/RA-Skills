#!/bin/bash
# Get Feishu tenant access token

set -e

# Source configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/config.sh"

# Get token from Feishu API
response=$(curl -s -X POST "${FEISHU_AUTH_ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"${FEISHU_APP_ID}\",
    \"app_secret\": \"${FEISHU_APP_SECRET}\"
  }")

# Check for errors
if [ "$(echo "$response" | jq -r '.code')" != "0" ]; then
  echo "Error getting token: $(echo "$response" | jq -r '.msg')" >&2
  exit 1
fi

# Extract and return token
echo "$response" | jq -r '.tenant_access_token'
