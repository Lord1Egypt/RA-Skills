#!/bin/bash
# ClawHub skill installer for dchat-clawhub
set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SKILL_DIR"

# Only install production dependencies (nkn-sdk, better-sqlite3, form-data).
# TypeScript and dev tools are NOT needed — dist/ is pre-built and shipped.
echo "[dchat] Installing production dependencies..."
npm install --omit=dev

# Verify the pre-built CLI exists
if [ ! -f dist/cli.js ]; then
  echo "[dchat] ERROR: dist/cli.js not found. The skill package may be corrupt."
  exit 1
fi

echo "[dchat] Generating bot identity..."
node dist/cli.js init

echo "[dchat] Installed successfully."
