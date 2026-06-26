#!/bin/bash
#
# Post-Restore Check Script - 恢复后检查脚本
# 在 one-click-restore.sh 之后运行，检查恢复状态
#
# Usage:
#   ./post-restore-check.sh <backup-file>
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================"
echo "  Post-Restore Check"
echo "========================================"
echo ""

WORKSPACE_DIR="$HOME/.openclaw/workspace"
BACKUP_FILE="$1"

# Colors helper
check() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
info() { echo -e "${BLUE}ℹ${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; }

# Check 1: Workspace files
echo -e "${YELLOW}[1/6] Checking workspace files...${NC}"
for f in MEMORY.md USER.md IDENTITY.md SOUL.md AGENTS.md TOOLS.md HEARTBEAT.md; do
    if [ -f "$WORKSPACE_DIR/$f" ]; then
        check "$f exists"
    else
        warn "$f missing"
    fi
done
echo ""

# Check 2: Skills
echo -e "${YELLOW}[2/6] Checking skills...${NC}"
if [ -d "$WORKSPACE_DIR/skills" ]; then
    SKILL_COUNT=$(ls -d "$WORKSPACE_DIR/skills"/*/ 2>/dev/null | wc -l)
    check "Skills directory exists ($SKILL_COUNT skills)"
else
    warn "Skills directory missing"
fi
echo ""

# Check 3: Python dependencies
echo -e "${YELLOW}[3/6] Checking Python dependencies...${NC}"
if [ -f "$WORKSPACE_DIR/requirements.txt" ]; then
    DEP_COUNT=$(wc -l < "$WORKSPACE_DIR/requirements.txt")
    check "requirements.txt exists ($DEP_COUNT packages)"
    
    # Suggest installation
    info "To install dependencies, run:"
    echo "  pip3 install -r $WORKSPACE_DIR/requirements.txt"
else
    warn "requirements.txt not found (optional)"
fi
echo ""

# Check 4: Node.js dependencies
echo -e "${YELLOW}[4/6] Checking Node.js dependencies...${NC}"
if [ -f "$WORKSPACE_DIR/package.json" ]; then
    check "package.json exists"
    info "To install dependencies, run:"
    echo "  cd $WORKSPACE_DIR && npm install"
else
    warn "package.json not found (optional)"
fi
echo ""

# Check 5: Cron tasks
echo -e "${YELLOW}[5/6] Checking cron tasks...${NC}"
if [ -f "$WORKSPACE_DIR/cron-tasks-"*.json ] 2>/dev/null; then
    check "Cron tasks export found"
    info "To restore cron tasks, run:"
    echo "  clawhub cron list"
else
    warn "Cron tasks export not found"
fi
echo ""

# Check 6: Config files
echo -e "${YELLOW}[6/6] Checking configuration...${NC}"
if [ -d "$WORKSPACE_DIR/configs" ]; then
    check "configs directory exists"
    if [ -f "$WORKSPACE_DIR/configs/public-config.json" ]; then
        check "public-config.json found"
    fi
else
    warn "configs directory missing"
fi
echo ""

# Summary
echo "========================================"
echo "  Check Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Review any warnings above"
echo "  2. Install dependencies if needed"
echo "  3. Recreate cron tasks if needed"
echo "  4. Test the restored workspace"
echo ""
