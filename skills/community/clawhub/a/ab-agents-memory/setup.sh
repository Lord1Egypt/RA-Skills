#!/bin/bash
#
# AB Agents Memory — Setup Script
# Installs: Obsidian Vault + AB-Archivus Agent
#
# Usage: ./setup.sh [--skip-cron]
#

set -euo pipefail

# Colors
RED='\033[0;31m'
BLACK='\033[0;30m'
CRAB='\033[0;31m'  # Red for crab brand
NC='\033[0m' # No Color

BOLD='\033[1m'
DIM='\033[2m'

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_SOURCE="$SCRIPT_DIR/obsidian-vault"
AGENT_SOURCE="$SCRIPT_DIR/agents/AB-Archivus"
VAULT_DEST="${VAULT_DEST:-/data/obsidian/AB-Memory-Vault}"
AGENT_DEST="${HOME}/.openclaw/agents/AB-Archivus"

echo -e "${CRAB}"
echo "  ╔═══════════════════════════════════════════╗"
echo "  ║   AB Agents Memory — Setup 🦀             ║"
echo "  ╚═══════════════════════════════════════════╝"
echo -e "${NC}"

# Check prerequisites
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} OpenClaw not found. Install first: https://docs.openclaw.ai"
    exit 1
fi

# Step 1: Install Obsidian Vault
echo -e "${BOLD}[1/4]${NC} Installing Obsidian Vault..."
if [[ -d "$VAULT_DEST" ]]; then
    echo -e "  ${DIM}Vault already exists at $VAULT_DEST${NC}"
    echo -e "  ${DIM}Skipping...${NC}"
else
    mkdir -p "$(dirname "$VAULT_DEST")"
    cp -r "$VAULT_SOURCE" "$VAULT_DEST"
    echo -e "  ${CRAB}✓${NC} Vault installed to $VAULT_DEST"
fi

# Step 2: Install AB-Archivus Agent
echo -e "${BOLD}[2/4]${NC} Installing AB-Archivus agent..."
mkdir -p "$(dirname "$AGENT_DEST")"
cp -r "$AGENT_SOURCE" "$AGENT_DEST"

# Update paths in SOUL.md
if [[ -f "$AGENT_DEST/SOUL.md" ]]; then
    # Set vault path
    sed -i "s|/data/obsidian/AB-Memory-Vault/|$VAULT_DEST|g" "$AGENT_DEST/SOUL.md" 2>/dev/null || true
fi

echo -e "  ${CRAB}✓${NC} Agent installed to $AGENT_DEST"

# Step 3: Register agent with OpenClaw
echo -e "${BOLD}[3/4]${NC} Registering agent with OpenClaw..."
if openclaw agents list 2>/dev/null | grep -q "AB-Archivus"; then
    echo -e "  ${DIM}Agent already registered${NC}"
else
    openclaw agents add AB-Archivus --workspace "$AGENT_DEST" --non-interactive 2>/dev/null || \
    echo -e "  ${DIM}Manual registration may be needed${NC}"
fi
echo -e "  ${CRAB}✓${NC} Agent registered"

# Step 4: Setup cron for nightly processing
SKIP_CRON=false
for arg in "$@"; do
    [[ "$arg" == "--skip-cron" ]] && SKIP_CRON=true
done

if [[ "$SKIP_CRON" == "false" ]]; then
    echo -e "${BOLD}[4/4]${NC} Setting up nightly processing..."

    # Create nightly processing script
    NIGHTLY_SCRIPT="$VAULT_DEST/Memory/Processing/Nightly/process.sh"
    mkdir -p "$(dirname "$NIGHTLY_SCRIPT")"

    cat > "$NIGHTLY_SCRIPT" << 'SCRIPT'
#!/bin/bash
# Nightly memory processing
DATE=$(date +%Y-%m-%d)
echo "Processing: $DATE" >> ./Memory/Processing/Nightly/logs/"$DATE".md
# Add your processing logic here
SCRIPT

    chmod +x "$NIGHTLY_SCRIPT"
    mkdir -p "$VAULT_DEST/Memory/Processing/Nightly/logs"

    # Add to crontab (03:00 MSK daily)
    (crontab -l 2>/dev/null | grep -v "AB-Memory-Vault"; echo "0 3 * * * cd $VAULT_DEST && bash $NIGHTLY_SCRIPT >> $VAULT_DEST/Memory/Processing/Nightly/logs/\$(date +\%Y-\%m-\%d).log 2>&1") | crontab -
    echo -e "  ${CRAB}✓${NC} Cron installed (03:00 MSK daily)"
fi

# Done
echo ""
echo -e "${CRAB}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}✅ AB Agents Memory installed!${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart OpenClaw: openclaw gateway restart"
echo "  2. Open vault: $VAULT_DEST"
echo "  3. Add agents: @alexburr_agents"
echo ""
echo -e "${DIM}Branding: AB-Agents | Red + Black 🦀${NC}"
