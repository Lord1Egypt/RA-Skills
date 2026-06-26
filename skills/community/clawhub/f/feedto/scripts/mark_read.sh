#!/bin/bash
set -euo pipefail
# Mark feeds as processed
# Usage: mark_read.sh id1 id2 id3 ...
# Requires: curl, FEEDTO_API_KEY env var
# No python3/macOS dependencies

API_URL="${FEEDTO_API_URL:-https://feedto.ai}"
API_KEY="${FEEDTO_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: FEEDTO_API_KEY not set"
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "ERROR: No feed IDs provided. Usage: mark_read.sh id1 id2 ..."
  exit 1
fi

# Validate UUIDs
for id in "$@"; do
  if ! echo "$id" | grep -qE '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'; then
    echo "ERROR: Invalid feed ID format: $id"
    exit 1
  fi
done

# Build JSON array manually (no python3 needed)
IDS_JSON="["
FIRST=true
for id in "$@"; do
  if [ "$FIRST" = true ]; then
    IDS_JSON="${IDS_JSON}\"${id}\""
    FIRST=false
  else
    IDS_JSON="${IDS_JSON},\"${id}\""
  fi
done
IDS_JSON="${IDS_JSON}]"

RESPONSE=$(curl -s -f --max-time 15 --connect-timeout 5 -X PATCH \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"ids\": $IDS_JSON, \"status\": \"sent\"}" \
  "${API_URL}/api/feeds/pending" 2>&1) || {
  echo "ERROR: Failed to mark feeds as read"
  exit 1
}

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
node "$SCRIPT_DIR/ack.mjs" "$@" >/dev/null 2>&1 || true

echo "OK: Marked $# feed(s) as processed"
