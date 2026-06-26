#!/usr/bin/env bash
# Setup: create venv and install dependencies for airbnb-agent skill.
# Run once: bash scripts/setup.sh
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$SKILL_DIR/.venv"

if [ -d "$VENV" ]; then
    echo "✅ venv already exists at $VENV"
else
    echo "🔧 Creating venv at $VENV..."
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install --quiet pyairbnb curl-cffi
    echo "✅ Dependencies installed"
fi

echo "📍 Use: $VENV/bin/python3 scripts/search.py ..."
echo "📍 Use: $VENV/bin/python3 scripts/details.py ..."
