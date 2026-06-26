#!/usr/bin/env bash
echo "DEPRECATED: This skill is no longer maintained. Use x402janus skill instead." && exit 1

# guardian-subscribe.sh — Subscribe a wallet to x402janus monitoring
# Usage: guardian-subscribe.sh <wallet_address> [--telegram <chat_id>] [--discord <webhook_url>] [--email <addr>]
#
# Env:
#   GUARDIAN_SESSION_TOKEN   Auth token (from guardian auth flow)
#   API_BASE                 Override API base (default: https://www.x402pulse.xyz)
set -euo pipefail

API_BASE="${API_BASE:-https://www.x402pulse.xyz}"
WALLET=""
TELEGRAM=""
DISCORD=""
EMAIL=""
SESSION_TOKEN="${GUARDIAN_SESSION_TOKEN:-}"

usage() {
  cat >&2 <<EOF
Usage: $0 <wallet_address> [--telegram <chat_id>] [--discord <webhook_url>] [--email <addr>]

At least one alert channel (telegram, discord, or email) is required.

Env:
  GUARDIAN_SESSION_TOKEN   Auth session token
  API_BASE                 Override API base (default: $API_BASE)

Example:
  $0 0xYourWallet --telegram -1001234567890
  $0 0xYourWallet --discord https://discord.com/api/webhooks/...
EOF
}

for dep in curl jq; do
  if ! command -v "$dep" &>/dev/null; then
    echo "Error: '$dep' is required but not installed." >&2; exit 1
  fi
done

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then usage; exit 0; fi

WALLET="$1"; shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --telegram) TELEGRAM="$2"; shift 2 ;;
    --discord)  DISCORD="$2";  shift 2 ;;
    --email)    EMAIL="$2";    shift 2 ;;
    -h|--help)  usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ ! "$WALLET" =~ ^0x[a-fA-F0-9]{40}$ ]]; then
  echo "Error: Invalid wallet address: $WALLET" >&2; exit 1
fi

if [[ -z "$TELEGRAM" && -z "$DISCORD" && -z "$EMAIL" ]]; then
  echo "Error: At least one alert channel required (--telegram, --discord, or --email)" >&2
  usage; exit 1
fi

# Build JSON payload
PAYLOAD=$(jq -n \
  --arg wallet "$WALLET" \
  --arg telegram "$TELEGRAM" \
  --arg discord "$DISCORD" \
  --arg email "$EMAIL" \
  '{
    walletAddress: $wallet,
    tier: "standard",
    alerts: {
      telegram: (if $telegram != "" then $telegram else null end),
      discord:  (if $discord  != "" then $discord  else null end),
      email:    (if $email    != "" then $email    else null end)
    }
  }')

echo "[guardian] Subscribing $WALLET to monitoring..." >&2

EXTRA_HEADER=()
if [[ -n "$SESSION_TOKEN" ]]; then
  EXTRA_HEADER=(-H "Cookie: guardian_session=$SESSION_TOKEN")
fi

RESPONSE=$(curl -s -w "\n__STATUS__%{http_code}" \
  -X POST "$API_BASE/api/guardian/subscribe" \
  -H "Content-Type: application/json" \
  "${EXTRA_HEADER[@]}" \
  -d "$PAYLOAD")

HTTP_STATUS=$(echo "$RESPONSE" | tail -1 | sed 's/__STATUS__//')
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "Error: Subscribe failed (HTTP $HTTP_STATUS)" >&2
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

echo "$BODY" | jq '{
  success: .success,
  wallet: .wallet,
  tier: .tier,
  alertChannels: .alertChannels,
  message: "x402janus monitoring active. You will receive alerts for risky approvals."
}' 2>/dev/null || echo "$BODY"
