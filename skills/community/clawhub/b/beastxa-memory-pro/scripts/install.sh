#!/usr/bin/env bash
#
# BeastXA Memory Pro — One-Click Installer
#
# Usage:
#   bash install.sh
#   bash install.sh --workspace /path/to/workspace
#
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}🧠 BeastXA Memory Pro — Installer${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Detect workspace
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Check if --workspace flag is provided
WORKSPACE=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --workspace|-w)
            WORKSPACE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Auto-detect workspace from OpenClaw config if not specified
if [ -z "$WORKSPACE" ]; then
    # Try to find workspace from openclaw config
    if command -v openclaw &> /dev/null; then
        WORKSPACE=$(openclaw config get agents.defaults.workspace 2>/dev/null || echo "")
    fi
    
    # Fallback: use current directory
    if [ -z "$WORKSPACE" ] || [ "$WORKSPACE" = "null" ]; then
        WORKSPACE="$(pwd)"
    fi
fi

echo -e "📂 Workspace: ${GREEN}${WORKSPACE}${NC}"
echo ""

# Step 1: Check prerequisites
echo -e "${YELLOW}Step 1/4: Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi
echo "   ✅ Python 3 found: $(python3 --version)"

if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ OpenClaw not found. Please install OpenClaw first.${NC}"
    echo "   See: https://docs.openclaw.ai"
    exit 1
fi
echo "   ✅ OpenClaw found"

OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
if [ ! -f "$OPENCLAW_CONFIG" ]; then
    echo -e "${RED}❌ OpenClaw config not found at $OPENCLAW_CONFIG${NC}"
    exit 1
fi
echo "   ✅ OpenClaw config found"
echo ""

# Step 2: Create memory structure
echo -e "${YELLOW}Step 2/4: Setting up memory structure...${NC}"
python3 "${SCRIPT_DIR}/setup_memory.py" --workspace "$WORKSPACE"
echo ""

# Step 3: Configure compaction enhancement
echo -e "${YELLOW}Step 3/4: Enhancing compaction config...${NC}"

python3 << PYEOF
import json
import os
import shutil
from datetime import datetime

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

# Backup config first
backup_path = config_path + f".backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
shutil.copy2(config_path, backup_path)
print(f"   📋 Config backed up to {os.path.basename(backup_path)}")

with open(config_path, 'r') as f:
    cfg = json.load(f)

# Ensure agents.defaults.compaction exists
agents = cfg.setdefault('agents', {})
defaults = agents.setdefault('defaults', {})
compaction = defaults.setdefault('compaction', {})

# Add memoryFlush if not present
if 'memoryFlush' not in compaction:
    compaction['memoryFlush'] = {
        "enabled": True,
        "prompt": (
            "Pre-compaction memory flush. Store durable memories only in "
            "memory/{date}.md (use today's date in YYYY-MM-DD format). "
            "Create memory/ directory if needed. "
            "If the file already exists, APPEND new content only — do not overwrite. "
            "Do NOT modify MEMORY.md, SOUL.md, TOOLS.md, or AGENTS.md. "
            "If nothing to store, reply with NO_REPLY."
        )
    }
    print("   ✅ memoryFlush configured")
else:
    print("   ⏭️  memoryFlush already configured")

# Add compaction instructions if not present
if 'instructions' not in compaction:
    compaction['instructions'] = (
        "Preserve in summary: 1) User's explicit decisions and instructions (quote verbatim) "
        "2) File paths and code changes 3) Errors encountered and fixes applied "
        "4) Current task being worked on 5) Next step to take "
        "6) All non-tool user messages 7) Pending tasks not yet completed"
    )
    print("   ✅ Compaction instructions configured")
else:
    print("   ⏭️  Compaction instructions already configured")

with open(config_path, 'w') as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)

print("   ✅ Config saved")
PYEOF
echo ""

# Step 4: Set up cron jobs
echo -e "${YELLOW}Step 4/4: Setting up maintenance crons...${NC}"

# Check if crons already exist
EXISTING_CRONS=$(openclaw cron list 2>/dev/null | grep -c "Memory Pro" || true)
if [ "$EXISTING_CRONS" -gt 0 ]; then
    echo "   ⏭️  Memory Pro crons already exist ($EXISTING_CRONS found)"
else
    # Daily maintenance cron
    openclaw cron add \
        --name "Memory Pro — Daily Cleanup" \
        --cron "30 23 * * *" \
        --tz "$(python3 -c 'import time; print(time.tzname[0])' 2>/dev/null || echo 'UTC')" \
        --timeout-seconds 120 \
        --message 'You are a memory maintenance assistant. Tasks:
1. Read today'\''s memory/YYYY-MM-DD.md (use today'\''s date)
2. Extract key decisions, lessons, and rules
3. Append them to the appropriate memory/topics/*.md files
4. Do NOT delete any files or overwrite existing content
5. If nothing to organize, reply "No maintenance needed today."
Output: ✅ Daily cleanup: X topics updated' \
        > /dev/null 2>&1 && echo "   ✅ Daily cleanup cron created (23:30)" || echo "   ⚠️  Failed to create daily cron"

    # Weekly deep maintenance cron
    openclaw cron add \
        --name "Memory Pro — Weekly Deep Clean" \
        --cron "0 23 * * 0" \
        --tz "$(python3 -c 'import time; print(time.tzname[0])' 2>/dev/null || echo 'UTC')" \
        --timeout-seconds 180 \
        --message 'You are a memory maintenance assistant. Weekly deep clean:
1. Read all memory/topics/*.md files
2. Remove duplicate content across files
3. Merge related entries
4. Trim each file to under 100 lines (keep most recent/important)
5. Update memory/MEMORY-INDEX.md if topics changed
6. Do NOT delete any files or modify MEMORY.md
Output: ✅ Weekly cleanup: X files updated, Y duplicates removed' \
        > /dev/null 2>&1 && echo "   ✅ Weekly deep clean cron created (Sunday 23:00)" || echo "   ⚠️  Failed to create weekly cron"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "What happens now:"
echo "  • Your agent auto-saves context before each compaction"
echo "  • Daily cleanup runs at 23:30 (organizes today's notes)"
echo "  • Weekly deep clean runs Sunday 23:00 (dedup + trim)"
echo ""
echo "Optional next steps:"
echo "  • Split existing MEMORY.md: python3 ${SCRIPT_DIR}/split_memory.py"
echo "  • Verify installation: bash ${SCRIPT_DIR}/verify.sh"
echo ""
