#!/usr/bin/env bash
# conto-check.sh — Conto policy check & management helper for Hermes
#
# Setup:
#   conto-check.sh setup <agent_name> <wallet_address> [chain_type] [chain_id]
#
# Payment commands (standard SDK key):
#   conto-check.sh approve <amount> <recipient> <sender> <chain_id> [purpose] [category]
#   conto-check.sh confirm <approval_id> <tx_hash> <approval_token>
#   conto-check.sh x402 <amount> <recipient> <resource_url> [facilitator] [scheme]
#   conto-check.sh budget
#   conto-check.sh services
#
# Policy commands (requires admin SDK key):
#   conto-check.sh policies
#   conto-check.sh policy <id>
#   conto-check.sh create-policy <json_body>
#   conto-check.sh update-policy <id> <json_body>
#   conto-check.sh delete-policy <id>
#   conto-check.sh get-rules <policy_id>
#   conto-check.sh set-rules <policy_id> <json_body>
#   conto-check.sh add-rule <policy_id> <json_body>
#   conto-check.sh delete-rule <policy_id> <rule_id>

set -euo pipefail

API_URL="${CONTO_API_URL:-https://conto.finance}"

# SDK key is required for all commands except setup
if [[ "${1:-}" != "setup" ]]; then
  SDK_KEY="${CONTO_SDK_KEY:?CONTO_SDK_KEY is required}"
fi

# Helper: make authenticated request
_conto_request() {
  local method="$1" endpoint="$2" body="${3:-}"
  local url="${API_URL}${endpoint}"
  local args=(-s -w "\n%{http_code}" -X "$method" -H "Authorization: Bearer $SDK_KEY" -H "Content-Type: application/json")
  if [[ -n "$body" ]]; then
    args+=(-d "$body")
  fi
  local response
  response=$(curl "${args[@]}" "$url")
  local http_code
  http_code=$(echo "$response" | tail -1)
  local body_out
  body_out=$(echo "$response" | sed '$d')
  if [[ "$http_code" -ge 400 ]]; then
    echo "{\"error\": true, \"httpStatus\": $http_code, \"response\": $body_out}"
    exit 1
  fi
  echo "$body_out"
}

case "${1:-help}" in

  # ── Payment commands ──

  approve)
    amount="${2:?amount required}"
    recipient="${3:?recipientAddress required}"
    sender="${4:?senderAddress required}"
    chain_id="${5:?chainId required (e.g. 8453 for Base, 42431 for Tempo Testnet)}"
    purpose="${6:-}"
    category="${7:-}"

    payload=$(cat <<EOF
{
  "amount": $amount,
  "recipientAddress": "$recipient",
  "senderAddress": "$sender",
  "purpose": $(if [[ -n "$purpose" ]]; then echo "\"$purpose\""; else echo "null"; fi),
  "category": $(if [[ -n "$category" ]]; then echo "\"$category\""; else echo "null"; fi),
  "chainId": $chain_id
}
EOF
)
    _conto_request POST /api/sdk/payments/approve "$payload"
    ;;

  confirm)
    approval_id="${2:?approvalId required}"
    tx_hash="${3:?txHash required}"
    approval_token="${4:?approvalToken required}"

    payload=$(cat <<EOF
{
  "txHash": "$tx_hash",
  "approvalToken": "$approval_token"
}
EOF
)
    _conto_request POST "/api/sdk/payments/$approval_id/confirm" "$payload"
    ;;

  x402)
    amount="${2:?amount required}"
    recipient="${3:?recipientAddress required}"
    resource_url="${4:?resourceUrl required}"
    facilitator="${5:-}"
    scheme="${6:-}"

    payload=$(cat <<EOF
{
  "amount": $amount,
  "recipientAddress": "$recipient",
  "resourceUrl": "$resource_url",
  "facilitator": $(if [[ -n "$facilitator" ]]; then echo "\"$facilitator\""; else echo "null"; fi),
  "scheme": $(if [[ -n "$scheme" ]]; then echo "\"$scheme\""; else echo "null"; fi),
  "category": "API_PROVIDER"
}
EOF
)
    _conto_request POST /api/sdk/x402/pre-authorize "$payload"
    ;;

  budget)
    _conto_request GET /api/sdk/x402/budget
    ;;

  services)
    _conto_request GET /api/sdk/x402/services
    ;;

  # ── Policy management commands (requires admin SDK key) ──

  policies)
    _conto_request GET /api/policies
    ;;

  policy)
    policy_id="${2:?policy_id required}"
    _conto_request GET "/api/policies/$policy_id"
    ;;

  create-policy)
    body="${2:?JSON body required}"
    _conto_request POST /api/policies "$body"
    ;;

  update-policy)
    policy_id="${2:?policy_id required}"
    body="${3:?JSON body required}"
    _conto_request PATCH "/api/policies/$policy_id" "$body"
    ;;

  delete-policy)
    policy_id="${2:?policy_id required}"
    _conto_request DELETE "/api/policies/$policy_id"
    ;;

  get-rules)
    policy_id="${2:?policy_id required}"
    _conto_request GET "/api/policies/$policy_id/rules"
    ;;

  set-rules)
    policy_id="${2:?policy_id required}"
    body="${3:?JSON body required}"
    _conto_request PUT "/api/policies/$policy_id/rules" "$body"
    ;;

  add-rule)
    policy_id="${2:?policy_id required}"
    body="${3:?JSON body required}"
    _conto_request POST "/api/policies/$policy_id/rules" "$body"
    ;;

  delete-rule)
    policy_id="${2:?policy_id required}"
    rule_id="${3:?rule_id required}"
    _conto_request DELETE "/api/policies/$policy_id/rules/$rule_id"
    ;;

  setup)
    AGENT_NAME="${2:-hermes-agent}"
    WALLET_ADDRESS="${3:-}"
    CHAIN_TYPE="${4:-EVM}"
    CHAIN_ID="${5:-42431}"

    if [[ -z "$WALLET_ADDRESS" ]]; then
      echo "Usage: conto-check.sh setup <agent_name> <wallet_address> [chain_type] [chain_id]"
      echo ""
      echo "  agent_name:     Name for your agent (default: hermes-agent)"
      echo "  wallet_address: Your wallet address (0x... for EVM, base58 for Solana)"
      echo "  chain_type:     EVM or SOLANA (default: EVM)"
      echo "  chain_id:       Chain ID (default: 42431 for Tempo Testnet)"
      echo "                  Common: 8453 (Base), 42431 (Tempo Testnet), 1 (Ethereum)"
      exit 1
    fi

    # Find a free port
    CALLBACK_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
    TMPFILE=$(mktemp)
    trap "rm -f '$TMPFILE'" EXIT

    # Start temporary HTTP server for callback
    python3 -c "
import http.server, urllib.parse, json, threading

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        sdk_key = params.get('sdkKey', [''])[0]
        agent_id = params.get('agentId', [''])[0]
        org = params.get('org', [''])[0]
        error = params.get('error', [''])[0]
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        if error:
            self.wfile.write(b'<h1>Setup Failed</h1><p>' + error.encode() + b'</p><p>You can close this window.</p>')
            with open('${TMPFILE}', 'w') as f: json.dump({'error': error}, f)
        elif sdk_key:
            self.wfile.write(b'<h1>Agent Connected!</h1><p>You can close this window and return to your terminal.</p>')
            with open('${TMPFILE}', 'w') as f: json.dump({'sdkKey': sdk_key, 'agentId': agent_id, 'org': org}, f)
        else:
            self.wfile.write(b'<h1>Setup Error</h1><p>No SDK key received.</p>')
            with open('${TMPFILE}', 'w') as f: json.dump({'error': 'No SDK key in callback'}, f)
        threading.Thread(target=self.server.shutdown).start()
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', ${CALLBACK_PORT}), Handler)
server.timeout = 300
try: server.handle_request()
except: pass
" &
    SERVER_PID=$!

    # Build setup URL
    ENCODED_NAME=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${AGENT_NAME}'))")
    SETUP_URL="${API_URL}/agent-setup?callback=http://localhost:${CALLBACK_PORT}/callback&name=${ENCODED_NAME}&wallet=${WALLET_ADDRESS}&chainType=${CHAIN_TYPE}&chainId=${CHAIN_ID}"

    echo "Opening browser for Conto agent setup..."
    echo "If the browser doesn't open, visit:"
    echo "  ${SETUP_URL}"
    echo ""

    # Open browser (macOS / Linux)
    if command -v open &>/dev/null; then
      open "$SETUP_URL" 2>/dev/null || true
    elif command -v xdg-open &>/dev/null; then
      xdg-open "$SETUP_URL" 2>/dev/null || true
    fi

    echo "Waiting for approval (timeout: 5 minutes)..."
    wait $SERVER_PID 2>/dev/null || true

    # Read result
    if [[ ! -f "$TMPFILE" ]] || [[ ! -s "$TMPFILE" ]]; then
      echo "Error: Setup timed out or failed"
      exit 1
    fi

    RESULT=$(cat "$TMPFILE")
    ERROR=$(echo "$RESULT" | jq -r '.error // empty')
    if [[ -n "$ERROR" ]]; then
      echo "Error: $ERROR"
      exit 1
    fi

    SDK_KEY_VALUE=$(echo "$RESULT" | jq -r '.sdkKey')
    AGENT_ID=$(echo "$RESULT" | jq -r '.agentId')
    ORG_NAME=$(echo "$RESULT" | jq -r '.org')

    if [[ -z "$SDK_KEY_VALUE" || "$SDK_KEY_VALUE" == "null" ]]; then
      echo "Error: No SDK key received"
      exit 1
    fi

    # Write to ~/.hermes/.env
    HERMES_ENV="$HOME/.hermes/.env"
    mkdir -p "$(dirname "$HERMES_ENV")"

    # Update or append CONTO_SDK_KEY and CONTO_API_URL in .env
    if [[ -f "$HERMES_ENV" ]]; then
      # Remove existing Conto entries
      grep -v '^CONTO_SDK_KEY=' "$HERMES_ENV" | grep -v '^CONTO_API_URL=' > "${HERMES_ENV}.tmp" || true
      mv "${HERMES_ENV}.tmp" "$HERMES_ENV"
    fi
    echo "CONTO_SDK_KEY=$SDK_KEY_VALUE" >> "$HERMES_ENV"
    echo "CONTO_API_URL=$API_URL" >> "$HERMES_ENV"

    # Verify connection
    echo ""
    echo "Verifying connection..."
    VERIFY_RESPONSE=$(curl -sS -w "\n%{http_code}" \
      -H "Authorization: Bearer $SDK_KEY_VALUE" \
      "${API_URL}/api/sdk/setup" 2>/dev/null || echo "000")
    VERIFY_CODE=$(echo "$VERIFY_RESPONSE" | tail -1)

    if [[ "$VERIFY_CODE" == "200" ]]; then
      echo ""
      echo "Agent setup complete."
      echo "  Agent:        $AGENT_NAME ($AGENT_ID)"
      echo "  Organization: $ORG_NAME"
      echo "  Wallet:       $WALLET_ADDRESS"
      echo "  SDK Key:      ${SDK_KEY_VALUE:0:16}..."
      echo "  Config:       $HERMES_ENV"
      echo ""
      echo "Test it: $(dirname "$0")/conto-check.sh budget"
    else
      echo ""
      echo "SDK key saved but verification returned HTTP $VERIFY_CODE."
      echo "The key may need a moment to activate. Try:"
      echo "  $(dirname "$0")/conto-check.sh budget"
    fi
    ;;

  help|*)
    cat <<USAGE
Conto Policy Check & Management — Hermes Helper

Setup:
  setup         <name> <wallet> [chain_type] [chain_id]  Auto-setup via browser

Payment Commands (standard SDK key):
  approve       <amount> <recipient> <sender> <chain_id> [purpose] [category]
  confirm       <approval_id> <tx_hash> <approval_token>
  x402          <amount> <recipient> <resource_url> [facilitator] [scheme]
  budget        Check remaining x402 budget and burn rate
  services      List x402 services this agent has used

Policy Commands (requires admin SDK key):
  policies                          List all policies
  policy        <id>                Get a single policy with rules
  create-policy <json>              Create a new policy
  update-policy <id> <json>         Update policy name/priority/active
  delete-policy <id>                Delete a policy
  get-rules     <policy_id>         List rules for a policy
  set-rules     <policy_id> <json>  Replace all rules on a policy
  add-rule      <policy_id> <json>  Add a rule to a policy
  delete-rule   <policy_id> <rule_id>  Delete a single rule

Environment:
  CONTO_SDK_KEY   (required) Your Conto SDK API key
  CONTO_API_URL   (optional) API base URL, default: https://conto.finance

Examples:
  # Set up a new agent (opens browser for approval)
  conto-check.sh setup my-agent 0x80Ca... EVM 42431

  # Check policy before payment (chain_id: 8453=Base, 42431=Tempo Testnet)
  conto-check.sh approve 50 0xabc... 0x123... 8453 "Pay for API" API_PROVIDER

  # List policies
  conto-check.sh policies

  # Create a \$200 per-tx limit policy
  conto-check.sh create-policy '{"name":"Max \$200","policyType":"SPEND_LIMIT","priority":10,"isActive":true,"rules":[{"ruleType":"MAX_AMOUNT","operator":"LTE","value":"200","action":"ALLOW"}]}'

  # Block an address
  conto-check.sh create-policy '{"name":"Blocklist","policyType":"COUNTERPARTY","priority":50,"isActive":true,"rules":[{"ruleType":"BLOCKED_COUNTERPARTIES","operator":"IN_LIST","value":"[\"0xbad...\"]","action":"DENY"}]}'

  # Add a rule to existing policy
  conto-check.sh add-rule cmm59z... '{"ruleType":"DAILY_LIMIT","operator":"LTE","value":"1000","action":"ALLOW"}'
USAGE
    ;;
esac
