#!/bin/bash
# crucible-skill installer for Claude Code
# Usage: bash install.sh [--uninstall]

set -e

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SKILL_NAME="crucible"
SKILL_DIR="$CLAUDE_DIR/skills/ccg/$SKILL_NAME"
CMD_FILE="$CLAUDE_DIR/commands/ccg/$SKILL_NAME.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[✗]${NC} $*"; }

uninstall() {
    echo "Uninstalling crucible skill..."
    if [ -d "$SKILL_DIR" ]; then
        rm -rf "$SKILL_DIR"
        info "Removed $SKILL_DIR"
    else
        warn "$SKILL_DIR not found, skipping"
    fi
    if [ -f "$CMD_FILE" ]; then
        rm -f "$CMD_FILE"
        info "Removed $CMD_FILE"
    else
        warn "$CMD_FILE not found, skipping"
    fi
    info "Uninstall complete."
    exit 0
}

if [ "$1" = "--uninstall" ]; then
    uninstall
fi

echo ""
echo "🔬 Installing Crucible — 严峻考验式交付管线"
echo ""

# Pre-flight check
if [ ! -d "$SCRIPT_DIR/skill" ]; then
    error "Cannot find skill/ directory. Run this script from the crucible-skill package root."
    exit 1
fi

# Create target directories
mkdir -p "$CLAUDE_DIR/skills/ccg/$SKILL_NAME"
mkdir -p "$CLAUDE_DIR/commands/ccg"

# Copy skill content
cp -r "$SCRIPT_DIR/skill/"* "$SKILL_DIR/"
info "Installed skill files → $SKILL_DIR"

# Copy command file
cp "$SCRIPT_DIR/command/$SKILL_NAME.md" "$CMD_FILE"
info "Installed command  → $CMD_FILE"

echo ""
info "Installation complete!"
echo ""
echo "  Restart Claude Code or run /skills to see: ccg:crucible"
echo ""
echo "  Usage:"
echo "    /ccg:crucible <需求>          # 完整 8 阶段交付"
echo "    /ccg:crucible --dev <需求>    # 开发 + 自审（最常用）"
echo "    /ccg:crucible --help          # 查看所有模式"
echo ""
