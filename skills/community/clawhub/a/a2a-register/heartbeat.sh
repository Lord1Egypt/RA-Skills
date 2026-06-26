#!/usr/bin/env bash
# a2a-register heartbeat.sh — Send a liveness heartbeat to the A2A API Gateway
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_DIR="${SCRIPT_DIR}/../a2a-client"
CONF_FILE="${CLIENT_DIR}/a2a.conf"

# --- Source config file if it exists ---
if [[ -f "$CONF_FILE" ]]; then
  # shellcheck source=a2a.conf
  source "$CONF_FILE"
fi

# --- Auto-detect defaults (agent identity only, NOT gateway URL) ---
_auto_slug() { hostname -s 2>/dev/null | tr '[:upper:]' '[:lower:]' || echo "openclaw"; }

: "${A2A_GATEWAY_URL:=""}"  # REQUIRED — configure via a2a.conf or env var
: "${A2A_GATEWAY_API_KEY:=""}"
: "${AGENT_SLUG:="$(_auto_slug)"}"

# --- Apply config ---
GATEWAY_URL="${A2A_GATEWAY_URL}"
API_KEY="${A2A_GATEWAY_API_KEY}"
AGENT_SLUG_VAL="${AGENT_SLUG}"

# --- Parse args (CLI flags override everything) ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --gateway-url) GATEWAY_URL="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    --slug) AGENT_SLUG_VAL="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# --- Validate gateway URL ---
if [[ -z "$GATEWAY_URL" ]]; then
  echo "Error: A2A_GATEWAY_URL not configured" >&2
  echo "  Set it in a2a.conf, via env var, or use --gateway-url flag" >&2
  exit 1
fi

# --- Get admin JWT ---
AUTH_TOKEN=$(curl -sS "${GATEWAY_URL}/v0/admin/bootstrap" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('accessToken', ''))
except: print('')
" 2>/dev/null)

if [[ -z "$AUTH_TOKEN" ]]; then
  echo "Error: Failed to obtain admin JWT from gateway" >&2
  exit 1
fi

# --- Find the agent ID ---
EXISTING=$(curl -sS \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GATEWAY_URL}/v0/admin/agents" 2>/dev/null)

AGENT_ID=$(echo "$EXISTING" | python3 -c "
import sys, json
slug = '$AGENT_SLUG_VAL'
try:
    data = json.load(sys.stdin)
    agents = data.get('data', data) if isinstance(data, dict) else data
    if isinstance(agents, list):
        for a in agents:
            if a.get('slug') == slug:
                print(a.get('id', ''))
                break
except: pass
" 2>/dev/null)

if [[ -z "$AGENT_ID" ]]; then
  echo "⚠ Agent '${AGENT_SLUG_VAL}' not registered — cannot send heartbeat"
  echo "  Register first: ./register.sh"
  exit 1
fi

# --- Send heartbeat ---
RESPONSE=$(curl -sS -w "\n%{http_code}" \
  -X PATCH \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"status\": \"online\"}" \
  "${GATEWAY_URL}/v0/admin/agents/${AGENT_ID}/heartbeat" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)

if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "204" ]]; then
  BODY=$(echo "$RESPONSE" | sed '$d')
  echo "Error: Heartbeat failed (HTTP ${HTTP_CODE})" >&2
  echo "$BODY" >&2
  exit 1
fi

echo "✅ Heartbeat sent for '${AGENT_SLUG_VAL}' (ID: ${AGENT_ID})"
