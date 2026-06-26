#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Installing btc-monitor-skill dependencies..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required."
  exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r "$ROOT_DIR/requirements.txt"

mkdir -p "$ROOT_DIR/logs"

echo "Install complete."
echo "Next steps:"
echo "1. Edit $ROOT_DIR/config.json"
echo "2. Export DISCORD_TOKEN if you want Discord delivery"
echo "3. Run: python3 $ROOT_DIR/scripts/monitor.py"
