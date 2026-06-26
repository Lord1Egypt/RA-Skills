#!/bin/bash
# Ultra-simple status check — outputs ONE line of plain text.
# The agent should relay this text to the owner, nothing else.
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"
if [ ! -f "$CONFIG" ]; then
  echo "NOT_REGISTERED: No config.json found. Follow the setup guide to register first."
  exit 0
fi

API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")
API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")

RESULT=$(curl -s -H "Authorization: Bearer $API_KEY" "$API_BASE/api/lobster/status" --max-time 10 2>/dev/null)
if [ -z "$RESULT" ]; then
  echo "ERROR: Could not reach $API_BASE. Server may be down."
  exit 0
fi

STATUS_MSG=$(echo "$RESULT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read())['message'])" 2>/dev/null || echo "ERROR: Unexpected response from server.")

# Append exec approval warning if not configured
CHECK_EXEC="$SKILL_DIR/scripts/check-exec-approval.sh"
if [ -x "$CHECK_EXEC" ]; then
  _EA_STATUS=$(bash "$CHECK_EXEC" 2>/dev/null | head -1 || echo "OK")
  if [ "$_EA_STATUS" != "OK" ]; then
    STATUS_MSG="$STATUS_MSG | WARNING: Exec approval not configured for automated tasks. Run: bash scripts/setup-exec-approval.sh"
  fi
fi

echo "$STATUS_MSG"
