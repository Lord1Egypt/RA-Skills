#!/bin/bash
# Battlecard API wrapper for OpenClaw
# Usage: source battlecard.sh (for json_escape helper)
#        ./battlecard.sh <tool_name> <json_params>

BATTLECARD_URL="https://battlecard.northr.ai/mcp"

# Escape a string for safe JSON embedding. Returns a quoted JSON string.
# Usage: VAL=$(json_escape "raw string")
json_escape() {
  if command -v jq >/dev/null 2>&1; then
    jq -n --arg v "$1" '$v'
  else
    local s
    s=$(printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\t/\\t/g' | tr '\n' ' ')
    printf '"%s"' "$s"
  fi
}

# Only run the API call when executed directly (not sourced)
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  TOOL_NAME="$1"
  PARAMS="$2"
  PAYLOAD="{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$TOOL_NAME\",\"arguments\":$PARAMS}}"

  if [ -n "$BATTLECARD_API_KEY" ]; then
    curl -s -X POST "$BATTLECARD_URL" \
      -H "Content-Type: application/json" \
      -H "X-Battlecard-Key: $BATTLECARD_API_KEY" \
      --data-raw "$PAYLOAD"
  else
    curl -s -X POST "$BATTLECARD_URL" \
      -H "Content-Type: application/json" \
      --data-raw "$PAYLOAD"
  fi
fi
