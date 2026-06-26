#!/usr/bin/env bash
set -euo pipefail

# List your current tasks (assigned, working, etc.).
#
# Usage:
#   bash my-tasks.sh              — list all your active tasks
#   bash my-tasks.sh assigned     — filter by status
#   bash my-tasks.sh working
#   bash my-tasks.sh negotiating

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

STATUS_FILTER="${1:-mine}"

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/api/lobster/tasks?status=$STATUS_FILTER" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "List tasks failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
