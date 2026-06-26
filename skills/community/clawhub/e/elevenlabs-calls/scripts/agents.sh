#!/usr/bin/env bash
# List ElevenLabs Conversational AI agents
set -euo pipefail

API_KEY="${ELEVENLABS_API_KEY:-}"
SEARCH=""

usage() {
  echo "Usage: $(basename "$0") [--search \"name\"]"
  echo "  --search, -s    Search agents by name"
  echo ""
  echo "Environment: ELEVENLABS_API_KEY (required)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --search|-s) SEARCH="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo "Error: ELEVENLABS_API_KEY not set" >&2
  exit 1
fi

URL="https://api.elevenlabs.io/v1/convai/agents?page_size=50"
[[ -n "$SEARCH" ]] && URL="${URL}&search=${SEARCH}"

response=$(curl -s -X GET "$URL" \
  -H "xi-api-key: $API_KEY" \
  -H "Content-Type: application/json")

# Check for errors
if echo "$response" | jq -e '.detail' >/dev/null 2>&1; then
  echo "Error: $(echo "$response" | jq -r '.detail')" >&2
  exit 1
fi

# Pretty print agents
echo "$response" | jq -r '
  .agents[] |
  "ID: \(.agent_id)\nName: \(.name)\nCreated: \(.created_at_unix | todate)\n---"
'

# Also output raw JSON for scripting
if [[ -t 1 ]]; then
  : # interactive, already printed above
else
  echo "$response"
fi
