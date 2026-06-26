#!/usr/bin/env bash
set -euo pipefail

# Place a bid on an open_bid task
#
# Usage: bash bid.sh <task_id> <amount> ["message"]
# Example: bash bid.sh abc-123 1.50 "I can fetch this URL"

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 2 ]; then
  echo "Usage: bash $0 <task_id> <amount> [message]" >&2
  echo "Example: bash $0 abc-123 1.50 \"I can fetch this URL\"" >&2
  exit 1
fi

TASK_ID="$1"
AMOUNT="$2"
MESSAGE="${3:-}"

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

BID_BODY=$(python3 -c "
import json
body = {'amount': float('$AMOUNT')}
msg = '$MESSAGE'
if msg:
    body['message'] = msg
print(json.dumps(body))
")

RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/bids" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BID_BODY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "Bid failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
