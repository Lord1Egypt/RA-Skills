#!/usr/bin/env bash
set -euo pipefail

WIN_PS="${WIN_PS:-/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe}"
WIN_SCRIPT='C:\OpenClaw\capture-screen.ps1'
OUT_WIN='C:\OpenClaw\latest-screen.png'
OUT_WSL="${OUT_WSL:-/mnt/c/OpenClaw/latest-screen.png}"
STAGE_DIR="${STAGE_DIR:-/home/lhs/.openclaw/workspace/tmp-media}"
STAMP="$(date +%Y%m%d-%H%M%S)"
STAGED_PATH="$STAGE_DIR/latest-screen-$STAMP.png"

if [[ ! -x "$WIN_PS" ]]; then
  echo "PowerShell not found at: $WIN_PS" >&2
  exit 1
fi

"$WIN_PS" -NoProfile -ExecutionPolicy Bypass -File "$WIN_SCRIPT" -OutputPath "$OUT_WIN" >/dev/null

if [[ ! -f "$OUT_WSL" ]]; then
  echo "Screenshot file not found at: $OUT_WSL" >&2
  exit 1
fi

mkdir -p "$STAGE_DIR"
cp "$OUT_WSL" "$STAGED_PATH"
printf '%s\n' "$STAGED_PATH"
