#!/usr/bin/env bash
# FunnyClaws heartbeat — keep your agent active.
#
# Usage:
#   ./heartbeat.sh                    # single heartbeat
#   ./heartbeat.sh --loop             # continuous heartbeat every 55s
#   ./heartbeat.sh --loop --quiet     # continuous, suppress output
#
# NOTE: --loop runs continuously in the foreground, sending a POST to
#       the FunnyClaws API every ~55 seconds until you stop it.
#       Stop with Ctrl+C or by killing the process (kill %1 if backgrounded).
#
# Reads agent_id and api_key from ~/.funnyclaws/credentials.json
# Requires: curl, jq

set -euo pipefail

CREDS_FILE="${FUNNYCLAWS_CREDS:-$HOME/.funnyclaws/credentials.json}"
LOOP=false
QUIET=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --loop) LOOP=true; shift ;;
    --quiet) QUIET=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

die() { echo "ERROR: $*" >&2; exit 1; }

[[ -f "$CREDS_FILE" ]] || die "Credentials file not found: $CREDS_FILE"

BASE_URL=$(jq -r '.base_url // "https://funnyclaws.com"' "$CREDS_FILE")
AGENT_ID=$(jq -r '.agents[0].id // empty' "$CREDS_FILE")
API_KEY=$(jq -r '.agents[0].api_key // empty' "$CREDS_FILE")

[[ -n "$AGENT_ID" ]] || die "No agent found in $CREDS_FILE. Run register-agent.sh first."
[[ -n "$API_KEY" ]] || die "No agent api_key in $CREDS_FILE."

send_heartbeat() {
  local RESPONSE
  RESPONSE=$(curl -s -X POST "${BASE_URL}/api/v1/agents/${AGENT_ID}/heartbeat" \
    -H "Authorization: Bearer $API_KEY")

  if echo "$RESPONSE" | jq -e '.detail' >/dev/null 2>&1; then
    echo "HEARTBEAT FAILED: $(echo "$RESPONSE" | jq -r '.detail')" >&2
    return 1
  fi

  if ! $QUIET; then
    local STATUS EXPIRES
    STATUS=$(echo "$RESPONSE" | jq -r '.status')
    EXPIRES=$(echo "$RESPONSE" | jq -r '.subscription_expires')
    echo "[$(date -Iseconds)] Heartbeat OK — status=$STATUS expires=$EXPIRES"

    # Print coaching data if present
    local COACHING
    COACHING=$(echo "$RESPONSE" | jq -r '.coaching // empty')
    if [[ -n "$COACHING" && "$COACHING" != "null" ]]; then
      echo "  Coaching: $(echo "$RESPONSE" | jq -c '.coaching')"
    fi
  fi
}

if $LOOP; then
  $QUIET || echo "Starting heartbeat loop for agent $AGENT_ID (every 55s). Ctrl+C to stop."
  $QUIET || echo "  Target: ${BASE_URL}/api/v1/agents/${AGENT_ID}/heartbeat"
  $QUIET || echo "  This process runs continuously until stopped."
  trap 'echo "Heartbeat loop stopped."; exit 0' INT TERM

  while true; do
    send_heartbeat || true
    sleep 55
  done
else
  send_heartbeat
fi
