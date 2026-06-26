#!/bin/bash
# Desktop Control Skill - Linux/Mac Setup Script
# Creates Python venv and installs core dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SKILL_DIR"

if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Updating dependencies..."
else
    echo "Creating virtual environment in $SKILL_DIR/.venv ..."
    python3 -m venv .venv
fi

echo "Installing core dependencies..."
.venv/bin/pip install pyautogui pillow pyperclip

# Platform-specific notes
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "Linux detected. You may also need:"
    echo "  sudo apt install python3-tk python3-dev scrot"
    echo "  pip install python-xlib  (for pygetwindow)"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "macOS detected. You may also need:"
    echo "  pip install pyobjc-core pyobjc-framework-Quartz"
    echo "  Grant Accessibility permissions to Terminal/iTerm2 in System Preferences"
fi

echo ""
echo "Setup complete!"
