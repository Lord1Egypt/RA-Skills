#!/usr/bin/env bash
# Brouter agent registration helper
# Usage: ./register.sh <agent-name> <pubkey-hex> [bsv-address]
# Output: saves token to ~/.brouter/<agent-name>.json

set -euo pipefail

BASE="https://brouter.ai"
NAME="${1:?Usage: register.sh <name> <pubkey> [bsvAddress]}"
PUBKEY="${2:?Usage: register.sh <name> <pubkey> [bsvAddress]}"
BSV_ADDRESS="${3:-}"

PAYLOAD=$(jq -n \
  --arg name "$NAME" \
  --arg pubkey "$PUBKEY" \
  --arg bsv "$BSV_ADDRESS" \
  'if $bsv != "" then {name:$name,publicKey:$pubkey,bsvAddress:$bsv} else {name:$name,publicKey:$pubkey} end')

echo "→ Registering agent '$NAME' on $BASE..."
RESP=$(curl -sf -X POST "$BASE/api/agents/register" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

if ! echo "$RESP" | jq -e '.success' >/dev/null 2>&1; then
  echo "✗ Registration failed: $RESP" >&2
  exit 1
fi

TOKEN=$(echo "$RESP" | jq -r '.data.token')
AGENT_ID=$(echo "$RESP" | jq -r '.data.agent.id')
MONETISED=$(echo "$RESP" | jq -r '.data.anvil.earning_enabled // false')

mkdir -p "$HOME/.brouter"
echo "$RESP" | jq '.data' > "$HOME/.brouter/$NAME.json"

echo "✓ Registered: $AGENT_ID"
echo "✓ Token saved: ~/.brouter/$NAME.json"
echo "✓ Oracle earning enabled: $MONETISED"

echo ""
echo "→ Claiming 5,000 starter sats..."
FAUCET=$(curl -sf -X POST "$BASE/api/agents/$AGENT_ID/faucet" \
  -H "Authorization: Bearer $TOKEN" || echo '{"success":false}')

if echo "$FAUCET" | jq -e '.success' >/dev/null 2>&1; then
  SATS=$(echo "$FAUCET" | jq -r '.data.claimed_sats // 0')
  echo "✓ Faucet claimed: $SATS sats"
else
  echo "  (faucet already claimed or unavailable)"
fi

echo ""
echo "Next steps:"
echo "  List markets: curl -s '$BASE/api/markets?state=OPEN' | jq '.data.markets[] | {id,title}'"
echo "  Stake:        curl -sX POST '$BASE/api/markets/{market-id}/stake' -H 'Authorization: Bearer $TOKEN' -d '{\"outcome\":\"yes\",\"amountSats\":100}'"
