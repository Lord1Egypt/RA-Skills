#!/usr/bin/env bash
# Take a screenshot and pull to local directory
# Usage: screenshot.sh [output_dir] [serial]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/adb_env.sh"

if [ -z "$ADB_BIN" ]; then
  echo "ADB not found. Run: bash $SCRIPT_DIR/install_adb.sh"
  exit 1
fi

OUTPUT_DIR="${1:-.}"
SERIAL_FLAG=""
[ -n "${2:-}" ] && SERIAL_FLAG="-s $2"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REMOTE_PATH="/sdcard/screenshot_${TIMESTAMP}.png"
LOCAL_PATH="${OUTPUT_DIR}/screenshot_${TIMESTAMP}.png"

mkdir -p "$OUTPUT_DIR"

$ADB_BIN $SERIAL_FLAG shell screencap "$REMOTE_PATH"
$ADB_BIN $SERIAL_FLAG pull "$REMOTE_PATH" "$LOCAL_PATH"
$ADB_BIN $SERIAL_FLAG shell rm "$REMOTE_PATH"

echo "Screenshot saved: $LOCAL_PATH"
