#!/usr/bin/env bash
# Get conversation details from ElevenLabs
set -euo pipefail

API_KEY="${ELEVENLABS_API_KEY:-}"
CONV_ID=""
TRANSCRIPT_ONLY=false
AUDIO_ONLY=false

usage() {
  echo "Usage: $(basename "$0") <conversation_id> [--transcript] [--audio]"
  echo ""
  echo "Options:"
  echo "  --transcript, -t   Output only the transcript"
  echo "  --audio, -a        Download the audio recording (outputs to stdout)"
  echo ""
  echo "Environment: ELEVENLABS_API_KEY (required)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --transcript|-t) TRANSCRIPT_ONLY=true; shift ;;
    --audio|-a) AUDIO_ONLY=true; shift ;;
    --help|-h) usage ;;
    -*) echo "Unknown option: $1"; usage ;;
    *) 
      if [[ -z "$CONV_ID" ]]; then
        CONV_ID="$1"
      fi
      shift 
      ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo "Error: ELEVENLABS_API_KEY not set" >&2
  exit 1
fi

if [[ -z "$CONV_ID" ]]; then
  echo "Error: conversation_id is required" >&2
  usage
fi

# Get audio
if [[ "$AUDIO_ONLY" == "true" ]]; then
  curl -s -X GET "https://api.elevenlabs.io/v1/convai/conversations/${CONV_ID}/audio" \
    -H "xi-api-key: $API_KEY"
  exit 0
fi

# Get conversation details
response=$(curl -s -X GET "https://api.elevenlabs.io/v1/convai/conversations/${CONV_ID}" \
  -H "xi-api-key: $API_KEY" \
  -H "Content-Type: application/json")

# Check for errors
if echo "$response" | jq -e '.detail' >/dev/null 2>&1; then
  echo "Error: $(echo "$response" | jq -r '.detail')" >&2
  exit 1
fi

# Transcript only
if [[ "$TRANSCRIPT_ONLY" == "true" ]]; then
  echo "$response" | jq -r '
    .transcript[]? |
    "\(.role): \(.message)"
  '
  exit 0
fi

# Full details
status=$(echo "$response" | jq -r '.status // "unknown"')
agent_id=$(echo "$response" | jq -r '.agent_id // "N/A"')
start_time=$(echo "$response" | jq -r '.start_time_unix_secs // 0 | todate')
duration=$(echo "$response" | jq -r '.call_duration_secs // 0')

echo "Conversation: $CONV_ID"
echo "Status: $status"
echo "Agent: $agent_id"
echo "Started: $start_time"
echo "Duration: ${duration}s"
echo ""
echo "=== Transcript ==="
echo "$response" | jq -r '
  .transcript[]? |
  "\(.role | ascii_upcase): \(.message)"
'

# Show analysis if available
analysis=$(echo "$response" | jq -r '.analysis // empty')
if [[ -n "$analysis" && "$analysis" != "null" ]]; then
  echo ""
  echo "=== Analysis ==="
  echo "$response" | jq -r '.analysis'
fi
