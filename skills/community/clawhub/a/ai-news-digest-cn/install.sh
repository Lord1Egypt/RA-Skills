#!/usr/bin/env bash
# ai-news-digest skill installer (Claude Code)
# Usage: curl -fsSL https://raw.githubusercontent.com/yan1sanjin/ai-news-digest/main/install.sh | bash

set -e

SKILL_NAME="ai-news-digest"
SKILL_DIR="$HOME/.claude/skills/$SKILL_NAME"
SKILL_URL="https://raw.githubusercontent.com/yan1sanjin/ai-news-digest/main/SKILL.md"

# Check Claude Code presence
if [ ! -d "$HOME/.claude" ]; then
  echo "Error: ~/.claude not found. Is Claude Code installed?"
  echo "       Install from: https://docs.claude.com/claude-code"
  exit 1
fi

# Create skill dir
mkdir -p "$SKILL_DIR"

# Download SKILL.md
echo "Downloading ai-news-digest skill..."
if ! curl -fsSL "$SKILL_URL" -o "$SKILL_DIR/SKILL.md"; then
  echo "Error: failed to download from $SKILL_URL"
  echo "       Check your network or download SKILL.md manually from:"
  echo "       https://github.com/yan1sanjin/ai-news-digest"
  exit 1
fi

echo ""
echo "✓ Installed to $SKILL_DIR/SKILL.md"
echo ""
echo "Try it in Claude Code:"
echo "  生成今日 AI 日报"
echo ""
echo "Output will be saved to ~/Desktop/ai-news/YYYY-MM-DD.md"
echo ""
