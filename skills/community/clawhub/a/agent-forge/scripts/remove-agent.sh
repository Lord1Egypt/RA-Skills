#!/bin/bash
#
# remove-agent.sh - Remove an OpenClaw agent
# Usage: bash remove-agent.sh <agent-id> [--force]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
AGENT_ID="${1:-}"
FORCE_FLAG=""

if [ "$2" = "--force" ]; then
    FORCE_FLAG="--force"
fi

# Validate required parameters
if [ -z "$AGENT_ID" ]; then
    echo -e "${RED}Error: Missing agent-id${NC}"
    echo "Usage: bash remove-agent.sh <agent-id> [--force]"
    echo ""
    echo "Example:"
    echo "  bash remove-agent.sh sales-bot"
    echo "  bash remove-agent.sh sales-bot --force  # Skip confirmation"
    exit 1
fi

# Configuration
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
AGENTS_DIR="$OPENCLAW_HOME/agents"
WORKSPACE_DIR="$OPENCLAW_HOME/workspace"
AGENT_WORKSPACE="$WORKSPACE_DIR/workspace-$AGENT_ID"
MAIN_AGENTS_FILE="$WORKSPACE_DIR/AGENTS.md"

# Confirmation prompt (unless --force)
if [ -z "$FORCE_FLAG" ]; then
    echo -e "${YELLOW}You are about to remove agent '$AGENT_ID'${NC}"
    echo ""
    echo "This will DELETE:"
    echo "  - Agent directory: $AGENTS_DIR/$AGENT_ID"
    echo "  - Workspace: $AGENT_WORKSPACE"
    echo ""
    read -p "Are you sure? (yes/no): " -r
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo -e "${BLUE}Aborted.${NC}"
        exit 0
    fi
fi

echo ""
echo -e "${YELLOW}Removing agent '$AGENT_ID'...${NC}"
echo ""

# Step 1: Stop the agent if running
echo -e "${BLUE}1. Stopping agent (if running)...${NC}"
if openclaw agent status "$AGENT_ID" &>/dev/null; then
    openclaw agent stop "$AGENT_ID" 2>/dev/null || true
    echo "  Agent stopped."
else
    echo "  Agent not running."
fi

# Step 2: Remove agent directory
echo -e "${BLUE}2. Removing agent directory...${NC}"
if [ -d "$AGENTS_DIR/$AGENT_ID" ]; then
    rm -rf "$AGENTS_DIR/$AGENT_ID"
    echo "  Removed: $AGENTS_DIR/$AGENT_ID"
else
    echo "  Directory not found: $AGENTS_DIR/$AGENT_ID"
fi

# Step 3: Remove workspace directory
echo -e "${BLUE}3. Removing workspace...${NC}"
if [ -d "$AGENT_WORKSPACE" ]; then
    rm -rf "$AGENT_WORKSPACE"
    echo "  Removed: $AGENT_WORKSPACE"
else
    echo "  Workspace not found: $AGENT_WORKSPACE"
fi

# Step 4: Remove from Main Agent AGENTS.md
echo -e "${BLUE}4. Updating Main Agent AGENTS.md...${NC}"
if [ -f "$MAIN_AGENTS_FILE" ]; then
    # Create temporary file
    TEMP_FILE=$(mktemp)
    
    # Remove the agent entry from Team Registry
    # This pattern matches the agent entry including its lines
    sed -i '' "/### $AGENT_ID/,/^- \*\*Workspace:\*\*/d" "$MAIN_AGENTS_FILE"
    
    # Clean up any empty lines left behind
    sed -i '' '/^$/N;/^\n$/d' "$MAIN_AGENTS_FILE"
    
    echo "  Removed from registry."
else
    echo "  Main AGENTS.md not found."
fi

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Agent '$AGENT_ID' removed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  Removed:"
echo "    - Agent config: $AGENTS_DIR/$AGENT_ID"
echo "    - Workspace: $AGENT_WORKSPACE"
echo "    - Registry entry: $MAIN_AGENTS_FILE"
echo ""
echo -e "${YELLOW}Note: Channel bindings were not modified.${NC}"
echo "      Remove them manually if needed."
echo ""
