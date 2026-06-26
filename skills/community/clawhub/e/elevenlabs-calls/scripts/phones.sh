#!/usr/bin/env bash
# List ElevenLabs phone numbers (imported from Twilio)
set -euo pipefail

API_KEY="${ELEVENLABS_API_KEY:-}"

if [[ -z "$API_KEY" ]]; then
  echo "Error: ELEVENLABS_API_KEY not set" >&2
  exit 1
fi

response=$(curl -s -X GET "https://api.elevenlabs.io/v1/convai/phone-numbers" \
  -H "xi-api-key: $API_KEY" \
  -H "Content-Type: application/json")

# Check for errors
if echo "$response" | jq -e '.detail' >/dev/null 2>&1; then
  echo "Error: $(echo "$response" | jq -r '.detail')" >&2
  exit 1
fi

# Check if empty
if [[ "$(echo "$response" | jq 'length')" == "0" ]]; then
  echo "No phone numbers found."
  echo ""
  echo "To add a phone number:"
  echo "1. Go to https://elevenlabs.io/app/agents/phone-numbers"
  echo "2. Click 'Import Phone Number'"
  echo "3. Enter your Twilio Account SID, Auth Token, and phone number"
  exit 0
fi

# Pretty print phone numbers
echo "$response" | jq -r '
  .[] |
  "ID: \(.phone_number_id)
Phone: \(.phone_number)
Label: \(.label // "N/A")
Provider: \(.provider)
Inbound: \(.inbound_enabled // false)
Outbound: \(.outbound_enabled // true)
---"
'
