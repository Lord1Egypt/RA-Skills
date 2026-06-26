#!/usr/bin/env bash
# conto-check.sh — Conto policy check & management helper for OpenClaw
#
# Payment commands (standard SDK key):
#   conto-check.sh approve <amount> <recipient> <sender> [purpose] [category] [chain_id]
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
SDK_KEY="${CONTO_SDK_KEY:?CONTO_SDK_KEY is required}"

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
    purpose="${5:-}"
    category="${6:-}"
    chain_id="${7:-42431}"

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

  help|*)
    cat <<USAGE
Conto Policy Check & Management — OpenClaw Helper

Payment Commands (standard SDK key):
  approve       <amount> <recipient> <sender> [purpose] [category] [chain_id]
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
  # Check policy before payment
  conto-check.sh approve 50 0xabc... 0x123... "Pay for API" API_PROVIDER

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
