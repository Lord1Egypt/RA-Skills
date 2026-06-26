#!/bin/bash
# Belong Events skill - JSON-RPC wrapper for OpenClaw agents
# Usage: invoke.sh <method> [params-json]
# Example: invoke.sh discover_events '{"city":"Miami"}'

set -euo pipefail

# Default production gateway is Belong-owned domain; override with BELONG_EVENTS_ENDPOINT for staging/self-hosted.
DEFAULT_ENDPOINT='https://join.belong.net/functions/v1/openclaw-skill-proxy'
ENDPOINT="${BELONG_EVENTS_ENDPOINT:-$DEFAULT_ENDPOINT}"
API_KEY="${BELONG_EVENTS_API_KEY:-}"

METHOD="${1:?Usage: invoke.sh <method> [params-json]}"
DEFAULT_PARAMS='{}'
PARAMS="${2:-$DEFAULT_PARAMS}"

if ! printf '%s' "$METHOD" | grep -Eq '^[A-Za-z][A-Za-z0-9_]*$'; then
  echo "Invalid method: $METHOD" >&2
  exit 2
fi

HEADERS=(-H "Content-Type: application/json")
if [ -n "$API_KEY" ]; then
  HEADERS+=(-H "X-OpenClaw-Key: $API_KEY")
fi

REQUEST_BODY="$(printf '{"jsonrpc":"2.0","id":1,"method":"%s","params":%s}' "$METHOD" "$PARAMS")"

printf '%s' "$REQUEST_BODY" | exec curl -sS -X POST "$ENDPOINT" \
  "${HEADERS[@]}" \
  --data-binary @-
