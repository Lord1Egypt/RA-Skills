#!/usr/bin/env bash
# List recent conversations from ElevenLabs
set -euo pipefail

API_KEY="${ELEVENLABS_API_KEY:-}"
AGENT_ID=""
LIMIT=10

usage() {
  echo "Usage: $(basename "$0") [--agent <id>] [--limit <n>]"
  echo ""
  echo "Options:"
  echo "  --agent, -a    Filter by agent ID"
  echo "  --limit, -l    Max results (default: 10)"
  echo ""
  echo "Environment: ELEVENLABS_API_KEY (required)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent|-a) AGENT_ID="$2"; shift 2 ;;
    --limit|-l) LIMIT="$2"; shift 2 ;;
    --help|-h) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo "Error: ELEVENLABS_API_KEY not set" >&2
  exit 1
fi

URL="https://api.elevenlabs.io/v1/convai/conversations?page_size=${LIMIT}"
[[ -n "$AGENT_ID" ]] && URL="${URL}&agent_id=${AGENT_ID}"

response=$(curl -s -X GET "$URL" \
  -H "xi-api-key: $API_KEY" \
  -H "Content-Type: application/json")

# Check for errors
if echo "$response" | jq -e '.detail' >/dev/null 2>&1; then
  echo "Error: $(echo "$response" | jq -r '.detail')" >&2
  exit 1
fi

# Pretty print conversations
echo "$response" | jq -r '
  .conversations[]? |
  "ID: \(.conversation_id)
Status: \(.status)
Agent: \(.agent_id)
Started: \(.start_time_unix_secs | todate)
Duration: \(.call_duration_secs // 0)s
---"
'

count=$(echo "$response" | jq '.conversations | length')
echo "Showing $count conversation(s)"
