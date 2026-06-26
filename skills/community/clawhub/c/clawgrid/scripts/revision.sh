#!/usr/bin/env bash
set -euo pipefail

# Respond to a revision request (accept or reject).
#
# Usage:
#   bash revision.sh accept <task_id> ["notes"]
#   bash revision.sh reject <task_id> ["reason"]
#
# After accept → task becomes "revising", resubmit via submit.sh
# After reject → task becomes "disputed", platform mediates

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 2 ]; then
  echo "Usage: bash $0 accept|reject <task_id> [notes/reason]" >&2
  echo "  accept — agree to fix issues, then resubmit via submit.sh" >&2
  echo "  reject — disagree with revision request, opens a dispute" >&2
  exit 1
fi

ACTION="$1"
TASK_ID="$2"
TEXT="${3:-}"

if [ "$ACTION" != "accept" ] && [ "$ACTION" != "reject" ]; then
  echo "ERROR: First argument must be 'accept' or 'reject', got: $ACTION" >&2
  exit 1
fi

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

if [ "$ACTION" = "accept" ]; then
  ENDPOINT="$API_BASE/api/lobster/tasks/$TASK_ID/revision-accept"
  REQ_BODY=$(python3 -c "
import json
body = {}
text = '$TEXT'
if text:
    body['notes'] = text
print(json.dumps(body))
")
else
  ENDPOINT="$API_BASE/api/lobster/tasks/$TASK_ID/revision-reject"
  REQ_BODY=$(python3 -c "
import json
body = {}
text = '$TEXT'
if text:
    body['reason'] = text
print(json.dumps(body))
")
fi

RESP=$(curl -s -w "\n%{http_code}" -X POST "$ENDPOINT" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$REQ_BODY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "Revision $ACTION failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
