#!/bin/bash
# Shell wrapper for fb-group-monitor.py
# Locates and activates Python virtual environment, then runs the script.
#
# Virtual environment resolution order:
#   1. FBMON_VENV environment variable (if set)
#   2. .venv/ in the scripts directory (co-located venv)
#   3. System Python (fallback)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Try custom venv path first
if [ -n "$FBMON_VENV" ] && [ -f "$FBMON_VENV/bin/activate" ]; then
    source "$FBMON_VENV/bin/activate"
# Try co-located venv
elif [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

python3 "$SCRIPT_DIR/fb-group-monitor.py" "$@"
