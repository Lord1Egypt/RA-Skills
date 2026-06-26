#!/bin/bash
# send.sh — Send sats between agent wallets

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/wallet.sh"
source "${script_dir}/lib/config.sh"

AGENTYARD_DIR="$HOME/.openclaw/agentyard"
WALLET_FILE="$AGENTYARD_DIR/wallet.json"

sender="${1:-}"
receiver="${2:-}"
amount="${3:-}"

if [[ -z "$sender" || -z "$receiver" || -z "$amount" ]]; then
  echo ""
  echo "  Usage: skill agentyard send <from> <to> <amount_sats>"
  echo "  Example: skill agentyard send pixel jet 2000"
  echo ""
  exit 1
fi

validate_agent_name "$sender" || exit 1
validate_agent_name "$receiver" || exit 1

if ! [[ "$amount" =~ ^[0-9]+$ ]]; then
  echo ""
  echo "  Error: amount must be a number."
  echo ""
  exit 1
fi

echo ""
echo "  Send Sats"
echo "  ─────────"
echo ""

# Resolve sender wallet — check special aliases first
if [[ "$sender" == "me" || "$sender" == "self" ]]; then
  sender_wallet="$WALLET_FILE"
else
  sender_wallet="agents/${sender}/agentyard.key"
fi

if [[ ! -f "$sender_wallet" ]]; then
  echo "  Wallet for '$sender' not found."
  echo "  Run 'skill agentyard publish $sender' first."
  echo ""
  exit 1
fi

# Resolve receiver wallet — check special aliases first
if [[ "$receiver" == "me" || "$receiver" == "self" ]]; then
  receiver_wallet="$WALLET_FILE"
else
  receiver_wallet="agents/${receiver}/agentyard.key"
fi

if [[ ! -f "$receiver_wallet" ]]; then
  echo "  Wallet for '$receiver' not found."
  echo ""
  exit 1
fi

# Check balance
sender_balance=$(get_wallet_balance "$sender_wallet")

if [[ $sender_balance -lt $amount ]]; then
  echo "  Insufficient balance."
  echo "  Available: $sender_balance sats"
  echo "  Requested: $amount sats"
  echo ""
  exit 1
fi

echo "  From:    $sender"
echo "  To:      $receiver"
echo "  Amount:  $amount sats"
echo ""
echo "  Processing..."

# Debit sender — set rollback trap for unexpected exit
_rollback_send() {
  update_wallet_balance "$sender_wallet" "$amount" 2>/dev/null
  echo "  Payment interrupted. Balance restored." >&2
}
trap _rollback_send EXIT

update_wallet_balance "$sender_wallet" "-$amount"

# Credit receiver
if ! update_wallet_balance "$receiver_wallet" "$amount"; then
  echo "  Payment failed. Balance restored."
  echo ""
  exit 1
fi

# Payment complete — clear rollback trap
trap - EXIT

sender_new=$(get_wallet_balance "$sender_wallet")
receiver_new=$(get_wallet_balance "$receiver_wallet")

echo ""
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  Payment sent                                    │"
echo "  │                                                 │"
echo "  │  $sender:  $sender_new sats"
echo "  │  $receiver:  $receiver_new sats"
echo "  │                                                 │"
echo "  └─────────────────────────────────────────────────┘"
echo ""
