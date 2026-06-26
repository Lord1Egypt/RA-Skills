#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/dario-github/biomorphic-memory.git"
INSTALL_DIR="${BIOMORPHIC_INSTALL_DIR:-$HOME/.biomorphic-memory}"

echo "🧠 Installing Biomorphic Memory — Brain-Inspired Agent Memory"
echo "============================================================="

python3 -c "import sys; assert sys.version_info >= (3, 11), f'Python 3.11+ required, got {sys.version}'" 2>/dev/null || {
    echo "❌ Python 3.11+ is required"
    exit 1
}

if [ -d "$INSTALL_DIR" ]; then
    echo "📦 Updating existing installation..."
    cd "$INSTALL_DIR" && git pull --ff-only 2>/dev/null || {
        rm -rf "$INSTALL_DIR"
        git clone "$REPO" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    }
else
    git clone "$REPO" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

pip install -e . 2>/dev/null || { echo "❌ Install failed"; exit 1; }

echo "✅ Biomorphic Memory installed at: $INSTALL_DIR"
