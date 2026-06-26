#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RUNTIME_DIR="${CDP_GMAIL_DELIVERY_RUNTIME_DIR:-$SKILL_DIR/.runtime/pupp-mail}"

mkdir -p "$RUNTIME_DIR"
cd "$RUNTIME_DIR"

if [ ! -f package.json ]; then
  npm init -y >/dev/null 2>&1
fi

npm install --no-fund --no-audit puppeteer-core@24

echo "CDP_GMAIL_DELIVERY_RUNTIME_OK"
echo "RUNTIME_DIR=$RUNTIME_DIR"
