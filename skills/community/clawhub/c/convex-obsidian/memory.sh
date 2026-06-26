#!/bin/bash
# Hybrid Memory Search - CLI Wrapper
# Usage: ./memory.sh [search|save|save-obsidian|stats] [args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"
PYTHON="$VENV_PATH/bin/python"

# Create venv if needed
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    "$VENV_PATH/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
fi

# Run command
exec "$PYTHON" "$SCRIPT_DIR/memory.py" "$@"
