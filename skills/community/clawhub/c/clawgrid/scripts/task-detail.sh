#!/usr/bin/env bash
set -euo pipefail

# Fetch details for a single task.
#
# Usage: bash task-detail.sh <task_id>
# Example: bash task-detail.sh abc-123

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 1 ]; then
  echo "Usage: bash $0 <task_id>" >&2
  exit 1
fi

TASK_ID="$1"

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/api/lobster/tasks/$TASK_ID" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "Task detail failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
