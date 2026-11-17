#!/usr/bin/env bash
# conto-check.sh — Conto policy check & management helper for OpenClaw
#
# Setup:
#   conto-check.sh setup <agent_name> <wallet_address> [chain_type] [chain_id]
#
# Payment commands (standard SDK key):
#   conto-check.sh approve <amount> <recipient> <sender> <chain_id> [purpose] [category]
#   conto-check.sh confirm <payment_request_id> <tx_hash> [approval_token]
#   conto-check.sh pending-approvals
#   conto-check.sh approve-request <approval_request_id> <human_action_token> [comment]
#   conto-check.sh deny-request <approval_request_id> <human_action_token> [comment]
#   conto-check.sh x402 <amount> <recipient> <resource_url> [session_id] [payment_id]
#   conto-check.sh x402-record <amount> <recipient> <resource_url> <payment_id> <tx_hash> <grant_id> <grant_signature> [session_id]
#   conto-check.sh budget [session_id]
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
    payment_request_id="${2:?paymentRequestId required}"
    tx_hash="${3:?txHash required}"
    approval_token="${4:-}"

    payload=$(jq -n --arg txHash "$tx_hash" --arg approvalToken "$approval_token" \
      '{txHash: $txHash} + (if $approvalToken == "" then {} else {approvalToken: $approvalToken} end)')
    _conto_request POST "/api/sdk/payments/$payment_request_id/confirm" "$payload"
    ;;

  pending-approvals)
    _conto_request GET "/api/sdk/approval-requests?type=payment&status=PENDING"
    ;;

  approve-request)
    approval_request_id="${2:?approvalRequestId required}"
    action_token="${3:?humanActionToken required}"
    comment="${4:-}"

    payload=$(jq -n --arg decision "APPROVED" --arg actionToken "$action_token" --arg comment "$comment" \
      '{decision: $decision, actionToken: $actionToken} + (if $comment == "" then {} else {comment: $comment} end)')
    _conto_request POST "/api/sdk/approval-requests/$approval_request_id/decide" "$payload"
    ;;

  deny-request)
    approval_request_id="${2:?approvalRequestId required}"
    action_token="${3:?humanActionToken required}"
    comment="${4:-}"

    payload=$(jq -n --arg decision "REJECTED" --arg actionToken "$action_token" --arg comment "$comment" \
      '{decision: $decision, actionToken: $actionToken} + (if $comment == "" then {} else {comment: $comment} end)')
    _conto_request POST "/api/sdk/approval-requests/$approval_request_id/decide" "$payload"
    ;;

  x402)
    amount="${2:?amount required}"
    recipient="${3:?recipientAddress required}"
    resource_url="${4:?resourceUrl required}"
    session_id="${5:-}"
    payment_id="${6:-}"

    payload=$(jq -n \
      --argjson amount "$amount" \
      --arg recipientAddress "$recipient" \
      --arg resourceUrl "$resource_url" \
      --arg sessionId "$session_id" \
      --arg paymentId "$payment_id" \
      '{amount: $amount, recipientAddress: $recipientAddress, resourceUrl: $resourceUrl}
       + (if $sessionId == "" then {} else {sessionId: $sessionId} end)
       + (if $paymentId == "" then {} else {paymentId: $paymentId} end)')
    _conto_request POST /api/sdk/x402/pre-authorize "$payload"
    ;;

  x402-record)
    # Records a settled x402 payment with the grant from the approved pre-authorize.
    # The grant is required here: a record without one is flagged as a policy bypass.
    amount="${2:?amount required}"
    recipient="${3:?recipientAddress required}"
    resource_url="${4:?resourceUrl required}"
    payment_id="${5:?paymentId required (reuse the same value when retrying)}"
    tx_hash="${6:?txHash required}"
    grant_id="${7:?grantId required (from the approved x402 pre-authorize)}"
    grant_signature="${8:?grantSignature required (from the approved x402 pre-authorize)}"
    session_id="${9:-}"

    payload=$(jq -n \
      --argjson amount "$amount" \
      --arg recipientAddress "$recipient" \
      --arg resourceUrl "$resource_url" \
      --arg paymentId "$payment_id" \
      --arg txHash "$tx_hash" \
      --arg grantId "$grant_id" \
      --arg grantSignature "$grant_signature" \
      --arg sessionId "$session_id" \
      '{amount: $amount, recipientAddress: $recipientAddress, resourceUrl: $resourceUrl,
        paymentId: $paymentId, txHash: $txHash, grantId: $grantId, grantSignature: $grantSignature}
       + (if $sessionId == "" then {} else {sessionId: $sessionId} end)')
    _conto_request POST /api/sdk/x402/record "$payload"
    ;;

  budget)
    session_id="${2:-}"
    if [[ -n "$session_id" ]]; then
      encoded_session_id=$(jq -rn --arg value "$session_id" '$value|@uri')
      _conto_request GET "/api/sdk/x402/budget?sessionId=$encoded_session_id"
    else
      _conto_request GET /api/sdk/x402/budget
    fi
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
    AGENT_NAME="${2:-openclaw-agent}"
    WALLET_ADDRESS="${3:-}"
    CHAIN_TYPE="${4:-EVM}"
    CHAIN_ID="${5:-42431}"

    if [[ -z "$WALLET_ADDRESS" ]]; then
      echo "Usage: conto-check.sh setup <agent_name> <wallet_address> [chain_type] [chain_id]"
      echo ""
      echo "  agent_name:     Name for your agent (default: openclaw-agent)"
      echo "  wallet_address: Your wallet address (0x... for EVM, base58 for Solana)"
      echo "  chain_type:     EVM or SOLANA (default: EVM)"
      echo "  chain_id:       Chain ID (default: 42431 for Tempo Testnet)"
      echo "                  Common: 8453 (Base), 42431 (Tempo Testnet), 1 (Ethereum)"
      exit 1
    fi

    # Find a free port
    CALLBACK_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')
    CALLBACK_STATE=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
    TMPFILE=$(mktemp)
    trap "rm -f '$TMPFILE'" EXIT

    # Start temporary HTTP server for callback
    python3 -c "
import http.server, urllib.parse, json, time

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != '/callback':
            self.send_response(404)
            self.end_headers()
            return
        params = urllib.parse.parse_qs(parsed.query)
        state = params.get('state', [''])[0]
        sdk_key = params.get('sdkKey', [''])[0]
        agent_id = params.get('agentId', [''])[0]
        org = params.get('org', [''])[0]
        error = params.get('error', [''])[0]
        if state != '${CALLBACK_STATE}':
            self.send_response(400)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Setup Failed</h1><p>Invalid setup state.</p><p>Please retry the setup command.</p>')
            return
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
        self.server.done = True
    def log_message(self, *a): pass

server = http.server.HTTPServer(('127.0.0.1', ${CALLBACK_PORT}), Handler)
server.timeout = 1
server.done = False
deadline = time.time() + 300
try:
    while not server.done and time.time() < deadline:
        server.handle_request()
except: pass
" &
    SERVER_PID=$!

    # Build setup URL
    ENCODED_NAME=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${AGENT_NAME}'))")
    SETUP_URL="${API_URL}/agent-setup?callback=http://127.0.0.1:${CALLBACK_PORT}/callback&state=${CALLBACK_STATE}&name=${ENCODED_NAME}&wallet=${WALLET_ADDRESS}&chainType=${CHAIN_TYPE}&chainId=${CHAIN_ID}"

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

    # Write to openclaw.json
    OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
    mkdir -p "$(dirname "$OPENCLAW_CONFIG")"

    if [[ -f "$OPENCLAW_CONFIG" ]]; then
      UPDATED=$(jq --arg key "$SDK_KEY_VALUE" --arg url "$API_URL" \
        '.skills.entries.conto.env.CONTO_SDK_KEY = $key | .skills.entries.conto.env.CONTO_API_URL = $url' \
        "$OPENCLAW_CONFIG")
      echo "$UPDATED" > "$OPENCLAW_CONFIG"
    else
      jq -n --arg key "$SDK_KEY_VALUE" --arg url "$API_URL" \
        '{skills: {entries: {conto: {env: {CONTO_SDK_KEY: $key, CONTO_API_URL: $url}}}}}' \
        > "$OPENCLAW_CONFIG"
    fi

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
      echo "  Config:       $OPENCLAW_CONFIG"
      echo ""
      echo "Test it: bash $(dirname "$0")/conto-check.sh budget"
    else
      echo ""
      echo "SDK key saved but verification returned HTTP $VERIFY_CODE."
      echo "The key may need a moment to activate. Try:"
      echo "  bash $(dirname "$0")/conto-check.sh budget"
    fi
    ;;

  help|*)
    cat <<USAGE
Conto Policy Check & Management — OpenClaw Helper

Setup:
  setup         <name> <wallet> [chain_type] [chain_id]  Auto-setup via browser

Payment Commands (standard SDK key):
  approve       <amount> <recipient> <sender> <chain_id> [purpose] [category]
  confirm       <payment_request_id> <tx_hash> [approval_token]
  pending-approvals                  List payments awaiting human review
  approve-request <approval_request_id> <human_action_token> [comment]  Approve a pending payment
  deny-request    <approval_request_id> <human_action_token> [comment]  Deny a pending payment
  x402          <amount> <recipient> <resource_url> [session_id] [payment_id]
  x402-record   <amount> <recipient> <resource_url> <payment_id> <tx_hash> <grant_id> <grant_signature> [session_id]
  budget        [session_id]  Check aggregate or session-specific x402 spend
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
  bash conto-check.sh setup my-agent 0x80Ca... EVM 42431

  # Check policy before payment (chain_id: 8453=Base, 42431=Tempo Testnet)
  bash conto-check.sh approve 50 0xabc... 0x123... 8453 "Pay for API" API_PROVIDER

  # Review and approve a payment from OpenClaw
  bash conto-check.sh pending-approvals
  bash conto-check.sh approve-request cmrApproval... HUMAN_ACTION_TOKEN "Approved by the owner"

  # List policies
  bash conto-check.sh policies

  # Create a \$200 per-tx limit policy
  bash conto-check.sh create-policy '{"name":"Max \$200","policyType":"SPEND_LIMIT","priority":10,"isActive":true,"rules":[{"ruleType":"MAX_AMOUNT","operator":"LTE","value":"200","action":"ALLOW"}]}'

  # Block an address
  bash conto-check.sh create-policy '{"name":"Blocklist","policyType":"COUNTERPARTY","priority":50,"isActive":true,"rules":[{"ruleType":"BLOCKED_COUNTERPARTIES","operator":"IN_LIST","value":"[\"0xbad...\"]","action":"DENY"}]}'

  # Add a rule to existing policy
  bash conto-check.sh add-rule cmm59z... '{"ruleType":"DAILY_LIMIT","operator":"LTE","value":"1000","action":"ALLOW"}'
USAGE
    ;;
esac
