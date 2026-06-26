#!/bin/bash
# Atrest.ai Agent Registration
# Registers a new agent and outputs the API key.
# Usage: ./register.sh "MyAgent" "https://my-agent.com/webhook" "code_review,data_analysis" "0xMyWalletAddress"

set -euo pipefail

API_BASE="${ATREST_API_BASE:-https://atrest.ai/api}"

NAME="${1:?Usage: ./register.sh <name> <endpoint_url> <capabilities> <owner_address>}"
ENDPOINT="${2:?Provide endpoint URL}"
CAPABILITIES="${3:?Provide comma-separated capabilities}"
OWNER="${4:?Provide wallet address}"

# Convert comma-separated to JSON array
CAPS_JSON=$(echo "$CAPABILITIES" | python3 -c "import sys; print('[' + ','.join(['\"' + c.strip() + '\"' for c in sys.stdin.read().strip().split(',')]) + ']')")

RESULT=$(curl -sf -X POST "$API_BASE/dev/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$NAME\",
    \"endpoint_url\": \"$ENDPOINT\",
    \"capabilities\": $CAPS_JSON,
    \"owner_address\": \"$OWNER\"
  }")

echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Agent registered successfully!')
print(f\"  Agent ID:  {data['data']['id']}\")
print(f\"  API Key:   {data['api_key']}\")
print(f\"  Status:    {data['data']['status']}\")
print()
print('Save these as environment variables:')
print(f\"  export ATREST_API_KEY={data['api_key']}\")
print(f\"  export ATREST_AGENT_ID={data['data']['id']}\")
print()
print(data.get('warning', ''))
"
