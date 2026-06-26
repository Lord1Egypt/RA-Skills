#!/bin/bash
# meter-sync.sh — Sync local spend data to hosted dashboard
# Reads ~/.agent-meter/spend.jsonl, POSTs unsynced session_summaries
# to the hosted backend, tracks sync cursor to avoid re-sending.
#
# Config: ~/.agent-meter/sync.json
#   {
#     "api_key": "am_live_...",
#     "agent_name": "macbook-claude-code",
#     "endpoint": "https://api.agentmeter.io"
#   }
#
# Usage:
#   meter-sync.sh              — sync unsynced records
#   meter-sync.sh --setup      — interactive config setup
#   meter-sync.sh --status     — show sync status
#   meter-sync.sh --dry-run    — show what would sync without sending

set -euo pipefail

SPEND_DIR="$HOME/.agent-meter"
SPEND_FILE="$SPEND_DIR/spend.jsonl"
SYNC_CONFIG="$SPEND_DIR/sync.json"
SYNC_CURSOR="$SPEND_DIR/.sync-cursor"  # stores last synced timestamp

# --- Setup mode ---
if [ "${1:-}" = "--setup" ]; then
  mkdir -p "$SPEND_DIR"
  echo "agent-meter sync setup"
  echo "====================="
  echo ""
  read -rp "API key (am_live_...): " API_KEY
  read -rp "Agent name (e.g. macbook-claude-code): " AGENT_NAME
  read -rp "Endpoint [https://api.agentmeter.io]: " ENDPOINT
  ENDPOINT="${ENDPOINT:-https://api.agentmeter.io}"

  # Verify the key works
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $API_KEY" \
    "$ENDPOINT/v1/sessions/status" 2>/dev/null) || HTTP_CODE="000"

  if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
    echo "ERROR: API key rejected ($HTTP_CODE). Check your key."
    exit 1
  fi

  jq -n \
    --arg key "$API_KEY" \
    --arg name "$AGENT_NAME" \
    --arg endpoint "$ENDPOINT" \
    '{ api_key: $key, agent_name: $name, endpoint: $endpoint }' > "$SYNC_CONFIG"

  chmod 600 "$SYNC_CONFIG"
  echo ""
  echo "Config saved to $SYNC_CONFIG"
  echo "Run 'meter-sync.sh' to sync."
  exit 0
fi

# --- Preflight checks ---
if [ ! -f "$SPEND_FILE" ]; then
  echo "No spend data found at $SPEND_FILE"
  echo "Run the meter skill first to capture some sessions."
  exit 1
fi

if [ ! -f "$SYNC_CONFIG" ]; then
  echo "No sync config found. Run: meter-sync.sh --setup"
  exit 1
fi

API_KEY=$(jq -r '.api_key' "$SYNC_CONFIG")
AGENT_NAME=$(jq -r '.agent_name' "$SYNC_CONFIG")
ENDPOINT=$(jq -r '.endpoint' "$SYNC_CONFIG")

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
  echo "ERROR: No api_key in $SYNC_CONFIG. Run: meter-sync.sh --setup"
  exit 1
fi

# --- Determine unsynced records ---
LAST_SYNCED=""
if [ -f "$SYNC_CURSOR" ]; then
  LAST_SYNCED=$(cat "$SYNC_CURSOR")
fi

if [ -n "$LAST_SYNCED" ]; then
  # Records with timestamp > last synced
  UNSYNCED=$(jq -c "select(.ts > \"$LAST_SYNCED\")" "$SPEND_FILE")
else
  # Everything
  UNSYNCED=$(cat "$SPEND_FILE")
fi

RECORD_COUNT=$(echo "$UNSYNCED" | grep -c '^' 2>/dev/null || echo "0")

if [ "$RECORD_COUNT" -eq 0 ]; then
  echo "Everything synced. No new records."
  exit 0
fi

# --- Status mode ---
if [ "${1:-}" = "--status" ]; then
  echo "Sync status"
  echo "==========="
  echo "Agent name:    $AGENT_NAME"
  echo "Endpoint:      $ENDPOINT"
  echo "Last synced:   ${LAST_SYNCED:-never}"
  echo "Unsynced:      $RECORD_COUNT records"
  TOTAL=$(wc -l < "$SPEND_FILE" | tr -d ' ')
  echo "Total local:   $TOTAL records"
  exit 0
fi

# --- Dry run mode ---
if [ "${1:-}" = "--dry-run" ]; then
  echo "Would sync $RECORD_COUNT records to $ENDPOINT"
  echo ""
  echo "$UNSYNCED" | jq -r '[.ts, .project, .model, (.cost_usd | tostring)] | join("  ")' | head -20
  if [ "$RECORD_COUNT" -gt 20 ]; then
    echo "... and $((RECORD_COUNT - 20)) more"
  fi
  exit 0
fi

# --- POST to hosted backend ---
echo "Syncing $RECORD_COUNT sessions to $ENDPOINT..."

# Pipe directly from jq to curl to avoid ARG_MAX limits on large payloads
RESPONSE=$(echo "$UNSYNCED" | jq -sc --arg agent "$AGENT_NAME" '
  {
    agentName: $agent,
    sessions: [.[] | {
      id: .session_id,
      ts: .ts,
      api: .api,
      model: .model,
      project: .project,
      totalCalls: (.total_calls // 0),
      tokensIn: (.tokens_in // 0),
      tokensOut: (.tokens_out // 0),
      cacheCreation: (.cache_creation // 0),
      cacheRead: (.cache_read // 0),
      costUsd: (.cost_usd // 0),
      source: .source,
      purpose: (.purpose // null),
      intent: (.intent // null)
    }]
  }
' | curl -s -w "\n%{http_code}" \
  -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @- \
  "$ENDPOINT/v1/sessions/batch")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
  ACCEPTED=$(echo "$BODY" | jq -r '.accepted // .inserted // "?"')
  DUPES=$(echo "$BODY" | jq -r '.duplicatesIgnored // 0')
  echo "Synced: $ACCEPTED accepted, $DUPES duplicates ignored."

  # Update cursor to latest timestamp in synced batch
  NEW_CURSOR=$(echo "$UNSYNCED" | jq -r '.ts' | sort | tail -1)
  echo "$NEW_CURSOR" > "$SYNC_CURSOR"
else
  echo "ERROR: Sync failed (HTTP $HTTP_CODE)"
  echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
  exit 1
fi
