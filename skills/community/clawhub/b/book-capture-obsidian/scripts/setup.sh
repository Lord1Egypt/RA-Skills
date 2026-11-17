#!/bin/sh
# Create a private virtualenv for this skill and install its Python packages.
# Safe to re-run; it only touches <skill>/.venv.
set -eu

SKILL_DIR=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
VENV_DIR="$SKILL_DIR/.venv"

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is required" >&2
    exit 2
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
    python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --quiet --upgrade pip
"$VENV_DIR/bin/python" -m pip install --quiet -r "$SKILL_DIR/requirements.txt"

echo "Python: $VENV_DIR/bin/python"
"$VENV_DIR/bin/python" "$SKILL_DIR/scripts/extract_isbn.py" --diagnose-deps
