#!/usr/bin/env bash
set -euo pipefail

# Obsidian Clipper — installer for Claude Code
#
# One-liner install:
#   curl -fsSL https://raw.githubusercontent.com/Gisg/obsidian-clipper/main/setup.sh | bash
#
# Or manual:
#   git clone https://github.com/Gisg/obsidian-clipper.git ~/.claude/skills/obsidian-clipper
#   cd ~/.claude/skills/obsidian-clipper && bash setup.sh

SKILL_DIR="$HOME/.claude/skills/obsidian-clipper"

echo "=== Obsidian Clipper Setup ==="
echo ""

# 1. Clone if not already in the skill directory
if [ -f "$SKILL_DIR/SKILL.md" ]; then
  echo "✓ Already installed at $SKILL_DIR"
else
  # If running from the repo (e.g., user cloned elsewhere), symlink
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  if [ -f "$SCRIPT_DIR/SKILL.md" ] && [ "$SCRIPT_DIR" != "$SKILL_DIR" ]; then
    mkdir -p "$SKILL_DIR"
    ln -sf "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/skill.md"
    echo "✓ Linked skill from $SCRIPT_DIR"
  else
    # Fresh install: clone directly into skills dir
    mkdir -p "$HOME/.claude/skills"
    git clone https://github.com/Gisg/obsidian-clipper.git "$SKILL_DIR"
    echo "✓ Cloned to $SKILL_DIR"
  fi
fi

# 2. Ensure SKILL.md is discoverable as skill.md
if [ -f "$SKILL_DIR/SKILL.md" ] && [ ! -f "$SKILL_DIR/skill.md" ]; then
  ln -sf "$SKILL_DIR/SKILL.md" "$SKILL_DIR/skill.md"
  echo "✓ Created skill.md symlink"
fi

# 3. Create config.yml if missing
if [ ! -f "$SKILL_DIR/config.yml" ]; then
  if [ -f "$SKILL_DIR/config.yml.example" ]; then
    cp "$SKILL_DIR/config.yml.example" "$SKILL_DIR/config.yml"
  fi
  echo ""
  echo "⚠  Please edit your config:"
  echo "   $SKILL_DIR/config.yml"
  echo ""
  echo "   Set vault.base_path to your Obsidian Vault clippings directory, e.g.:"
  echo '   base_path: "/Users/yourname/Vault/My Vault/Clippings"'
else
  echo "✓ config.yml exists"
fi

# 4. Check optional dependencies
echo ""
if command -v defuddle &>/dev/null; then
  echo "✓ defuddle found (Web handler ready)"
else
  echo "○ defuddle not found (optional — install: npm install -g defuddle-cli)"
fi

if command -v python3 &>/dev/null; then
  echo "✓ python3 found (Xiaohongshu handler ready)"
else
  echo "○ python3 not found (needed for Xiaohongshu handler)"
fi

echo ""
echo "✅ Done! Restart Claude Code to load the skill."
echo "   Then paste a URL and say '收藏' or 'clip this'."
