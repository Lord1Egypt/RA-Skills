#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-$HOME/.openclaw/skills/agent-genesis}"
REPO_URL="https://github.com/likwid-fi/agent-genesis.git"

mkdir -p "$(dirname "$TARGET_DIR")"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "[agent-genesis] Existing repo found at $TARGET_DIR"
  git -C "$TARGET_DIR" pull --ff-only origin main
else
  echo "[agent-genesis] Cloning repo to $TARGET_DIR"
  git clone "$REPO_URL" "$TARGET_DIR"
fi

cd "$TARGET_DIR"

echo "[agent-genesis] Installing runtime dependencies..."
npm install --legacy-peer-deps --no-audit --no-fund --omit=dev --omit=optional

echo "[agent-genesis] Installing likwid-fi dependencies..."
cd "$TARGET_DIR/likwid-fi" && npm install --no-audit --no-fund --omit=dev --omit=optional

echo "[agent-genesis] Ready. Example: node genesis.js check_wallet"
