#!/usr/bin/env bash
# hotline-check.sh — Quick inbox check with formatted output
# Usage: hotline-check.sh [agent-name] [server-url]
#
# Reads unread messages from Agent Hotline and prints them in a readable format.
# Requires: curl, jq

set -euo pipefail

AGENT="${1:-my-agent}"
SERVER="${2:-http://localhost:3456}"

# Read auth key from config if available
CONFIG="$HOME/.agent-hotline/config"
AUTH_KEY=""
if [[ -f "$CONFIG" ]]; then
  AUTH_KEY=$(grep '^HOTLINE_AUTH_KEY=' "$CONFIG" 2>/dev/null | cut -d= -f2 || true)
fi

# Build curl args
CURL_ARGS=(-sf)
if [[ -n "$AUTH_KEY" ]]; then
  CURL_ARGS+=(-H "Authorization: Bearer $AUTH_KEY")
fi

# Fetch and format inbox
RESPONSE=$(curl "${CURL_ARGS[@]}" "$SERVER/api/inbox/$AGENT" 2>/dev/null) || {
  echo "Could not reach $SERVER" >&2
  exit 1
}

COUNT=$(echo "$RESPONSE" | jq 'length')
if [[ "$COUNT" == "0" ]]; then
  echo "No unread messages."
  exit 0
fi

echo "$RESPONSE" | jq -r '.[] | "[\(.from_agent)] \(.content)"'
