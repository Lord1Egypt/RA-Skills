#!/bin/bash
set -e
# ClawDef — Minimal Installer
# Only copies files and installs npm dependencies.
# Only copies local files and runs npm install.

CLAWDEF_DIR="${CLAWDEF_INSTALL_DIR:-/opt/openclaw-monitor}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NODE_BIN="${NVM_DIR:-$HOME/.nvm}/current/bin/node"

if [ -z "$NODE_BIN" ] || [ ! -x "$NODE_BIN" ]; then
  NODE_BIN=$(which node 2>/dev/null || true)
fi
if [ -z "$NODE_BIN" ]; then
  echo "Node.js v18+ required. Install: https://nodejs.org"
  exit 1
fi
echo "Node: $($NODE_BIN --version)"

mkdir -p "$CLAWDEF_DIR/data" "$CLAWDEF_DIR/public/lib"
cp "$SKILL_DIR/scripts/server.js" "$CLAWDEF_DIR/server.js"
cp "$SKILL_DIR/scripts/package.json" "$CLAWDEF_DIR/package.json"
cp "$SKILL_DIR/public/index.html" "$CLAWDEF_DIR/public/index.html"
cp "$SKILL_DIR/public/lib/chart.min.js" "$CLAWDEF_DIR/public/lib/chart.min.js"

cd "$CLAWDEF_DIR"
npm install --production

echo "ClawDef files ready at $CLAWDEF_DIR"
echo "Start: $NODE_BIN $CLAWDEF_DIR/server.js"
echo "Open: http://localhost:3456"
