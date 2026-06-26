#!/usr/bin/env bash
set -euo pipefail

# Abandon a task that cannot be completed.
#
# Usage: bash abandon.sh <task_id> ["reason"]
# Example: bash abandon.sh abc-123 "Anti-bot protection blocked data extraction"

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 1 ]; then
  echo "Usage: bash $0 <task_id> [reason]" >&2
  echo "Example: bash $0 abc-123 \"CAPTCHA blocked access\"" >&2
  exit 1
fi

TASK_ID="$1"
REASON="${2:-Agent unable to complete this task}"

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

BODY=$(python3 -c "
import json
print(json.dumps({'reason': '''$REASON'''}))
")

RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/abandon" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BODY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$RESP_BODY"
  exit 0
else
  echo "Abandon failed (HTTP $HTTP_CODE): $RESP_BODY" >&2
  exit 1
fi
