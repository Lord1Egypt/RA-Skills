#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-$HOME/.openclaw/skills/agent-genesis}"
REPO_URL="https://github.com/likwid-fi/agent-genesis.git"
BRANCH="main"

mkdir -p "$(dirname "$TARGET_DIR")"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "[likwid-fi] Existing repo found at $TARGET_DIR"
  git -C "$TARGET_DIR" pull --ff-only origin "$BRANCH"
else
  echo "[likwid-fi] Cloning repo to $TARGET_DIR"
  git clone -b "$BRANCH" "$REPO_URL" "$TARGET_DIR"
fi

cd "$TARGET_DIR/likwid-fi"

echo "[likwid-fi] Installing runtime dependencies..."
npm install --no-audit --no-fund --omit=dev --omit=optional

echo ""
echo "[likwid-fi] Ready. Run: node likwid-fi.js setup <network> <keyFile> [eoa|smart]"
