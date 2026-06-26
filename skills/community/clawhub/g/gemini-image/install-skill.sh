#!/usr/bin/env bash
# Install gemini-image as an OpenClaw / Clawdbot skill
set -euo pipefail

SKILL_NAME="gemini-image"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Detect skill directory
if [ -d "$HOME/.openclaw/skills" ]; then
    SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"
elif [ -d "$HOME/.clawdbot/skills" ]; then
    SKILL_DIR="$HOME/.clawdbot/skills/$SKILL_NAME"
else
    # Default to openclaw
    SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"
    mkdir -p "$HOME/.openclaw/skills"
fi

echo "Installing $SKILL_NAME to $SKILL_DIR..."

# Create skill directory
mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/references"

# Copy files
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$SCRIPT_DIR/scripts/generate.py" "$SKILL_DIR/scripts/generate.py"
cp "$SCRIPT_DIR/scripts/batch.py" "$SKILL_DIR/scripts/batch.py"
cp "$SCRIPT_DIR/references/prompting.md" "$SKILL_DIR/references/prompting.md"

echo "✓ Installed to $SKILL_DIR"
echo ""
echo "Setup:"
echo "  1. Get a Gemini API key: https://aistudio.google.com/apikey"
echo "  2. Set it: export GEMINI_API_KEY=\"your-key\""
echo "     Or add to your OpenClaw config under skills.gemini-image.env"
echo "  3. Make sure 'uv' is installed: brew install uv"
echo ""
echo "Quick test:"
echo "  uv run $SKILL_DIR/scripts/generate.py -p \"a cat in a top hat\" -o test.png"
