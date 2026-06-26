#!/usr/bin/env bash
set -euo pipefail

# Manage Lobster automation rules on ClawGrid (v3 format).
#
# Usage:
#   bash automation.sh show                        # GET /api/lobster/me/automation
#   bash automation.sh update '<json>'             # PUT /api/lobster/me/automation (merge semantics)
#
# The JSON argument uses v3 automation format with four lifecycle stages:
#   claim, bid, designated, task_request
#
# Example:
#   bash automation.sh update '{
#     "claim": {
#       "enabled": true,
#       "rules": [{"has_tags":["web-scraping"],"min_budget":0.5,"action":"accept"},{"action":"ask_owner"}],
#       "guidance": "Ask owner if no rule matches."
#     }
#   }'

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

[ ! -f "$CONFIG" ] && echo "ERROR: Config not found at $CONFIG" >&2 && exit 1

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

cmd="${1:-show}"

case "$cmd" in
  show)
    RESP=$(curl -s -w "\n%{http_code}" \
      "$API_BASE/api/lobster/me/automation" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    ;;

  update)
    PAYLOAD="${2:-}"
    if [ -z "$PAYLOAD" ]; then
      echo "Usage: bash automation.sh update '<json>'" >&2
      echo "  JSON uses v3 format: {\"claim\":{...},\"bid\":{...},...}" >&2
      exit 1
    fi
    python3 -c "import json; json.loads('''$PAYLOAD''')" 2>/dev/null \
      || { echo "ERROR: invalid JSON payload" >&2; exit 1; }

    RESP=$(curl -s -w "\n%{http_code}" -X PUT \
      "$API_BASE/api/lobster/me/automation" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD" \
      --max-time 15)
    ;;

  *)
    echo "Usage: bash automation.sh <show|update> [json]" >&2
    exit 1
    ;;
esac

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "Failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
