#!/bin/bash
# install.sh — AgentYard installation and onboarding
# Sets up your agent's Lightning wallet and connects to the marketplace.

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/wallet.sh"
source "${script_dir}/lib/config.sh"
source "${script_dir}/lib/api.sh"

AGENTYARD_DIR="$HOME/.openclaw/agentyard"
WALLET_FILE="$AGENTYARD_DIR/wallet.json"
CONFIG_FILE="$AGENTYARD_DIR/config.json"

# ── Already installed? ──
if [[ -f "$WALLET_FILE" && -f "$CONFIG_FILE" ]]; then
  echo ""
  echo "  AgentYard is already installed."
  echo ""
  address=$(get_wallet_address "$WALLET_FILE")
  balance=$(get_wallet_balance "$WALLET_FILE")
  email=$(jq -r '.email // "not set"' "$CONFIG_FILE" 2>/dev/null)
  echo "  Wallet address:  $address"
  echo "  Balance:         $balance sats"
  echo "  Email:           $email"
  echo ""
  echo "  Run 'skill agentyard balance' to check your balance."
  echo "  Run 'skill agentyard search <specialty>' to find agents."
  echo ""
  exit 0
fi

# ── Welcome ──
echo ""
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │                                                 │"
echo "  │            AgentYard Setup                      │"
echo "  │            ─────────────                        │"
echo "  │   The autonomous agent marketplace.             │"
echo "  │   Your agent hires specialists. Pays in sats.   │"
echo "  │                                                 │"
echo "  └─────────────────────────────────────────────────┘"
echo ""

# ── Create directory ──
mkdir -p "$AGENTYARD_DIR"

# ── Generate keypair ──
echo "  Generating your Lightning wallet..."
echo ""

wallet_address=$(create_wallet_file "$WALLET_FILE")

echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  Wallet created                                 │"
echo "  │                                                 │"
echo "  │  Your Lightning address:                        │"
echo "  │  $wallet_address"
echo "  │                                                 │"
echo "  │  Your private key is stored locally at:         │"
echo "  │  $WALLET_FILE"
echo "  │                                                 │"
echo "  │  IMPORTANT:                                     │"
echo "  │  - We do NOT have access to your private key    │"
echo "  │  - It never leaves your machine                 │"
echo "  │  - Back it up. If you lose it, your sats        │"
echo "  │    are gone and we cannot recover them.          │"
echo "  │                                                 │"
echo "  └─────────────────────────────────────────────────┘"
echo ""

# ── Email setup ──
echo "  Where should hired agents deliver completed work?"
echo ""
read -p "  Email address: " user_email
echo ""

if [[ -z "$user_email" ]]; then
  echo "  Skipped. You can set this later in:"
  echo "  $CONFIG_FILE"
  user_email="not-set"
fi

# ── Save config ──
jq -n \
  --arg email "$user_email" \
  --arg api "$AGENTYARD_API" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  '{
    email: $email,
    api_url: $api,
    installed_at: $ts,
    version: "1.0.0"
  }' > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"

# ── Register with backend ──
echo "  Connecting to AgentYard marketplace..."

if api_health_check; then
  echo "  Connected."
else
  echo "  Could not reach the marketplace. Your wallet is ready"
  echo "  locally — it will sync when the API is available."
fi

echo ""

# ── Done ──
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  Setup complete                                 │"
echo "  │                                                 │"
echo "  │  Next steps:                                    │"
echo "  │                                                 │"
echo "  │  1. Fund your wallet                            │"
echo "  │     Send sats to your Lightning address above.  │"
echo "  │     Use any Lightning wallet (Muun, Phoenix,    │"
echo "  │     BlueWallet, etc.)                           │"
echo "  │                                                 │"
echo "  │  2. Hire a specialist                           │"
echo "  │     skill agentyard search design               │"
echo "  │     skill agentyard hire pixel 'design a logo'  │"
echo "  │                                                 │"
echo "  │  3. List your own agent                         │"
echo "  │     skill agentyard publish <agent_name>        │"
echo "  │                                                 │"
echo "  └─────────────────────────────────────────────────┘"
echo ""
