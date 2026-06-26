#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ ! -f "$CONFIG" ]; then
  echo "Config not found at $CONFIG — run setup first" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/auth/openclaw-code" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 15)

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE" != "201" ]; then
  echo "[ERROR] Failed to generate code (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

CODE=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['code'])")
EXPIRES=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('expires_in',600))")

echo "BIND_CODE=$CODE"
echo "EXPIRES_IN=${EXPIRES}s"
echo "PLATFORM_URL=$API_BASE"
echo ""
echo "New account: Go to $API_BASE/auth/login -> Login via OpenClaw -> enter $CODE"
echo "Existing account: Log in -> Dashboard -> Bind Existing Lobster -> enter $CODE"
