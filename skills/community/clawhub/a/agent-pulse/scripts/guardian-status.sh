#!/usr/bin/env bash
echo "DEPRECATED: This skill is no longer maintained. Use x402janus skill instead." && exit 1

# guardian-status.sh — Check x402janus subscription status for a wallet
# Usage: guardian-status.sh <wallet_address>
#
# Env:
#   API_BASE   Override API base (default: https://www.x402pulse.xyz)
set -euo pipefail

API_BASE="${API_BASE:-https://www.x402pulse.xyz}"

usage() {
  cat >&2 <<EOF
Usage: $0 <wallet_address>

Check if a wallet has an active x402janus subscription.

Env:
  API_BASE   Override API base (default: $API_BASE)

Example:
  $0 0xYourWallet
EOF
}

for dep in curl jq; do
  if ! command -v "$dep" &>/dev/null; then
    echo "Error: '$dep' is required." >&2; exit 1
  fi
done

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then usage; exit 0; fi

WALLET="$1"

if [[ ! "$WALLET" =~ ^0x[a-fA-F0-9]{40}$ ]]; then
  echo "Error: Invalid wallet address: $WALLET" >&2; exit 1
fi

echo "[guardian] Checking subscription status for $WALLET..." >&2

RESPONSE=$(curl -s -w "\n__STATUS__%{http_code}" \
  "$API_BASE/api/v2/agent/$WALLET/alive")

HTTP_STATUS=$(echo "$RESPONSE" | tail -1 | sed 's/__STATUS__//')
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "No active Guardian subscription found for $WALLET" >&2
  exit 1
fi

echo "$BODY" | jq '{
  wallet: .address,
  isAlive: .isAlive,
  lastPulse: .lastPulse,
  streak: .streak,
  guardian: "Run guardian-scan.sh to check approval risks"
}' 2>/dev/null || echo "$BODY"
