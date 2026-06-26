#!/usr/bin/env bash
# Setup defi-yield-monitor: clone repo + create venv + install deps + init config
set -euo pipefail

REPO_URL="https://github.com/reed1898/defi-yield-monitor.git"
DEFAULT_DIR="${DEFI_MONITOR_DIR:-$HOME/.openclaw/workspace/projects/defi-yield-monitor}"

DIR="${1:-$DEFAULT_DIR}"

if [ -d "$DIR/.git" ]; then
  echo "✔ Project already exists at $DIR, pulling latest..."
  cd "$DIR" && git pull --ff-only origin main 2>/dev/null || true
else
  echo "Cloning $REPO_URL → $DIR"
  git clone "$REPO_URL" "$DIR"
fi

cd "$DIR"

if [ ! -d ".venv" ]; then
  echo "Creating virtualenv..."
  python3 -m venv .venv
fi

echo "Installing dependencies..."
.venv/bin/pip install -q requests>=2.32.0

if [ ! -f "config/config.json" ]; then
  cp config/config.example.json config/config.json
  echo "⚠️  Created config/config.json from example. Edit it to add your wallet addresses."
else
  echo "✔ config/config.json already exists"
fi

echo ""
echo "✅ Setup complete!"
echo "   Project: $DIR"
echo "   Config:  $DIR/config/config.json"
echo ""
echo "Next: edit config.json with your wallet addresses, then run:"
echo "   cd $DIR && .venv/bin/python main.py --config config/config.json"
