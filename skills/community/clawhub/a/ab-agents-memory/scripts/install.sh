#!/bin/bash
#
# AB Agents Memory — Installer
# Installs memory system for OpenClaw agents
#

set -e

echo "🦀 AB Agents Memory Installer"
echo "=============================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as user (not root for files)
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running as root. Files will be owned by root.${NC}"
    echo "Consider running as regular user for OpenClaw."
    echo ""
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "Installation directory: $REPO_DIR"
echo ""

# Ask where to install
DEFAULT_VAULT_DIR="$HOME/AB-Memory-Vault"
echo -n "Obsidian Vault location [$DEFAULT_VAULT_DIR]: "
read vault_dir
vault_dir="${vault_dir:-$DEFAULT_VAULT_DIR}"

# Ask for agent workspace
DEFAULT_AGENT_DIR="$HOME/.openclaw/workspace/agents/ab-memory"
echo -n "Agent workspace [$DEFAULT_AGENT_DIR]: "
read agent_dir
agent_dir="${agent_dir:-$DEFAULT_AGENT_DIR}"

echo ""
echo "Installing to:"
echo "  Vault:  $vault_dir"
echo "  Agent:  $agent_dir"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Copy Obsidian vault
echo -e "${GREEN}Installing Obsidian vault...${NC}"
mkdir -p "$vault_dir"
cp -r "$REPO_DIR/obsidian-vault/"* "$vault_dir/"
echo "  → Vault installed to $vault_dir"

# Copy agent
echo -e "${GREEN}Installing AB-Archivus agent...${NC}"
mkdir -p "$(dirname "$agent_dir")"
cp -r "$REPO_DIR/agents/AB-Archivus" "$agent_dir"
echo "  → Agent installed to $agent_dir"

# Update agent paths in SOUL.md
echo -e "${GREEN}Configuring agent paths...${NC}"
sed -i "s|~/Memory|$vault_dir/Memory|g" "$agent_dir/SOUL.md"
sed -i "s|~/Templates|$vault_dir/Templates|g" "$agent_dir/SOUL.md"
sed -i "s|~/Logs|$vault_dir/Logs|g" "$agent_dir/SOUL.md"
echo "  → Paths configured"

echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Add agent to OpenClaw: openclaw agents add ab-memory --workspace $agent_dir"
echo "  2. Restart gateway: openclaw gateway restart"
echo "  3. Configure bot token for @ab_memory_bot (optional)"
echo ""
echo "Documentation: $REPO_DIR/README.md"
echo "Channel: https://t.me/alexburr_agents"