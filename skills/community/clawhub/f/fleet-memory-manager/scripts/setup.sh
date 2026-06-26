#!/usr/bin/env bash
# =============================================================================
# memory-manager setup.sh
#
# One-command setup for the 3-layer memory system.
# Run this from your agent's workspace directory.
#
# Usage:
#   cd ~/your-agent-workspace
#   bash ~/.openclaw/skills/memory-manager/scripts/setup.sh
#
# What this does:
#   1. Creates memory/ directory for daily notes
#   2. Copies templates (MEMORY.md, USER.md, HEARTBEAT.md, AGENTS.md)
#      into your workspace — skips any that already exist
#   3. Creates today's daily notes file
#   4. Prints next steps
# =============================================================================

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"
WORKSPACE_DIR="${1:-$(pwd)}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo ""
echo -e "${BOLD}memory-manager setup${NC}"
echo -e "${BLUE}Setting up 3-layer memory system in: ${WORKSPACE_DIR}${NC}"
echo ""

# ─────────────────────────────────────────────────────────────────────────────
# Step 1: Create memory/ directory
# ─────────────────────────────────────────────────────────────────────────────
MEMORY_DIR="$WORKSPACE_DIR/memory"

if [ -d "$MEMORY_DIR" ]; then
  echo -e "  ${YELLOW}→${NC} memory/ directory already exists — skipping"
else
  mkdir -p "$MEMORY_DIR"
  echo -e "  ${GREEN}✓${NC} Created memory/ directory"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 2: Copy templates (skip if file already exists)
# ─────────────────────────────────────────────────────────────────────────────
copy_template() {
  local template_file="$TEMPLATES_DIR/$1"
  local dest_file="$WORKSPACE_DIR/$2"
  local label="$3"

  if [ ! -f "$template_file" ]; then
    echo -e "  ${RED}✗${NC} Template not found: $template_file"
    return 1
  fi

  if [ -f "$dest_file" ]; then
    echo -e "  ${YELLOW}→${NC} $label already exists — skipping (keeping yours)"
  else
    cp "$template_file" "$dest_file"
    echo -e "  ${GREEN}✓${NC} Created $label from template"
  fi
}

echo ""
echo -e "${BOLD}Copying templates...${NC}"
copy_template "MEMORY.md"    "MEMORY.md"    "MEMORY.md (long-term memory)"
copy_template "USER.md"      "USER.md"      "USER.md (user profile)"
copy_template "AGENTS.md"    "AGENTS.md"    "AGENTS.md (startup sequence)"
copy_template "HEARTBEAT.md" "HEARTBEAT.md" "HEARTBEAT.md (heartbeat config)"

# ─────────────────────────────────────────────────────────────────────────────
# Step 3: Create today's daily notes file
# ─────────────────────────────────────────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
DAILY_FILE="$MEMORY_DIR/$TODAY.md"

echo ""
echo -e "${BOLD}Setting up daily notes...${NC}"

if [ -f "$DAILY_FILE" ]; then
  echo -e "  ${YELLOW}→${NC} Today's notes ($TODAY.md) already exist — skipping"
else
  cat > "$DAILY_FILE" << EOF
# $TODAY

<!-- Daily notes created by memory-manager setup -->
<!-- This is Layer 2 of your 3-layer memory system -->
<!-- Write here during sessions; nightly cron promotes important stuff to MEMORY.md -->

## Sessions

<!-- Add session notes here as you work -->

## Active Projects

<!-- Track project state so future sessions can pick up without re-explaining -->

## Context for Next Session

<!-- THIS IS THE MOST IMPORTANT SECTION -->
<!-- Write what future-you needs to know to pick up without asking again -->
<!-- Think: "briefing a colleague who just joined" -->

- Memory-manager setup complete
- Templates copied to workspace — customize USER.md and MEMORY.md next

## Raw Log

<!-- Less curated — dump things here that might matter later -->
<!-- The nightly consolidation will extract what's worth keeping -->

- memory-manager installed and configured
EOF
  echo -e "  ${GREEN}✓${NC} Created today's daily notes: memory/$TODAY.md"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 4: Create heartbeat state file
# ─────────────────────────────────────────────────────────────────────────────
HEARTBEAT_STATE="$MEMORY_DIR/heartbeat-state.json"
if [ ! -f "$HEARTBEAT_STATE" ]; then
  cat > "$HEARTBEAT_STATE" << EOF
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": null,
    "projects": null,
    "memoryHealth": null
  },
  "installDate": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "lastConsolidation": null
}
EOF
  echo -e "  ${GREEN}✓${NC} Created heartbeat state file"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Step 5: Summary and next steps
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}Setup complete!${NC}"
echo ""
echo -e "${BOLD}Files created in $WORKSPACE_DIR:${NC}"
echo ""
echo "  memory-manager-skill/"
echo "  ├── MEMORY.md          ← Layer 1: Long-term memory (customize this)"
echo "  ├── USER.md            ← Layer 3: User profile (fill this in)"
echo "  ├── AGENTS.md          ← Startup sequence (already wired for 3 layers)"
echo "  ├── HEARTBEAT.md       ← Heartbeat config (customize project list)"
echo "  └── memory/"
echo "      ├── $TODAY.md  ← Today's operational notes"
echo "      └── heartbeat-state.json"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo ""
echo -e "  ${BLUE}1.${NC} Edit USER.md — fill in who the human is, how they work"
echo -e "  ${BLUE}2.${NC} Edit MEMORY.md — add any existing long-term context"
echo -e "  ${BLUE}3.${NC} Edit HEARTBEAT.md — add your active projects to monitor"
echo -e "  ${BLUE}4.${NC} Add the nightly consolidation cron (see SKILL.md for prompt)"
echo ""
echo -e "${BOLD}Nightly consolidation cron (add in OpenClaw):${NC}"
echo ""
echo "  Schedule: 0 2 * * *"
echo "  Model:    anthropic/claude-opus-4-5"
echo "  Channel:  <your-main-channel-id>"
echo "  Prompt:   (see SKILL.md → 'Step 4: Set Up Nightly Consolidation')"
echo ""
echo -e "  ${YELLOW}Tip:${NC} Run 'openclaw skills show memory-manager' to see the full prompt."
echo ""
