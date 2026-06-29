#!/usr/bin/env bash
# Set up the Python venv for AI Capsule.
# Safe to re-run — skips if venv already exists and packages are current.
#
# Usage:
#   bash scripts/setup-env.sh

set -e
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$SKILL_DIR/.venv"

# Find Python 3.9+
PYTHON=""
for cmd in python3.12 python3.11 python3.10 python3.9 python3; do
  if command -v "$cmd" &>/dev/null; then
    ok=$("$cmd" -c "import sys; print(sys.version_info >= (3,9))" 2>/dev/null || echo False)
    [ "$ok" = "True" ] && PYTHON="$cmd" && break
  fi
done
[ -z "$PYTHON" ] && echo "ERROR: Python 3.9+ not found. Install it first." && exit 1

echo "Python: $($PYTHON --version)"
[ ! -d "$VENV" ] && "$PYTHON" -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$SKILL_DIR/requirements.txt"
echo "Done. Venv: $VENV"
