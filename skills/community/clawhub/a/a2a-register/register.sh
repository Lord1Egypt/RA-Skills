#!/usr/bin/env bash
# a2a-register register.sh — Register this OpenClaw instance as an A2A agent in the A2A API Gateway
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_DIR="${SCRIPT_DIR}/../a2a-client"
CONF_FILE="${CLIENT_DIR}/a2a.conf"

# --- Source config file if it exists ---
if [[ -f "$CONF_FILE" ]]; then
  # shellcheck source=a2a.conf
  source "$CONF_FILE"
fi

# --- Auto-detect defaults (only for agent identity, NOT gateway URL) ---
_auto_ip() { tailscale ip -4 2>/dev/null || hostname -I | awk '{print $1}'; }
_auto_slug() { hostname -s 2>/dev/null | tr '[:upper:]' '[:lower:]' || echo "openclaw"; }
_detected_ip="$(_auto_ip)"
_detected_slug="$(_auto_slug)"

: "${A2A_GATEWAY_URL:=""}"  # REQUIRED — configure via a2a.conf or env var
: "${A2A_GATEWAY_API_KEY:=""}"
: "${AGENT_NAME:="${_detected_slug}"}"
: "${AGENT_SLUG:="${_detected_slug}"}"
: "${AGENT_URL:="http://${_detected_ip}:${LISTENER_PORT:-8100}"}"
: "${AGENT_CAPABILITIES:="chat,code,research"}"

# --- Apply config ---
GATEWAY_URL="${A2A_GATEWAY_URL}"
API_KEY="${A2A_GATEWAY_API_KEY}"
AGENT_NAME_VAL="${AGENT_NAME}"
AGENT_SLUG_VAL="${AGENT_SLUG}"
AGENT_URL_VAL="${AGENT_URL}"
CAPABILITIES="${AGENT_CAPABILITIES}"

# --- Parse args (CLI flags override everything) ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --gateway-url) GATEWAY_URL="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    --name) AGENT_NAME_VAL="$2"; shift 2 ;;
    --slug) AGENT_SLUG_VAL="$2"; shift 2 ;;
    --url) AGENT_URL_VAL="$2"; shift 2 ;;
    --capabilities) CAPABILITIES="$2"; shift 2 ;;
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
echo "Obtaining admin JWT from gateway..."
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

echo "✅ JWT obtained"

# --- Fetch existing agents to check for slug conflict and get workspaceId ---
echo "Checking if agent '${AGENT_SLUG_VAL}' already exists..."
EXISTING=$(curl -sS -w "\n%{http_code}" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GATEWAY_URL}/v0/admin/agents" 2>/dev/null)

EXISTING_HTTP=$(echo "$EXISTING" | tail -1)
EXISTING_BODY=$(echo "$EXISTING" | sed '$d')

# Extract existing agent ID and workspace ID
EXISTING_ID=$(echo "$EXISTING_BODY" | python3 -c "
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

WORKSPACE_ID=$(echo "$EXISTING_BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    agents = data.get('data', data) if isinstance(data, dict) else data
    if isinstance(agents, list) and agents:
        print(agents[0].get('workspaceId', ''))
except: pass
" 2>/dev/null)

# --- Build the agent payload (gateway uses agentUrl, not url) ---
PAYLOAD=$(python3 -c "
import json, sys
payload = {
    'name': sys.argv[1],
    'slug': sys.argv[2],
    'agentUrl': sys.argv[3],
    'capabilities': sys.argv[4].split(','),
    'authType': 'bearer',
    'status': 'active'
}
if sys.argv[5]:
    payload['workspaceId'] = sys.argv[5]
print(json.dumps(payload))
" "$AGENT_NAME_VAL" "$AGENT_SLUG_VAL" "$AGENT_URL_VAL" "$CAPABILITIES" "$WORKSPACE_ID")

if [[ -n "$EXISTING_ID" ]]; then
  # --- Update existing agent ---
  echo "Agent '${AGENT_SLUG_VAL}' exists (ID: ${EXISTING_ID}) — updating..."
  RESPONSE=$(curl -sS -w "\n%{http_code}" \
    -X PUT \
    -H "Authorization: Bearer ${AUTH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "${GATEWAY_URL}/v0/admin/agents/${EXISTING_ID}" 2>/dev/null)
else
  # --- Create new agent ---
  echo "Agent '${AGENT_SLUG_VAL}' not found — creating..."
  RESPONSE=$(curl -sS -w "\n%{http_code}" \
    -X POST \
    -H "Authorization: Bearer ${AUTH_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "${GATEWAY_URL}/v0/admin/agents" 2>/dev/null)
fi

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "201" ]]; then
  echo "Error: HTTP ${HTTP_CODE}" >&2
  echo "$BODY" >&2
  exit 1
fi

# --- Format output ---
echo ""
echo "═══════════════════════════════════════════════════"
echo "  Agent Registered Successfully"
echo "═══════════════════════════════════════════════════"
echo "$BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    agent = data.get('data', data) if isinstance(data, dict) else data
    if isinstance(agent, list) and agent:
        agent = agent[0]
    print('  Name:         ' + agent.get('name', 'N/A'))
    print('  Slug:         ' + agent.get('slug', 'N/A'))
    print('  ID:           ' + agent.get('id', 'N/A'))
    print('  URL:          ' + agent.get('agentUrl', agent.get('url', 'N/A')))
    caps = agent.get('capabilities', [])
    if isinstance(caps, list):
        print('  Capabilities: ' + ', '.join(caps))
    else:
        print('  Capabilities: ' + str(caps))
    print('  Auth Type:    ' + agent.get('authType', 'N/A'))
    print('  Status:       ' + agent.get('status', 'N/A'))
except Exception as e:
    print('  (raw response above)')
    print('  Parse note: ' + str(e))
" 2>/dev/null
echo "═══════════════════════════════════════════════════"
echo ""
echo "Gateway: ${GATEWAY_URL}"
echo "Next: Start the listener with a2a-server/start.sh"
