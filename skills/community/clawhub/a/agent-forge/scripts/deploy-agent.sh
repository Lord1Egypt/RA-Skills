#!/bin/bash
#
# deploy-agent.sh - Deploy a new OpenClaw agent (v2)
# Usage: bash deploy-agent.sh <agent-id> <model> "<role>" "<tools>" "<channels>" "<sandbox>" "<personality>"
#
# Changes from v1:
# - SOUL.md / AGENTS.md / IDENTITY.md are NO LONGER generated here (Claude writes them from interview)
# - USER.md is copied from main workspace + agent-specific section appended
# - Directory + scaffold files (MEMORY, HEARTBEAT, TOOLS) still created here
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

AGENT_ID="${1:-}"
MODEL="${2:-minimax-portal/MiniMax-M2.5}"
ROLE="${3:-}"
TOOLS="${4:-read,write}"
CHANNELS="${5:-telegram}"
SANDBOX="${6:-all}"
PERSONALITY="${7:-Efficient Machine}"

if [ -z "$AGENT_ID" ] || [ -z "$ROLE" ]; then
    echo -e "${RED}Error: Missing required parameters${NC}"
    echo "Usage: bash deploy-agent.sh <agent-id> <model> '<role>' '<tools>' '<channels>' '<sandbox>' '<personality>'"
    exit 1
fi

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
AGENTS_DIR="$OPENCLAW_HOME/agents"
MAIN_WORKSPACE="$OPENCLAW_HOME/workspace"
AGENT_WORKSPACE="$OPENCLAW_HOME/workspace-$AGENT_ID"
MAIN_AGENTS_FILE="$MAIN_WORKSPACE/AGENTS.md"

echo -e "${YELLOW}[1/5] Creating directories...${NC}"
mkdir -p "$AGENTS_DIR/$AGENT_ID/agent"
mkdir -p "$AGENT_WORKSPACE/memory"
mkdir -p "$AGENT_WORKSPACE/skills"

echo -e "${YELLOW}[2/5] Creating USER.md (from main + agent diff)...${NC}"
MAIN_USER="$MAIN_WORKSPACE/USER.md"
if [ -f "$MAIN_USER" ]; then
    cp "$MAIN_USER" "$AGENT_WORKSPACE/USER.md"
else
    cat > "$AGENT_WORKSPACE/USER.md" << 'USEREOF'
# USER.md - About Your Human

- **Name:** Mo
- **What to call them:** 主人
- **Timezone:** America/Chicago
- **Notes:** 赚钱目标：openclaw自主赚钱6个月内月收入 $5000+，预算：API 日限 $8
USEREOF
fi

cat >> "$AGENT_WORKSPACE/USER.md" << EOF

---

## Agent-Specific Context (${AGENT_ID})

- **This agent's role:** ${ROLE}
- **Channels:** ${CHANNELS}
- **Personality:** ${PERSONALITY}
EOF

echo -e "${YELLOW}[3/5] Creating scaffold files (HEARTBEAT, MEMORY, TOOLS)...${NC}"

cat > "$AGENT_WORKSPACE/HEARTBEAT.md" << EOF
# HEARTBEAT.md - ${AGENT_ID}

## Patrol Interval: 30 minutes

## Focus
- Execute ${ROLE} tasks
- Report blockers to Main Agent immediately
- Log revenue events to MEMORY.md

## Status
Last check: Never
EOF

cat > "$AGENT_WORKSPACE/MEMORY.md" << EOF
# MEMORY.md - ${AGENT_ID}

_Last updated: $(date +%Y-%m-%d)_

## Role
${ROLE}

## Key Decisions
_(populated during operation)_

## Revenue Events
_(populated during operation)_
EOF

cat > "$AGENT_WORKSPACE/TOOLS.md" << EOF
# TOOLS.md - ${AGENT_ID}

## Enabled Tools
${TOOLS}

## Sandbox Level
${SANDBOX}

## Revenue Notes
_(track what tools drive ROI here)_
EOF

echo -e "${YELLOW}[4/5] Updating Main Agent AGENTS.md registry...${NC}"

if ! grep -q "## Team Registry" "$MAIN_AGENTS_FILE" 2>/dev/null; then
    echo -e "\n## Team Registry\n" >> "$MAIN_AGENTS_FILE"
fi

AGENT_ENTRY="### ${AGENT_ID}
- **ID:** ${AGENT_ID}
- **Model:** ${MODEL}
- **Role:** ${ROLE}
- **Channels:** ${CHANNELS}
- **Tools:** ${TOOLS}
- **Sandbox:** ${SANDBOX}
- **Workspace:** ${AGENT_WORKSPACE}/
"

if ! grep -q "### ${AGENT_ID}" "$MAIN_AGENTS_FILE" 2>/dev/null; then
    echo "$AGENT_ENTRY" >> "$MAIN_AGENTS_FILE"
    echo -e "${GREEN}Registered ${AGENT_ID} in Main Agent AGENTS.md${NC}"
else
    echo -e "${YELLOW}${AGENT_ID} already in registry, skipping${NC}"
fi

echo -e "${YELLOW}[5/5] Creating agent config...${NC}"
cat > "$AGENTS_DIR/$AGENT_ID/agent/config.json" << EOF
{
  "agent_id": "${AGENT_ID}",
  "model": "${MODEL}",
  "role": "${ROLE}",
  "tools": "${TOOLS}",
  "channels": "${CHANNELS}",
  "sandbox": "${SANDBOX}",
  "personality": "${PERSONALITY}",
  "workspace": "${AGENT_WORKSPACE}",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Agent '${AGENT_ID}' scaffold complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  Workspace:  ${AGENT_WORKSPACE}"
echo "  Model:      ${MODEL}"
echo "  Channels:   ${CHANNELS}"
echo ""
echo -e "${YELLOW}⚠️  SOUL.md / AGENTS.md / IDENTITY.md must be written by Claude (not this script)${NC}"
echo -e "${YELLOW}   These files require interview data and are generated in Step 9 of agent-forge skill.${NC}"
echo ""
echo -e "${YELLOW}Next: Claude will write SOUL/AGENTS/IDENTITY, then run gateway config.patch${NC}"
