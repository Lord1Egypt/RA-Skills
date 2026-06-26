#!/bin/bash
# Enhanced Memory Search - CLI Wrapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"
PYTHON="$VENV_PATH/bin/python"

if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
    "$VENV_PATH/bin/pip" install -q requests
fi

exec "$PYTHON" "$SCRIPT_DIR/search.py" "$@"
