#!/usr/bin/env bash
# Garmin Frisbee Analysis - Clawdbot Skill Installation
# Run this after cloning the skill to your Clawdbot skills directory

set -e  # Exit on error

echo "🥏 Installing Garmin Frisbee Analysis Skill..."
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Install Python dependencies
echo
echo "📦 Installing Python dependencies..."

if pip3 install --user -r requirements.txt 2>/dev/null; then
    echo "✓ Dependencies installed (--user)"
elif pip3 install --break-system-packages -r requirements.txt 2>/dev/null; then
    echo "✓ Dependencies installed (--break-system-packages)"
elif pip3 install -r requirements.txt 2>/dev/null; then
    echo "✓ Dependencies installed (system-wide)"
else
    echo "❌ Failed to install Python dependencies"
    echo "   Try manually: pip3 install --user -r requirements.txt"
    exit 1
fi

# Success
echo
echo "✅ Installation complete!"
echo
echo "Next steps:"
echo "  1. Set your Garmin credentials as environment variables:"
echo "     export GARMIN_EMAIL=\"your-email@example.com\""
echo "     export GARMIN_PASSWORD=\"your-password\""
echo "     (Add these to ~/.zshrc or ~/.bashrc to persist them)"
echo
echo "  2. Authenticate:"
echo "     python3 scripts/garmin_auth.py login"
echo
echo "  3. Test:"
echo "     python3 scripts/garmin_data.py summary --days 7"
echo
echo "📖 Read SKILL.md for full documentation"
