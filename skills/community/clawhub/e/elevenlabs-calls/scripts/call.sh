#!/usr/bin/env bash
# Make an outbound phone call using ElevenLabs Conversational AI
set -euo pipefail

API_KEY="${ELEVENLABS_API_KEY:-}"
AGENT_ID=""
PHONE_ID=""
TO_NUMBER=""
DYNAMIC_VARS=""

usage() {
  echo "Usage: $(basename "$0") --agent <id> --phone <id> --to <number> [--vars '{...}']"
  echo ""
  echo "Options:"
  echo "  --agent, -a     Agent ID (required)"
  echo "  --phone, -p     Phone number ID from ElevenLabs (required)"
  echo "  --to, -t        Phone number to call, E.164 format e.g. +15551234567 (required)"
  echo "  --vars, -v      JSON object of dynamic variables for the agent (optional)"
  echo ""
  echo "Environment: ELEVENLABS_API_KEY (required)"
  echo ""
  echo "Example:"
  echo "  $(basename "$0") -a agent_abc123 -p phone_xyz -t '+15121234567' \\"
  echo "    --vars '{\"customer_name\":\"Nat\",\"purpose\":\"schedule inspection\"}'"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent|-a) AGENT_ID="$2"; shift 2 ;;
    --phone|-p) PHONE_ID="$2"; shift 2 ;;
    --to|-t) TO_NUMBER="$2"; shift 2 ;;
    --vars|-v) DYNAMIC_VARS="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo "Error: ELEVENLABS_API_KEY not set" >&2
  exit 1
fi

if [[ -z "$AGENT_ID" || -z "$PHONE_ID" || -z "$TO_NUMBER" ]]; then
  echo "Error: --agent, --phone, and --to are required" >&2
  usage
fi

# Build request body
if [[ -n "$DYNAMIC_VARS" ]]; then
  BODY=$(jq -n \
    --arg agent_id "$AGENT_ID" \
    --arg phone_id "$PHONE_ID" \
    --arg to "$TO_NUMBER" \
    --argjson vars "$DYNAMIC_VARS" \
    '{
      agent_id: $agent_id,
      agent_phone_number_id: $phone_id,
      to_number: $to,
      conversation_initiation_client_data: {
        dynamic_variables: $vars
      }
    }')
else
  BODY=$(jq -n \
    --arg agent_id "$AGENT_ID" \
    --arg phone_id "$PHONE_ID" \
    --arg to "$TO_NUMBER" \
    '{
      agent_id: $agent_id,
      agent_phone_number_id: $phone_id,
      to_number: $to
    }')
fi

echo "Initiating call to $TO_NUMBER..."

response=$(curl -s -X POST "https://api.elevenlabs.io/v1/convai/twilio/outbound-call" \
  -H "xi-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BODY")

# Check response
success=$(echo "$response" | jq -r '.success // false')
message=$(echo "$response" | jq -r '.message // "Unknown error"')
conv_id=$(echo "$response" | jq -r '.conversation_id // "N/A"')
call_sid=$(echo "$response" | jq -r '.callSid // "N/A"')

if [[ "$success" == "true" ]]; then
  echo "✓ Call initiated successfully!"
  echo ""
  echo "Conversation ID: $conv_id"
  echo "Twilio Call SID: $call_sid"
  echo ""
  echo "To check the conversation later:"
  echo "  $(dirname "$0")/conversation.sh $conv_id"
else
  echo "✗ Call failed: $message" >&2
  echo "$response" | jq . >&2
  exit 1
fi
