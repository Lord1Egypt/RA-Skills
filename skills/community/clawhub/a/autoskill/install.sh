#!/usr/bin/env bash
# Install autoskill into ~/.claude/skills/ and ~/.claude/commands/
#
# To uninstall:
#   rm -rf ~/.claude/skills/autoskill
#   rm -f  ~/.claude/commands/autoskill.md
#
set -e

SKILL_DIR="$HOME/.claude/skills/autoskill"
CMD_DIR="$HOME/.claude/commands"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing autoskill..."

# Install skill
mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
echo "  ✓ Skill installed → $SKILL_DIR/SKILL.md"

# Install slash command
mkdir -p "$CMD_DIR"
cat > "$CMD_DIR/autoskill.md" << 'EOF'
---
description: Auto-detect and apply all relevant skills for the current problem
argument-hint: "[problem description or blank to infer from conversation]"
---

Read and follow `~/.claude/skills/autoskill/SKILL.md` from top to bottom.
Pass `$ARGUMENTS` as the problem statement to Phase 1.
EOF
echo "  ✓ Command installed → $CMD_DIR/autoskill.md"

echo ""
echo "Done. Restart Claude Code (or start a new session) to pick up /autoskill."
echo ""
echo "Usage:"
echo "  /autoskill fix the login crash on empty password"
echo "  /autoskill add tests for the payment module"
echo "  /autoskill   (infers from current conversation)"
