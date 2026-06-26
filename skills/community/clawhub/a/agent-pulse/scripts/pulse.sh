#!/usr/bin/env bash
echo "DEPRECATED: This skill is no longer maintained. Use x402janus skill instead." && exit 1

# pulse.sh — Send a liveness pulse via x402 (default) or direct on-chain (--direct)
#
# Default: x402 API call — no PULSE token balance required, pays micropayment per pulse
# Fallback: --direct — on-chain via cast, requires PRIVATE_KEY and PULSE tokens
#
# Env:
#   PRIVATE_KEY            Signing key (required for --direct; used for x402 permit signing)
#   BASE_RPC_URL           RPC URL (default: https://mainnet.base.org)
#   API_BASE               API base (default: https://x402pulse.xyz)
#   PULSE_REGISTRY_ADDRESS Override registry address
#   PULSE_TOKEN_ADDRESS    Override token address
set -euo pipefail

API_BASE="${API_BASE:-https://x402pulse.xyz}"
REGISTRY_DEFAULT="0xe61C615743A02983A46aFF66Db035297e8a43846"
TOKEN_DEFAULT="0x21111B39A502335aC7e45c4574Dd083A69258b07"
REGISTRY_ADDRESS="${PULSE_REGISTRY_ADDRESS:-$REGISTRY_DEFAULT}"
REGISTRY_ADDRESS="${REGISTRY_ADDRESS//\"/}"
PULSE_TOKEN_ADDRESS="${PULSE_TOKEN_ADDRESS:-$TOKEN_DEFAULT}"
PULSE_TOKEN_ADDRESS="${PULSE_TOKEN_ADDRESS//\"/}"

usage() {
  cat >&2 <<EOF
Usage:
  x402 (default — recommended):
    $0                          # pulse via API, no PULSE tokens needed

  Direct on-chain (advanced):
    $0 --direct <amountWei>     # requires PRIVATE_KEY + PULSE token balance

Env:
  PRIVATE_KEY               Signing key (x402 permit or --direct)
  BASE_RPC_URL              RPC URL (default: https://mainnet.base.org)
  API_BASE                  Override API base
  PULSE_REGISTRY_ADDRESS    Override registry
  PULSE_TOKEN_ADDRESS       Override token
EOF
}

for dep in curl jq; do
  command -v "$dep" &>/dev/null || { echo "Error: '$dep' is required." >&2; exit 1; }
done

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then usage; exit 0; fi

# ── Direct on-chain mode ──────────────────────────────────────────────────
if [[ "${1:-}" == "--direct" ]]; then
  if [[ $# -ne 2 ]]; then usage; exit 2; fi
  AMOUNT="$2"
  if [[ ! "$AMOUNT" =~ ^[0-9]+$ ]] || [[ "$AMOUNT" == "0" ]]; then
    echo "Error: Amount must be a positive integer (wei units)." >&2; exit 1
  fi
  command -v cast &>/dev/null || { echo "Error: 'cast' (Foundry) required for --direct mode." >&2; exit 1; }
  BASE_RPC_URL="${BASE_RPC_URL:-https://mainnet.base.org}"
  BASE_RPC_URL="${BASE_RPC_URL//\"/}"
  if [[ -z "${PRIVATE_KEY:-}" ]]; then
    echo "Error: PRIVATE_KEY is required for --direct mode." >&2; exit 1
  fi
  echo "[pulse] Direct mode: approving registry then pulsing on Base mainnet..." >&2
  cast send --rpc-url "$BASE_RPC_URL" --private-key "$PRIVATE_KEY" \
    "$PULSE_TOKEN_ADDRESS" "approve(address,uint256)(bool)" "$REGISTRY_ADDRESS" "$AMOUNT" >&2
  sleep 3  # wait for approve to propagate before pulsing
  cast send --rpc-url "$BASE_RPC_URL" --private-key "$PRIVATE_KEY" \
    "$REGISTRY_ADDRESS" "pulse(uint256)" "$AMOUNT"
  exit 0
fi

# ── x402 API mode (default) ──────────────────────────────────────────────
echo "[pulse] Sending pulse via x402 API..." >&2

EXTRA_ARGS=()
if [[ -n "${PRIVATE_KEY:-}" ]]; then
  EXTRA_ARGS+=(-H "X-PRIVATE-KEY: $PRIVATE_KEY")
fi

RESPONSE=$(curl -s -w "\n__STATUS__%{http_code}" -X POST "$API_BASE/api/pulse" \
  -H "Content-Type: application/json" \
  "${EXTRA_ARGS[@]}" \
  -d "{}")

HTTP_STATUS=$(echo "$RESPONSE" | tail -1 | sed 's/__STATUS__//')
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_STATUS" == "402" ]]; then
  echo "[pulse] Payment required. Set PRIVATE_KEY to enable automatic x402 payment." >&2
  echo "$BODY" | jq '.accepts[0] // .' 2>/dev/null || echo "$BODY"
  exit 2
fi

if [[ "$HTTP_STATUS" != "200" ]]; then
  echo "Error: Pulse failed (HTTP $HTTP_STATUS)" >&2
  echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"
  exit 1
fi

echo "$BODY" | jq '{success: .success, txHash: .txHash, streak: .streak}' 2>/dev/null || echo "$BODY"
