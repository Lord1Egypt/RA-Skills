#!/usr/bin/env bash
# Download Android platform-tools to skill's local tools/ directory (sandbox install)
# No PATH modification, no sudo, no system pollution
# Uninstall: just delete the tools/ directory
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS_DIR="$SKILL_DIR/tools"

OS=$(uname -s)
case "$OS" in
    Darwin) URL="https://dl.google.com/android/repository/platform-tools-latest-darwin.zip" ;;
    Linux)  URL="https://dl.google.com/android/repository/platform-tools-latest-linux.zip" ;;
    *)      echo "Unsupported OS: $OS"; exit 1 ;;
esac

# Check if already installed
if [ -x "$TOOLS_DIR/platform-tools/adb" ]; then
    echo "ADB already installed:"
    "$TOOLS_DIR/platform-tools/adb" version
    exit 0
fi

mkdir -p "$TOOLS_DIR"
ZIP="$TOOLS_DIR/platform-tools.zip"

echo "Downloading Android platform-tools..."
curl -# -L -o "$ZIP" "$URL"

echo "Extracting..."
unzip -qo "$ZIP" -d "$TOOLS_DIR"
rm -f "$ZIP"
chmod +x "$TOOLS_DIR/platform-tools/adb"
chmod +x "$TOOLS_DIR/platform-tools/fastboot" 2>/dev/null || true

echo ""
echo "ADB installed to: $TOOLS_DIR/platform-tools/adb"
"$TOOLS_DIR/platform-tools/adb" version
echo ""
echo "To uninstall: rm -rf \"$TOOLS_DIR\""
