#!/usr/bin/env bash
# Capture logcat with common filters
# Usage:
#   logcat_capture.sh all [output_file] [serial]
#   logcat_capture.sh crash [output_file] [serial]
#   logcat_capture.sh app <package> [output_file] [serial]
#   logcat_capture.sh tag <TAG> [output_file] [serial]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/adb_env.sh"

if [ -z "$ADB_BIN" ]; then
  echo "ADB not found. Run: bash $SCRIPT_DIR/install_adb.sh"
  exit 1
fi

MODE="${1:-all}"
shift || true

# Parse positional args based on mode
case "$MODE" in
  app)
    PKG="${1:-}"
    if [ -z "$PKG" ]; then echo "Usage: logcat_capture.sh app <package> [output_file] [serial]"; exit 1; fi
    shift
    OUTPUT="${1:-}"
    [ -n "${1:-}" ] && shift
    SERIAL="${1:-}"
    ;;
  tag)
    TAG="${1:-}"
    if [ -z "$TAG" ]; then echo "Usage: logcat_capture.sh tag <TAG> [output_file] [serial]"; exit 1; fi
    shift
    OUTPUT="${1:-}"
    [ -n "${1:-}" ] && shift
    SERIAL="${1:-}"
    ;;
  all|crash)
    OUTPUT="${1:-}"
    [ -n "${1:-}" ] && shift
    SERIAL="${1:-}"
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Modes: all | crash | app <package> | tag <TAG>"
    exit 1
    ;;
esac

SERIAL_FLAG=""
[ -n "${SERIAL:-}" ] && SERIAL_FLAG="-s $SERIAL"

# Build command
CMD="$ADB_BIN $SERIAL_FLAG logcat -d"

case "$MODE" in
  crash) CMD="$CMD -b crash" ;;
  app)
    PID=$($ADB_BIN $SERIAL_FLAG shell pidof "$PKG" 2>/dev/null || echo "")
    if [ -z "$PID" ]; then echo "Process not running: $PKG"; exit 1; fi
    CMD="$CMD --pid=$PID"
    ;;
  tag) CMD="$CMD -s $TAG" ;;
esac

if [ -n "$OUTPUT" ]; then
  eval "$CMD" > "$OUTPUT"
  LINES=$(wc -l < "$OUTPUT" | tr -d ' ')
  echo "Captured $LINES lines -> $OUTPUT"
else
  eval "$CMD"
fi
