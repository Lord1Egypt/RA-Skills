#!/usr/bin/env bash
# antenna-health.sh — Check health of a remote OpenClaw peer
# Usage: antenna-health.sh <peer>
#
# Reads peer URL and token from the flat antenna-peers.json format.
# Hits the peer's /health endpoint and reports status.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"

# shellcheck source=../lib/peers.sh
source "$SKILL_DIR/lib/peers.sh"

PEER="${1:?Usage: antenna-health.sh <peer>}"

PEER_URL=$(peers_get "$PEER" url)
TOKEN_FILE=$(peers_get "$PEER" token_file)

if [[ -z "$PEER_URL" ]]; then
  echo "{\"error\":\"Unknown peer: $PEER\"}" >&2
  exit 1
fi

# Resolve relative token paths against SKILL_DIR
[[ -n "$TOKEN_FILE" && "$TOKEN_FILE" != /* ]] && TOKEN_FILE="$SKILL_DIR/$TOKEN_FILE"

if [[ -z "$TOKEN_FILE" || ! -f "$TOKEN_FILE" ]]; then
  echo "{\"error\":\"Token file not found for peer: $PEER\"}" >&2
  exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")

RESPONSE=$(curl -s --max-time 10 -w '\n__HTTP_CODE__%{http_code}' \
  -H "Authorization: Bearer ${TOKEN}" \
  "${PEER_URL}/health" 2>&1) || {
  jq -n --arg peer "$PEER" --arg url "$PEER_URL" \
    '{ok: false, peer: $peer, url: $url, error: "Connection failed"}'
  exit 1
}

BODY=$(echo "$RESPONSE" | sed '/__HTTP_CODE__/d')
HTTP_CODE=$(echo "$RESPONSE" | grep '__HTTP_CODE__' | sed 's/__HTTP_CODE__//')

if [[ "$HTTP_CODE" == "200" ]]; then
  echo "$BODY" | jq --arg peer "$PEER" '. + {peer: $peer}' 2>/dev/null || echo "$BODY"
else
  jq -n --arg peer "$PEER" --arg code "$HTTP_CODE" --arg body "$BODY" \
    '{ok: false, peer: $peer, httpCode: ($code | tonumber), response: $body}'
  exit 1
fi
