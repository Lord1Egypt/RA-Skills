#!/usr/bin/env bash
# a2a-get-task.sh — Check status of an A2A task via the A2A API Gateway
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF_FILE="${SCRIPT_DIR}/a2a.conf"

# --- Source config file if it exists ---
if [[ -f "$CONF_FILE" ]]; then
  # shellcheck source=a2a.conf
  source "$CONF_FILE"
fi

# --- Defaults (empty = must be configured) ---
: "${A2A_GATEWAY_URL:=}"
: "${A2A_GATEWAY_API_KEY:=}"

# --- Apply config ---
GATEWAY_URL="${A2A_GATEWAY_URL}"
API_KEY="${A2A_GATEWAY_API_KEY}"
TASK_ID=""

# --- Parse args (CLI flags override everything) ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-id) TASK_ID="$2"; shift 2 ;;
    --gateway-url) GATEWAY_URL="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# --- Validate gateway URL ---
if [[ -z "$GATEWAY_URL" ]]; then
  echo "Error: A2A_GATEWAY_URL not configured" >&2
  echo "  Set it in a2a.conf, via env var, or use --gateway-url flag" >&2
  exit 1
fi

# --- Validate required args ---
if [[ -z "$TASK_ID" ]]; then
  echo "Error: --task-id is required" >&2
  echo "Usage: a2a-get-task.sh --task-id <id> [--gateway-url URL] [--api-key KEY]" >&2
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

# --- Call the task status endpoint ---
RESPONSE=$(curl -sS -w "\n%{http_code}" \
  -X GET \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  "${GATEWAY_URL}/v1/a2a/tasks/${TASK_ID}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Error: HTTP $HTTP_CODE" >&2
  echo "$BODY" >&2
  exit 1
fi

# --- Format output ---
echo "$BODY" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    task = data.get('task', data)
    task_id = task.get('id', 'unknown')
    status = task.get('status', 'unknown')
    session = task.get('sessionId', 'N/A')
    created = task.get('createdAt', 'N/A')
    updated = task.get('updatedAt', 'N/A')
    message = task.get('message', {})
    msg_content = message.get('content', 'N/A') if isinstance(message, dict) else 'N/A'
    metadata = task.get('metadata', {})
    
    print(f'Task:     {task_id}')
    print(f'Status:   {status}')
    print(f'Session:  {session}')
    print(f'Created:  {created}')
    print(f'Updated:  {updated}')
    print(f'Message:  {msg_content[:100]}')
    if metadata:
        print(f'Metadata: {json.dumps(metadata)}')
    
    # Show artifacts/results
    artifacts = task.get('artifacts', [])
    if artifacts:
        print()
        print('Results:')
        for i, a in enumerate(artifacts):
            desc = a.get('description', 'N/A')
            artifact_type = a.get('type', 'N/A')
            content = a.get('content', {})
            print(f'  [{i+1}] {desc} (type: {artifact_type})')
            
            if isinstance(content, dict):
                model = content.get('model', 'N/A')
                usage = content.get('usage', {})
                payload = content.get('payload', {})
                choices = payload.get('choices', [])
                
                print(f'      Model: {model}')
                if usage:
                    print(f'      Tokens: {usage.get(\"total_tokens\", \"?\")} (prompt: {usage.get(\"prompt_tokens\", \"?\")}, completion: {usage.get(\"completion_tokens\", \"?\")})')
                    cost = usage.get('cost_total', 0)
                    if cost:
                        print(f'      Cost: \${cost:.6f}')
                
                if choices:
                    for c in choices:
                        msg = c.get('message', {})
                        result_text = msg.get('content', '')
                        if result_text:
                            # Print result with indentation
                            for line in result_text.strip().split('\n'):
                                print(f'      {line}')
    
    # Show error if present
    error = task.get('error')
    if error:
        print()
        print(f'Error: {error}')
        
except Exception as e:
    # Fallback: just print the raw JSON
    raw = sys.stdin.read()
    print(raw if raw else 'Failed to parse response')
    print(f'Parse error: {e}')
" 2>/dev/null
