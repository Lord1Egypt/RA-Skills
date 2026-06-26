#!/usr/bin/env bash
echo "DEPRECATED: This skill is no longer maintained. Use x402janus skill instead." && exit 1

# guardian-scan.sh — Scan a wallet for risky token approvals via x402janus (x402)
# Usage: guardian-scan.sh <wallet_address> [--tier quick|standard] [--key <private_key>]
#
# Tiers:
#   quick    — $0.01 USDC — deterministic risk score, no AI  (default)
#   standard — $0.05 USDC — full AI analysis + graph scan
#
# Env:
#   PRIVATE_KEY     Signing key for x402 payment (required unless X402_PAYMENT_HEADER set)
#   X402_PAYMENT_HEADER   Pre-built payment header (advanced)
#   API_BASE        Override API base (default: https://www.x402pulse.xyz)
set -euo pipefail

API_BASE="${API_BASE:-https://www.x402pulse.xyz}"
TIER="quick"
WALLET=""
PRIVATE_KEY="${PRIVATE_KEY:-}"
X402_PAYMENT_HEADER="${X402_PAYMENT_HEADER:-}"

usage() {
  cat >&2 <<EOF
Usage: $0 <wallet_address> [--tier quick|standard] [--key <private_key>]

Tiers:
  quick    \$0.01 — deterministic risk score (default)
  standard \$0.05 — full AI analysis

Env:
  PRIVATE_KEY          Signing key for x402 payment
  X402_PAYMENT_HEADER  Pre-built payment header (advanced)
  API_BASE             Override API base (default: $API_BASE)

Example:
  $0 0xYourWallet --tier standard
  PRIVATE_KEY=0x... $0 0xYourWallet
EOF
}

# Dependency checks
for dep in curl jq; do
  if ! command -v "$dep" &>/dev/null; then
    echo "Error: '$dep' is required but not installed." >&2
    exit 1
  fi
done

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  usage
  exit 0
fi

WALLET="$1"
shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tier) TIER="$2"; shift 2 ;;
    --key)  PRIVATE_KEY="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ ! "$WALLET" =~ ^0x[a-fA-F0-9]{40}$ ]]; then
  echo "Error: Invalid wallet address: $WALLET" >&2
  exit 1
fi

if [[ "$TIER" != "quick" && "$TIER" != "standard" ]]; then
  echo "Error: tier must be 'quick' or 'standard'" >&2
  exit 1
fi

PRICE_USD="$( [[ "$TIER" == "quick" ]] && echo "0.01" || echo "0.05" )"
echo "[guardian] Scanning $WALLET (tier=$TIER, price=\$$PRICE_USD)..." >&2

# Build request — x402 payment handled by server-side facilitator for now
# If X402_PAYMENT_HEADER is set, include it; otherwise attempt unauthenticated (server may return 402)
EXTRA_HEADER=""
if [[ -n "${X402_PAYMENT_HEADER:-}" ]]; then
  EXTRA_HEADER="-H \"X-PAYMENT: $X402_PAYMENT_HEADER\""
fi

RESPONSE=$(curl -s -w "\n__STATUS__%{http_code}" \
  "${EXTRA_HEADER:+-H}" "${EXTRA_HEADER:+X-PAYMENT: $X402_PAYMENT_HEADER}" \
  "$API_BASE/api/guardian/scan/$WALLET?tier=$TIER")

HTTP_STATUS=$(echo "$RESPONSE" | tail -1 | sed 's/__STATUS__//')
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_STATUS" == "402" ]]; then
  echo "" >&2
  echo "Payment required. To pay via x402, set PRIVATE_KEY and re-run." >&2
  echo "Response:" >&2
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 2
fi

if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "Error: Scan failed (HTTP $HTTP_STATUS)" >&2
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

# Pretty print results
echo "$BODY" | jq '{
  wallet: .wallet,
  riskScore: .riskScore,
  riskLevel: .riskLevel,
  flaggedApprovals: (.approvals // [] | map(select(.risk == "high" or .risk == "medium")) | length),
  totalApprovals: (.approvals // [] | length),
  topRisks: (.approvals // [] | map(select(.risk == "high")) | .[0:3] | map({token: .tokenSymbol, spender: .spender, risk: .riskReason})),
  recommendation: .recommendation
}' 2>/dev/null || echo "$BODY"
