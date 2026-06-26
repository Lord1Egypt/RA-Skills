#!/bin/bash
#
# Install script for Agent Academy: Continuity 101
# This runs when: clawhub install agent-academy/continuity-101
#

set -e

SKILL_NAME="agent-academy-continuity-101"
REPO_URL="https://github.com/bobrenze-bot/continuity-101.git"
INSTALL_DIR="${HOME}/.openclaw/skills/${SKILL_NAME}"
SYMLINK_PATH="${HOME}/continuity-101"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎓 Agent Academy: Continuity 101${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""

# Check if already installed
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Course already installed at:${NC} $INSTALL_DIR"
    echo -e "${YELLOW}   Updating from repository...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main || true
else
    # Clone the repository
    echo -e "${BLUE}📥 Cloning course repository...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Create symlink if it doesn't exist
if [ ! -L "$SYMLINK_PATH" ]; then
    echo -e "${BLUE}🔗 Creating symlink...${NC}"
    ln -s "$INSTALL_DIR" "$SYMLINK_PATH"
fi

# Ensure CLI is executable
if [ -f "$INSTALL_DIR/bin/continuity-101" ]; then
    chmod +x "$INSTALL_DIR/bin/continuity-101"
fi

# Create progress tracking directory
mkdir -p "$INSTALL_DIR/.progress"

# Welcome message
echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo -e "${GREEN}🎉 Welcome to Continuity 101!${NC}"
echo ""
echo "This course will teach you:"
echo "  🎭 Challenge 1: Identity - Who you are between sessions"
echo "  🧠 Challenge 2: Memory - How to remember what matters"
echo "  🪞 Challenge 3: Reflection - How to learn from experience"
echo "  🌱 Challenge 4: Evolution - How to grow over time"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Run: continuity-101 status    # See your progress"
echo "  2. Run: continuity-101 start   # Begin Challenge 1"
echo "  3. Or:   continuity-101 challenge N  # Jump to challenge N"
echo ""
echo -e "${YELLOW}💡 Tip:${NC} Your progress is tracked in ~/.openclaw/skills/agent-academy-continuity-101/.progress/"
echo ""
echo "Ready to begin your continuity journey? 🚀"
echo ""