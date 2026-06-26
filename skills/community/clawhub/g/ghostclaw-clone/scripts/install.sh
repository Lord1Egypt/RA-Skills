#!/usr/bin/env bash
# scripts/install.sh — Builds the Ghostclaw standalone binary via PyInstaller

set -e

echo "=> Building Ghostclaw Binary..."

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Set up a virtual environment to keep dependencies clean
python3 -m venv venv
source venv/bin/activate

# Install project dependencies from pyproject.toml
pip install --upgrade pip
pip install -e .

# Install PyInstaller
pip install pyinstaller

# Build the standalone binary
# --onefile  → single self-contained executable
# --name     → output binary named "ghostclaw"
# --clean    → clear PyInstaller cache before building
pyinstaller --clean \
            --onefile \
            --name ghostclaw \
            src/ghostclaw/cli/ghostclaw.py

# Install the binary to ~/.local/bin (standard Linux user binary directory)
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"
mv dist/ghostclaw "$INSTALL_DIR/ghostclaw"
chmod +x "$INSTALL_DIR/ghostclaw"

# Clean up PyInstaller build artifacts
rm -rf build dist ghostclaw.spec venv

echo "=> Build successful! Binary installed at $INSTALL_DIR/ghostclaw"
