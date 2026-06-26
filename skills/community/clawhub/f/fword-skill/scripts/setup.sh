#!/usr/bin/env bash
# Fword skill setup — install dependencies
set -e

echo "=== Fword Setup ==="

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.10+."
    exit 1
fi

# Check Pandoc
if ! command -v pandoc &>/dev/null; then
    echo "Pandoc not found. Attempting to install..."
    if command -v apt &>/dev/null; then
        sudo apt install -y pandoc
    elif command -v brew &>/dev/null; then
        brew install pandoc
    elif command -v pacman &>/dev/null; then
        sudo pacman -S --noconfirm pandoc
    else
        echo "ERROR: Cannot auto-install Pandoc. Please install it manually:"
        echo "  https://pandoc.org/installing.html"
        exit 1
    fi
fi

# Install Python dependencies
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

if [ -f "$REQ_FILE" ]; then
    pip3 install -q -r "$REQ_FILE"
else
    pip3 install -q pypandoc anthropic python-docx rich
fi

echo "=== Fword ready ==="
pandoc --version | head -1
python3 -c "import pypandoc, anthropic, docx; print('All Python deps OK')"
