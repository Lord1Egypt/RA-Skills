#!/bin/bash
# macOS setup script for screen-vision skill

set -e

echo "=== Screen-Vision macOS Setup ==="
echo ""

# Check Homebrew
if ! command -v brew &>/dev/null; then
    echo "ERROR: Homebrew required. Install from https://brew.sh"
    exit 1
fi

# Install cliclick (mouse/keyboard automation)
echo "[1/3] Installing cliclick..."
brew install cliclick 2>/dev/null || echo "  Already installed"

# Install Python dependencies
echo "[2/3] Installing Python dependencies..."
pip3 install --quiet Pillow numpy 2>/dev/null || pip install --quiet Pillow numpy

# Verify
echo "[3/3] Verifying..."
command -v cliclick && echo "  ✅ cliclick"
command -v screencapture && echo "  ✅ screencapture (built-in)"
python3 -c "from PIL import Image; print('  ✅ Pillow')" 2>/dev/null

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "⚠️  IMPORTANT: Grant these permissions:"
echo "  System Preferences → Privacy & Security → Accessibility → Add Terminal/OpenClaw"
echo "  System Preferences → Privacy & Security → Screen Recording → Add Terminal/OpenClaw"
