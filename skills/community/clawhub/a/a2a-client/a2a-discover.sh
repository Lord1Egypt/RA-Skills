#!/usr/bin/env bash
# a2a-discover.sh — List available agents and providers on the A2A API Gateway
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF_FILE="${SCRIPT_DIR}/a2a.conf"

# --- Source config file if it exists ---
if [[ -f "$CONF_FILE" ]]; then
  # shellcheck source=a2a.conf
  source "$CONF_FILE"
fi

# --- Defaults (MUST be configured via a2a.conf or env vars) ---
: "${A2A_GATEWAY_URL:=}"
: "${A2A_GATEWAY_API_KEY:=}"

# --- Validate required config ---
if [[ -z "$A2A_GATEWAY_URL" ]]; then
  echo "❌ ERROR: A2A_GATEWAY_URL not set. Configure it in a2a.conf or export it."
  echo "   Example: A2A_GATEWAY_URL=http://your-gateway-host:8090"
  exit 1
fi

GATEWAY_URL="${A2A_GATEWAY_URL}"
API_KEY="${A2A_GATEWAY_API_KEY}"

# --- Parse args (CLI flags override everything) ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --gateway-url) GATEWAY_URL="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# --- Validate gateway URL ---
if [[ -z "$GATEWAY_URL" ]]; then
  echo "❌ ERROR: A2A_GATEWAY_URL not set. Configure it in a2a.conf or export it." >&2
  echo "  Set it in a2a.conf, via env var, or use --gateway-url flag" >&2
  exit 1
fi

# --- Get admin JWT for API authentication ---
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

# --- Try the A2A agents endpoint ---
AGENTS_RESPONSE=$(curl -sS -w "\n%{http_code}" \
  -X GET \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GATEWAY_URL}/v1/a2a/agents" 2>/dev/null)

AGENTS_HTTP=$(echo "$AGENTS_RESPONSE" | tail -1)
AGENTS_BODY=$(echo "$AGENTS_RESPONSE" | sed '$d')

echo "═══════════════════════════════════════════════════"
echo "  A2A API Gateway — Agent & Provider Discovery"
echo "═══════════════════════════════════════════════════"
echo ""

if [[ "$AGENTS_HTTP" == "200" ]]; then
  AGENT_COUNT=$(echo "$AGENTS_BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    agents = data if isinstance(data, list) else data.get('agents', data.get('data', []))
    print(len(agents))
except: print('0')
" 2>/dev/null)
  
  if [[ "$AGENT_COUNT" != "0" ]]; then
    echo "Registered A2A Agents:"
    echo "$AGENTS_BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    agents = data if isinstance(data, list) else data.get('agents', data.get('data', []))
    for a in agents:
        print(f\"  Name:         {a.get('name', 'N/A')}\")
        print(f\"  Slug:         {a.get('slug', 'N/A')}\")
        print(f\"  URL:          {a.get('url', 'N/A')}\")
        print(f\"  Capabilities: {a.get('capabilities', 'none')}\")
        print(f\"  Status:       {a.get('status', 'N/A')}\")
        print('  ─────────────────────────────────')
except Exception as e:
    print(f'  Parse error: {e}')
" 2>/dev/null
  else
    echo "No A2A agents registered yet."
  fi
else
  echo "⚠ A2A agents endpoint not available (HTTP ${AGENTS_HTTP})"
  echo "  The /v1/a2a/agents route may not be implemented on this gateway."
  echo ""
fi

# --- Also show available LLM providers (as they represent routing targets) ---
echo ""
echo "Available LLM Providers:"
echo "───────────────────────────────────────────────────"

PROVIDERS_RESPONSE=$(curl -sS \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GATEWAY_URL}/v0/admin/providers" 2>/dev/null)

echo "$PROVIDERS_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    providers = data.get('data', []) if isinstance(data, dict) else data
    if not providers:
        print('  No providers configured.')
    for p in providers:
        name = p.get('name', 'N/A')
        slug = p.get('slug', 'N/A')
        ptype = p.get('providerType', 'N/A')
        models = p.get('config', {}).get('models', [])
        model_names = [m.get('id', m.get('name', '?')) for m in models[:5]]
        suffix = f' (+{len(models)-5} more)' if len(models) > 5 else ''
        print(f'  {name} ({slug}) [{ptype}]')
        print(f'    Models: {\", \".join(model_names)}{suffix}')
        print(f'    ─────────────────────────────────')
except Exception as e:
    print(f'  Parse error: {e}')
" 2>/dev/null

echo ""
echo "Gateway: ${GATEWAY_URL}"
echo "Note: To send a task, use the provider slug in --agent flag"
