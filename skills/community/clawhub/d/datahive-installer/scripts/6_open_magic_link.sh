#!/bin/bash
set -euo pipefail
CDP_URL="${CDP_URL:-http://localhost:9222}"
TARGET_URL="${TARGET_URL:?TARGET_URL env variable is required}"

curl -sf "$CDP_URL/json/version" >/dev/null || {
  echo "Error: Chrome DevTools endpoint is unavailable at $CDP_URL (is Chrome running with --remote-debugging-port=9222?)" >&2
  exit 1
}

NEW_TAB=$(curl -sf -X PUT "$CDP_URL/json/new") || {
  echo "Error: failed to create tab at $CDP_URL" >&2
  exit 1
}

WS_URL=$(echo "$NEW_TAB" | grep '"webSocketDebuggerUrl"' | cut -d'"' -f4)
RESPONSE=$(websocat -n1 "$WS_URL" <<< "{\"id\":1,\"method\":\"Page.navigate\",\"params\":{\"url\":\"$TARGET_URL\"}}")

echo "$RESPONSE"
echo "Opened $TARGET_URL"
