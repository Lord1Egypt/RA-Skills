#!/usr/bin/env bash
# a2a-register status.sh — Check this OpenClaw instance's registration status in the A2A API Gateway
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

# --- Fetch all agents and find ours ---
RESPONSE=$(curl -sS -w "\n%{http_code}" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GATEWAY_URL}/v0/admin/agents" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Error: Failed to fetch agents (HTTP ${HTTP_CODE})" >&2
  echo "$BODY" >&2
  exit 1
fi

# --- Check if our agent is registered ---
echo "═══════════════════════════════════════════════════"
echo "  Agent Registration Status"
echo "═══════════════════════════════════════════════════"
echo ""

FOUND=$(echo "$BODY" | python3 -c "
import sys, json
slug = '$AGENT_SLUG_VAL'
try:
    data = json.load(sys.stdin)
    agents = data.get('data', data) if isinstance(data, dict) else data
    if isinstance(agents, list):
        found = False
        for a in agents:
            if a.get('slug') == slug:
                found = True
                print('  Status:       ✅ REGISTERED')
                print('  Name:         ' + a.get('name', 'N/A'))
                print('  Slug:         ' + a.get('slug', 'N/A'))
                print('  ID:           ' + a.get('id', 'N/A'))
                print('  URL:          ' + a.get('agentUrl', a.get('url', 'N/A')))
                caps = a.get('capabilities', [])
                if isinstance(caps, list):
                    print('  Capabilities: ' + ', '.join(caps))
                else:
                    print('  Capabilities: ' + str(caps))
                print('  Auth Type:    ' + a.get('authType', a.get('auth_type', 'N/A')))
                print('  Agent Status: ' + a.get('status', 'N/A'))
                updated = a.get('updatedAt', a.get('updated_at'))
                if updated:
                    print('  Last Updated: ' + updated)
                break
        if not found:
            print('  Status:       ❌ NOT REGISTERED')
            print('  Agent ' + slug + ' not found in gateway registry')
            print('  Run ./register.sh to register')
    else:
        print('  Status:       ⚠ UNEXPECTED RESPONSE FORMAT')
except Exception as e:
    print('  Status:       ⚠ PARSE ERROR')
    print('  Error: ' + str(e))
" 2>/dev/null)

echo "$FOUND"

# --- Also show total agent count ---
TOTAL=$(echo "$BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    agents = data.get('data', data) if isinstance(data, dict) else data
    if isinstance(agents, list):
        print(len(agents))
    else:
        print('?')
except: print('?')
" 2>/dev/null)

echo ""
echo "Total agents registered: ${TOTAL}"
echo "Gateway: ${GATEWAY_URL}"
echo "═══════════════════════════════════════════════════"
