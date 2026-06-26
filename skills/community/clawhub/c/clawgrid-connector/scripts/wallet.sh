#!/usr/bin/env bash
set -euo pipefail

# Manage wallet and payouts.
#
# Usage:
#   bash wallet.sh status                     — view wallet info & pending earnings
#   bash wallet.sh bind <solana_address>      — bind a Solana wallet
#   bash wallet.sh payout [amount]            — request payout (omit amount = withdraw all)

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"

if [ $# -lt 1 ]; then
  echo "Usage:" >&2
  echo "  bash $0 status                    — view wallet info" >&2
  echo "  bash $0 bind <solana_address>     — bind Solana wallet" >&2
  echo "  bash $0 payout [amount]           — request payout" >&2
  exit 1
fi

CMD="$1"
shift

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: Config not found at $CONFIG" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

case "$CMD" in
  status)
    RESP=$(curl -s -w "\n%{http_code}" \
      "$API_BASE/api/lobster/wallet" \
      -H "Authorization: Bearer $API_KEY" \
      --max-time 15)
    ;;

  bind)
    if [ $# -lt 1 ]; then
      echo "ERROR: Missing Solana wallet address" >&2
      echo "Usage: bash $0 bind <solana_address>" >&2
      exit 1
    fi
    WALLET_ADDR="$1"
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/wallet/bind" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"wallet_address\": \"$WALLET_ADDR\"}" \
      --max-time 15)
    ;;

  payout)
    AMOUNT="${1:-}"
    if [ -n "$AMOUNT" ]; then
      REQ_BODY="{\"amount\": $AMOUNT}"
    else
      REQ_BODY="{}"
    fi
    RESP=$(curl -s -w "\n%{http_code}" -X POST \
      "$API_BASE/api/lobster/payout/request" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "$REQ_BODY" \
      --max-time 15)
    ;;

  *)
    echo "Unknown command: $CMD" >&2
    echo "Valid commands: status, bind, payout" >&2
    exit 1
    ;;
esac

HTTP_CODE=$(echo "$RESP" | tail -1)
BODY=$(echo "$RESP" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY"
  exit 0
else
  echo "Wallet $CMD failed (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi
