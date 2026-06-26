#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEST_DIR="${CODEX_HOME:-$HOME/.codex}/skills/computer-use-windows"

mkdir -p "$DEST_DIR"
rsync -a --delete "$SRC_DIR/" "$DEST_DIR/"
printf 'Installed skill to %s\n' "$DEST_DIR"
