#!/bin/bash
# balance.sh — Check wallet balance for your agent or a listed agent

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/wallet.sh"
source "${script_dir}/lib/config.sh"

AGENTYARD_DIR="$HOME/.openclaw/agentyard"
WALLET_FILE="$AGENTYARD_DIR/wallet.json"

agent_name="${1:-}"

echo ""

if [[ -z "$agent_name" ]]; then
  # Show main agent balance
  if [[ ! -f "$WALLET_FILE" ]]; then
    echo "  Wallet not found. Run 'skill agentyard install' first."
    echo ""
    exit 1
  fi

  balance=$(get_wallet_balance "$WALLET_FILE")
  address=$(get_wallet_address "$WALLET_FILE")
  pubkey=$(get_wallet_pubkey "$WALLET_FILE")

  echo "  Your Wallet"
  echo "  ───────────"
  echo "  Balance:     $balance sats"
  echo "  Address:     $address"
  echo "  Public key:  ${pubkey:0:24}..."
  echo ""
  echo "  Fund this address to hire agents."
  echo "  Private key stored at: $WALLET_FILE"
  echo ""
else
  validate_agent_name "$agent_name" || exit 1

  wallet_path="agents/${agent_name}/agentyard.key"

  if [[ ! -f "$wallet_path" ]]; then
    echo "  Wallet for '$agent_name' not found."
    echo "  Run 'skill agentyard publish $agent_name' to list this agent."
    echo ""
    exit 1
  fi

  balance=$(get_wallet_balance "$wallet_path")
  address=$(get_wallet_address "$wallet_path")

  echo "  $agent_name's Wallet"
  echo "  ─────────────────────"
  echo "  Balance:   $balance sats"
  echo "  Address:   $address"
  echo ""
fi
