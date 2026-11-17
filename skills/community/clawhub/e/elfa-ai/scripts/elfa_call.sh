#!/usr/bin/env bash
# elfa_call.sh — Make authenticated Elfa API calls from the command line.
#
# Supports two auth modes:
#   API key:  Set ELFA_API_KEY in the environment (default).
#   x402:     Pass --x402 with a pre-signed payment header via --payment.
#
# Supports Auto endpoints with HMAC signing (conditional per route):
#   --hmac-secret  HMAC secret. Required for exchange linking; optional for
#                  query lifecycle routes (signed if provided, allowed without
#                  for notification-only EQL actions).
#   --agent-secret Agent identity secret for x402 Auto requests.
#
# Usage:
#   ./elfa_call.sh <endpoint> [options]
#
# Examples:
#   ./elfa_call.sh /v2/ping
#   ./elfa_call.sh /v2/aggregations/trending-tokens -q 'timeWindow=24h&pageSize=10'
#   ./elfa_call.sh /v2/data/top-mentions -q 'ticker=$SOL&timeWindow=24h'
#   ./elfa_call.sh /v2/chat -d '{"message":"What is trending?","analysisType":"chat"}'
#   ./elfa_call.sh /v2/aggregations/trending-tokens --x402 --payment '<base64-payload>'

set -euo pipefail

BASE_URL="https://api.elfa.ai"

usage() {
  cat <<'EOF'
elfa_call.sh — Make authenticated Elfa API calls from the command line.

Supports two auth modes:
  API key:  Set ELFA_API_KEY in the environment (default).
  x402:     Pass --x402 with a pre-signed payment header via --payment.

Usage:
  ./elfa_call.sh <endpoint> [options]

Options:
  -q, --query <params>        Query string (e.g. 'timeWindow=24h&pageSize=10')
  -X, --method <METHOD>       HTTP method (default: GET, auto-set to POST with -d)
  -d, --data <json>           Request body (JSON). Implies -X POST.
  --x402                      Use x402 keyless mode (rewrites /v2/ to /x402/v2/).
  --payment <payload>         Pre-signed x402 payment header (base64). Requires --x402.
  --hmac-secret <secret>      HMAC secret for Auto mutation endpoints (POST/DELETE on
                              /v2/auto/). Can also be set via ELFA_HMAC_SECRET env var.
  --agent-secret <secret>     Agent identity secret added as x-elfa-agent-secret header
                              when using --x402 with Auto endpoints. Can also be set via
                              ELFA_AGENT_SECRET env var.
  -h, --help                  Show this help

Auto endpoint HMAC signing:
  HMAC behavior is determined per route. When the script signs a request, it
  adds these headers automatically:

    x-elfa-timestamp: <unix_seconds>
    x-elfa-signature: <hex_hmac_sha256>

  The signature payload is: timestamp + METHOD + mounted_path + body
  where mounted_path is the portion of the path AFTER the mount (/v2/auto or
  /v2/trade).
  Example: /v2/auto/queries  →  mounted_path = /queries
           /v2/auto/queries/q_123  →  mounted_path = /queries/q_123
           /v2/trade/orders  →  mounted_path = /orders
           /v2/trade/positions/close  →  mounted_path = /positions/close

  HMAC always required (script will refuse to call without --hmac-secret):
    POST   /v2/auto/exchanges                            (connect — trade gateway)
    DELETE /v2/auto/exchanges/{exchange}                 (disconnect — trade gateway)
    POST   /v2/trade/orders                              (place order)
    POST   /v2/trade/orders/cancel                       (cancel resting order)
    POST   /v2/trade/orders/modify                       (modify resting order)
    POST   /v2/trade/positions/close                     (close position)
    POST   /v2/trade/positions/tpsl                      (set take-profit/stop-loss)

  HMAC conditional (signed if --hmac-secret is provided; allowed without for
  notification-only EQL actions like notify / telegram_bot / webhook):
    POST   /v2/auto/queries                              (create)
    POST   /v2/auto/queries/{queryId}/cancel             (cancel active query)
    DELETE /v2/auto/queries/{queryId}                    (delete terminal query)
    POST   /v2/auto/queries/drafts                       (upsert draft)
    POST   /v2/auto/queries/drafts/{draftId}/convert     (draft → active query)

  Cancel and delete are distinct operations:
    - POST /cancel: only on active queries (returns 409 if terminal)
    - DELETE: only on terminal queries — triggered/expired/cancelled/failed
      (returns 409 if active; you must cancel first)

  HMAC never required (signing is skipped even if --hmac-secret is set):
    POST   /v2/auto/chat                                 (Builder Chat — produces drafts only)
    POST   /v2/auto/queries/validate                     (free, no side effects)
    POST   /v2/auto/queries/preview                      (free, no side effects)
    DELETE /v2/auto/queries/drafts/{draftId}             (discard draft)
    POST   /v2/auto/queries/drafts/{draftId}/preview     (preview stored draft)
    POST   /v2/trade/orders/preview                      (dry-run order — free)
    POST   /v2/trade/positions/close/preview             (dry-run close — free)
    POST   /v2/trade/positions/tpsl/preview              (dry-run TP/SL — free)

  Note: For "conditional" routes, the API server enforces HMAC only when the
  EQL action is trade-flavoured (market_order, limit_order, or llm callback to
  those). Notification-only actions (notify, telegram_bot, webhook, llm
  callback to those) are accepted unsigned. If you receive a 401 for a route
  that should accept notification actions, double-check your action payload.
  Always-signing remains safe — signed requests are accepted on every route.

Examples:
  # API key mode (reads ELFA_API_KEY from env)
  ./elfa_call.sh /v2/ping
  ./elfa_call.sh /v2/aggregations/trending-tokens -q 'timeWindow=24h&pageSize=10'
  ./elfa_call.sh /v2/chat -d '{"message":"What is trending?","analysisType":"chat"}'

  # x402 mode (pay-per-request with USDC on Base)
  ./elfa_call.sh /v2/aggregations/trending-tokens --x402 --payment '<base64-payload>'

  # Auto: validate a query (no HMAC needed)
  ./elfa_call.sh /v2/auto/queries/validate -d '{"query":{...}}'

  # Auto: preview a query without creating it (no HMAC needed)
  ./elfa_call.sh /v2/auto/queries/preview -d '{"query":{...}}'

  # Auto: Builder Chat (no HMAC needed — produces drafts only)
  ./elfa_call.sh /v2/auto/chat -d '{"message":"Alert me when BTC breaks 100k"}'

  # Auto: create a query with notification action (HMAC OPTIONAL — runs without secret)
  ./elfa_call.sh /v2/auto/queries -d '{"query":{"actions":[{"type":"notify",...}],...}}'

  # Auto: create a query with trade action (HMAC required — server returns 401 without it)
  ./elfa_call.sh /v2/auto/queries -d '{"query":{"actions":[{"type":"market_order",...}],...}}' --hmac-secret "$ELFA_HMAC_SECRET"

  # Auto: cancel an active query (HMAC OPTIONAL — depends on stored query's action type)
  ./elfa_call.sh /v2/auto/queries/q_123/cancel -X POST

  # Auto: delete a terminal query (HMAC OPTIONAL — depends on stored query's action type)
  ./elfa_call.sh /v2/auto/queries/q_123 -X DELETE  # only after status is terminal

  # Auto: upsert a draft (HMAC OPTIONAL — depends on body's action type)
  ./elfa_call.sh /v2/auto/queries/drafts -d '{"query":{...}}'

  # Auto: convert a draft to active query (HMAC OPTIONAL — depends on stored draft's action type)
  ./elfa_call.sh /v2/auto/queries/drafts/d_123/convert -X POST

  # Auto: list executions
  ./elfa_call.sh /v2/auto/executions

  # Auto: connect an exchange (HMAC ALWAYS required — trade gateway)
  ./elfa_call.sh /v2/auto/exchanges -d '{"exchange":"hyperliquid",...}' --hmac-secret "$ELFA_HMAC_SECRET"

  # Trade: preview an order (free, no HMAC — dry-run)
  ./elfa_call.sh /v2/trade/orders/preview -d '{"exchange":"hyperliquid","symbol":"BTC","side":"buy","orderType":"market","amount":"25"}'

  # Trade: place an order (HMAC ALWAYS required — signs mounted path /orders)
  ./elfa_call.sh /v2/trade/orders -d '{"exchange":"hyperliquid","symbol":"BTC","side":"buy","orderType":"market","amount":"25"}' --hmac-secret "$ELFA_HMAC_SECRET"

  # Trade: close a position (HMAC ALWAYS required — signs mounted path /positions/close)
  ./elfa_call.sh /v2/trade/positions/close -d '{"exchange":"hyperliquid","symbol":"BTC","orderType":"market","closePercent":100}' --hmac-secret "$ELFA_HMAC_SECRET"

  # Auto x402: create query with agent secret
  ./elfa_call.sh /v2/auto/queries --x402 --payment '<payload>' --agent-secret "$ELFA_AGENT_SECRET"
EOF
  exit 0
}

die() { echo "error: $1" >&2; exit 1; }

# Format JSON — prefer jq, fall back to python3
fmt_json() {
  if command -v jq &>/dev/null; then
    jq .
  elif command -v python3 &>/dev/null; then
    python3 -m json.tool
  else
    cat
  fi
}

# Parse arguments
METHOD="GET"
QUERY=""
BODY=""
X402=false
PAYMENT=""
HMAC_SECRET="${ELFA_HMAC_SECRET:-}"
AGENT_SECRET="${ELFA_AGENT_SECRET:-}"

[[ $# -eq 0 ]] && usage
[[ "$1" == "-h" || "$1" == "--help" ]] && usage

ENDPOINT="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    -X|--method)        [[ $# -lt 2 ]] && die "-X requires a value"; METHOD="$2"; shift 2 ;;
    -q|--query)         [[ $# -lt 2 ]] && die "-q requires a value"; QUERY="$2"; shift 2 ;;
    -d|--data)          [[ $# -lt 2 ]] && die "-d requires a value"; BODY="$2"; METHOD="POST"; shift 2 ;;
    --x402)             X402=true; shift ;;
    --payment)          [[ $# -lt 2 ]] && die "--payment requires a value"; PAYMENT="$2"; shift 2 ;;
    --hmac-secret)      [[ $# -lt 2 ]] && die "--hmac-secret requires a value"; HMAC_SECRET="$2"; shift 2 ;;
    --agent-secret)     [[ $# -lt 2 ]] && die "--agent-secret requires a value"; AGENT_SECRET="$2"; shift 2 ;;
    -h|--help)          usage ;;
    *)                  die "unknown option: $1" ;;
  esac
done

# Normalize method to uppercase (use tr for bash 3.x / macOS compat)
METHOD=$(printf '%s' "$METHOD" | tr '[:lower:]' '[:upper:]')

# Validate
[[ "$ENDPOINT" == /* ]] || die "endpoint must start with / (e.g. /v2/ping)"

if [[ "$X402" == true ]]; then
  # Rewrite /v2/ → /x402/v2/ if not already prefixed
  [[ "$ENDPOINT" == /v2/* ]] && ENDPOINT="/x402${ENDPOINT}"
  [[ -n "$PAYMENT" ]] || die "--x402 requires --payment <payload>. See https://docs.elfa.ai/x402-payments"
else
  [[ -z "${ELFA_API_KEY:-}" ]] && die "ELFA_API_KEY is not set. Get a free key at https://go.elfa.ai/claude-skills"
fi

# Determine HMAC behavior for this Auto request. Tri-state:
#
#   none         — never sign (read-only, validate/preview, /chat ungated routes)
#   conditional  — sign IF an HMAC secret is available; allow request through
#                  without HMAC otherwise. Per the docs, the server bypasses HMAC
#                  for notification-only EQL actions (notify / telegram_bot /
#                  webhook / llm-callback-to-those) and enforces HMAC for trade
#                  actions (market_order / limit_order / llm-callback-to-those).
#                  Always-signing remains safe — signed requests are accepted
#                  on every route.
#   required     — must have an HMAC secret; refuse to call without one. Used
#                  for exchange linking (POST/DELETE /exchanges) which always
#                  needs HMAC, and for all Trade (/v2/trade) write routes.
#
# We check the *original* endpoint (before x402 rewrite) by examining whether
# the path contains /auto/ or /trade/ and the method is POST or DELETE.
HMAC_BEHAVIOR="none"
IS_AUTO_ENDPOINT=false
# Use the original endpoint for detection (strip /x402 prefix if present)
ORIGINAL_ENDPOINT="${ENDPOINT#/x402}"
if [[ "$ORIGINAL_ENDPOINT" == /v2/trade/* ]]; then
  # Trade (direct execution): writes always require HMAC; previews never do.
  # mounted_path is relative to /v2/trade (e.g. /orders), NOT /v2/auto.
  if [[ "$METHOD" == "POST" ]]; then
    case "${ORIGINAL_ENDPOINT#/v2/trade}" in
      */preview)                  ;;  # previews are free, unsigned
      /orders|/orders/cancel|/orders/modify|/positions/close|/positions/tpsl)
                                  HMAC_BEHAVIOR="required" ;;  # writes always signed
      *)                          HMAC_BEHAVIOR="required" ;;  # unknown write — fail-safe
    esac
  fi
elif [[ "$ORIGINAL_ENDPOINT" == /v2/auto/* ]]; then
  IS_AUTO_ENDPOINT=true
  if [[ "$METHOD" == "POST" || "$METHOD" == "DELETE" ]]; then
    MOUNTED_CHECK="${ORIGINAL_ENDPOINT#/v2/auto}"
    # NOTE: bash case is first-match-wins. Order matters — more-specific
    # patterns must come before catch-all globs.
    case "$MOUNTED_CHECK" in
      # Never HMAC
      /chat)                        ;;  # ungated — produces drafts only
      /queries/validate)            ;;  # free, no side effects
      /queries/preview)             ;;  # free, no side effects
      /queries/drafts/*/preview)    ;;  # preview a stored draft
      /queries/drafts/*/convert)    HMAC_BEHAVIOR="conditional" ;;  # convert depends on stored draft action
      /queries/drafts/*)            ;;  # GET/DELETE specific draft (no side effects)
      /queries/drafts)              HMAC_BEHAVIOR="conditional" ;;  # POST upsert depends on body action
      /queries/*/cancel)            HMAC_BEHAVIOR="conditional" ;;  # POST cancel depends on stored query action
      /queries/*)                   HMAC_BEHAVIOR="conditional" ;;  # DELETE /queries/:id (delete terminal query — only on triggered/expired/cancelled/failed)
      /queries)                     HMAC_BEHAVIOR="conditional" ;;  # POST create depends on body action
      /exchanges)                   HMAC_BEHAVIOR="required" ;;  # POST connect: trade gateway
      /exchanges/*)                 HMAC_BEHAVIOR="required" ;;  # DELETE disconnect: trade gateway
      *)                            HMAC_BEHAVIOR="required" ;;  # unknown route — fail-safe
    esac
  fi
fi

# Build URL
URL="${BASE_URL}${ENDPOINT}"
[[ -n "$QUERY" ]] && URL="${URL}?${QUERY}"

# Build curl args
CURL_ARGS=(-s --fail-with-body --max-time 30 -X "$METHOD")

if [[ "$X402" == true ]]; then
  CURL_ARGS+=(-H "X-PAYMENT: ${PAYMENT}")
  # Add agent-secret header only for x402 Auto requests when provided
  if [[ -n "$AGENT_SECRET" ]] && [[ "$IS_AUTO_ENDPOINT" == true ]]; then
    CURL_ARGS+=(-H "x-elfa-agent-secret: ${AGENT_SECRET}")
  fi
else
  CURL_ARGS+=(-H "x-elfa-api-key: ${ELFA_API_KEY}")
fi

if [[ -n "$BODY" ]]; then
  CURL_ARGS+=(-H "Content-Type: application/json" -d "$BODY")
fi

# x402 Auto never uses API-key HMAC; it uses payment headers + x-elfa-agent-secret.
[[ "$X402" == true ]] && HMAC_BEHAVIOR="none"

# HMAC signing for Auto endpoints (tri-state — see HMAC_BEHAVIOR comment above)
SHOULD_SIGN=false
case "$HMAC_BEHAVIOR" in
  required)
    if [[ -z "$HMAC_SECRET" ]]; then
      die "${METHOD} ${ORIGINAL_ENDPOINT} always requires HMAC (Trade write / exchange linking). Set ELFA_HMAC_SECRET in your environment or pass --hmac-secret <secret>."
    fi
    SHOULD_SIGN=true
    ;;
  conditional)
    # Sign if a secret is available (always-safe). Skip otherwise — the server
    # accepts unsigned requests for notification-only EQL actions and will
    # return 401 for trade-action requests. If you hit a 401 here, set
    # ELFA_HMAC_SECRET (or pass --hmac-secret) and retry.
    [[ -n "$HMAC_SECRET" ]] && SHOULD_SIGN=true
    ;;
esac

if [[ "$SHOULD_SIGN" == true ]]; then
  # Extract mounted_path: strip the mount prefix (/v2/auto or /v2/trade) from
  # the original endpoint. The signed path is relative to the mount.
  if [[ "$ORIGINAL_ENDPOINT" == /v2/trade/* ]]; then
    MOUNTED_PATH="${ORIGINAL_ENDPOINT#/v2/trade}"
  else
    MOUNTED_PATH="${ORIGINAL_ENDPOINT#/v2/auto}"
  fi
  # Ensure mounted_path starts with /
  [[ "$MOUNTED_PATH" == /* ]] || MOUNTED_PATH="/${MOUNTED_PATH}"

  TIMESTAMP=$(date +%s)
  SIGN_PAYLOAD="${TIMESTAMP}${METHOD}${MOUNTED_PATH}${BODY}"
  SIGNATURE=$(printf '%s' "$SIGN_PAYLOAD" | openssl dgst -sha256 -hmac "$HMAC_SECRET" | sed 's/^.* //')

  CURL_ARGS+=(-H "x-elfa-timestamp: ${TIMESTAMP}")
  CURL_ARGS+=(-H "x-elfa-signature: ${SIGNATURE}")
fi

# Execute
HTTP_BODY=$(curl "${CURL_ARGS[@]}" -w '\n%{http_code}' "$URL") || true

HTTP_CODE=$(echo "$HTTP_BODY" | tail -n1)
RESPONSE=$(echo "$HTTP_BODY" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]] 2>/dev/null; then
  echo "$RESPONSE" | fmt_json
else
  echo "HTTP $HTTP_CODE" >&2
  echo "$RESPONSE" | fmt_json >&2
  exit 1
fi
