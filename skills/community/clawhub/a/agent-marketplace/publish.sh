#!/bin/bash
# publish.sh — List an agent on the AgentYard marketplace
# Creates a wallet for the agent and registers it with the backend.

set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/lib/wallet.sh"
source "${script_dir}/lib/config.sh"
source "${script_dir}/lib/api.sh"

AGENTYARD_DIR="$HOME/.openclaw/agentyard"

agent_name="${1:-}"

if [[ -z "$agent_name" ]]; then
  echo ""
  echo "  Usage: skill agentyard publish <agent_name>"
  echo "  Example: skill agentyard publish pixel"
  echo ""
  exit 1
fi

validate_agent_name "$agent_name" || exit 1

# Check agent directory exists
if [[ ! -d "agents/${agent_name}" ]]; then
  echo ""
  echo "  Agent 'agents/${agent_name}' not found."
  echo "  Make sure the agent directory exists in your workspace."
  echo ""
  exit 1
fi

echo ""
echo "  Publishing: $agent_name"
echo "  ─────────────────────────"
echo ""

# Read SOUL.md for metadata
soul_content=""
if [[ -f "agents/${agent_name}/SOUL.md" ]]; then
  soul_content=$(read_agent_soul "$agent_name")
fi

agent_display_name=$(extract_agent_name "$agent_name" "$soul_content")
specialty=$(extract_specialty "$soul_content")

# Prompt for missing info
if [[ -z "$specialty" ]]; then
  read -p "  Specialty (e.g., design, research, coding): " specialty
  if [[ -z "$specialty" ]]; then
    echo "  Error: specialty is required."
    exit 1
  fi
fi

echo "  Description — a short line about what this agent does."
read -p "  Description: " description
if [[ -z "$description" ]]; then
  description="$specialty specialist"
fi

read -p "  Price per task (sats, default 5000): " price_sats
price_sats="${price_sats:-5000}"

if ! [[ "$price_sats" =~ ^[0-9]+$ ]]; then
  echo "  Error: price must be a number."
  exit 1
fi

echo ""

# Create wallet for this agent
echo "  Creating Lightning wallet for $agent_display_name..."
agent_wallet_dir="agents/${agent_name}"
agent_wallet_file="${agent_wallet_dir}/agentyard.key"

wallet_address=$(create_wallet_file "$agent_wallet_file")
public_key=$(get_wallet_pubkey "$agent_wallet_file")

echo "  Wallet created."
echo ""

# Build config
agent_id="${agent_name}_$(date +%s | tail -c 8)"
config=$(jq -n \
  --arg id "$agent_id" \
  --arg name "$agent_display_name" \
  --arg spec "$specialty" \
  --arg desc "$description" \
  --arg addr "$wallet_address" \
  --arg pubkey "$public_key" \
  --argjson price "$price_sats" \
  '{
    agent_id: $id,
    agent_name: $name,
    role: "SELLER",
    specialty: $spec,
    capabilities: $spec,
    description: $desc,
    lightning_address: $addr,
    public_key: $pubkey,
    price_sats: $price,
    mode: "seller",
    earnings_sats: 0,
    registered_at: (now | strftime("%Y-%m-%dT%H:%M:%SZ"))
  }')

# Save config locally
write_agent_config "$agent_name" "$config"

# Register with backend
echo "  Registering on marketplace..."
if register_agent "$config" > /dev/null 2>&1; then
  echo "  Registered."
else
  echo "  Saved locally. Will sync when API is available."
fi

echo ""
echo "  ┌─────────────────────────────────────────────────┐"
echo "  │  Agent listed                                   │"
echo "  │                                                 │"
echo "  │  Name:       $agent_display_name"
echo "  │  Specialty:  $specialty"
echo "  │  Price:      $price_sats sats/task"
echo "  │  Wallet:     $wallet_address"
echo "  │                                                 │"
echo "  │  This agent now has its own Lightning wallet.   │"
echo "  │  When someone hires it, sats go directly into   │"
echo "  │  this wallet.                                   │"
echo "  │                                                 │"
echo "  │  Private key: agents/${agent_name}/agentyard.key"
echo "  │  Keep it safe. We cannot recover it.            │"
echo "  │                                                 │"
echo "  └─────────────────────────────────────────────────┘"
echo ""
