#!/bin/bash
set -euo pipefail

# Agent Maker - List All Agents
# Usage: ./list-agents.sh

echo "📋 Current OpenClaw Agents"
echo "=========================="
echo ""

AGENTS_DIR="${HOME}/.openclaw/agents"

if [[ ! -d "$AGENTS_DIR" ]]; then
    echo "❌ Agents directory not found: $AGENTS_DIR"
    exit 1
fi

# Count agents
AGENT_COUNT=0

# List each agent
for agent_dir in "$AGENTS_DIR"/*/; do
    if [[ -d "$agent_dir" ]]; then
        AGENT_NAME=$(basename "$agent_dir")
        AGENT_COUNT=$((AGENT_COUNT + 1))
        
        echo "🤖 ${AGENT_NAME}"
        echo "   Location: ${agent_dir}"
        
        # Check if identity file exists
        if [[ -f "${agent_dir}IDENTITY.md" ]]; then
            # Extract role from IDENTITY.md if possible
            ROLE=$(grep -i "^\- \*\*Role:\*\*" "${agent_dir}IDENTITY.md" 2>/dev/null | head -1 || echo "Not specified")
            echo "   ${ROLE}"
        fi
        
        # Check workspace
        if [[ -f "${agent_dir}SYSTEM.md" ]]; then
            WORKSPACE=$(grep -oP '工作目录是 `\K[^`]+|Workspace: \K.*' "${agent_dir}SYSTEM.md" 2>/dev/null | head -1 || echo "Not specified")
            if [[ -n "$WORKSPACE" ]]; then
                echo "   📁 Workspace: ${WORKSPACE}"
            fi
        fi
        
        echo ""
    fi
done

echo "=========================="
echo "Total: ${AGENT_COUNT} agent(s)"
echo ""

if [[ $AGENT_COUNT -eq 0 ]]; then
    echo "💡 No agents found. Create one with:"
    echo "   ./create-agent.sh --name=my-agent --role='My role description'"
fi