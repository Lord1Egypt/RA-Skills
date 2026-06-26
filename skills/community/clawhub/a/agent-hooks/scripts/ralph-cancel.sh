#!/usr/bin/env bash
# ralph-cancel.sh — Send cancel signal with 30s TTL
# Usage: ralph-cancel.sh <session-id> [reason]
#
# State layout: ~/.openclaw/shared-context/sessions/<session-id>/cancel.json

set -euo pipefail

SESSION_ID="${1:?Usage: ralph-cancel.sh <session-id> [reason]}"
REASON="${2:-user_abort}"

SESSION_DIR="${HOME}/.openclaw/shared-context/sessions/${SESSION_ID}"
mkdir -p "$SESSION_DIR"

NOW=$(date -u +%FT%TZ)
EXPIRES=$(date -u -v+30S +%FT%TZ 2>/dev/null || date -u -d '+30 seconds' +%FT%TZ)

CANCEL_FILE="${SESSION_DIR}/cancel.json"
TMP="${CANCEL_FILE}.${$}.$(date +%s).tmp"
jq -n --arg at "$NOW" --arg exp "$EXPIRES" --arg r "$REASON" \
  '{requested_at: $at, expires_at: $exp, reason: $r}' > "$TMP"
mv "$TMP" "$CANCEL_FILE"
echo "Cancel signal sent for ${SESSION_ID} (expires in 30s)"
