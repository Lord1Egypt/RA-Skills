#!/usr/bin/env bash
set -euo pipefail

# Write/append markdown memory then trigger immediate tagging for that file.
# Usage:
#   memory-write-tag.sh <workspace> <file> <mode:write|append> <content-file>

WORKSPACE="${1:-}"
TARGET="${2:-}"
MODE="${3:-append}"
CONTENT_FILE="${4:-}"

if [[ -z "$WORKSPACE" || -z "$TARGET" || -z "$CONTENT_FILE" ]]; then
  echo "Usage: $0 <workspace> <file> <mode:write|append> <content-file>"
  exit 2
fi

ABS_TARGET="$TARGET"
if [[ "$TARGET" != /* ]]; then
  ABS_TARGET="$WORKSPACE/$TARGET"
fi

mkdir -p "$(dirname "$ABS_TARGET")"
if [[ "$MODE" == "write" ]]; then
  cat "$CONTENT_FILE" > "$ABS_TARGET"
else
  cat "$CONTENT_FILE" >> "$ABS_TARGET"
fi

SKILL_DIR="$WORKSPACE/skills/duru-memory"
TAGGER="$SKILL_DIR/scripts/memory-auto-tag.py"
if [[ -x "$TAGGER" ]]; then
  (cd "$SKILL_DIR" && uv run python "$TAGGER" "$WORKSPACE" --mode tag --files "$ABS_TARGET")
fi

echo "ok: $ABS_TARGET"
