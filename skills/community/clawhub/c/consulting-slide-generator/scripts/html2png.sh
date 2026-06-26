#!/usr/bin/env bash
# html2png.sh - HTML to PNG conversion using Chrome headless
# Usage: html2png.sh <input.html> [output.png]
set -euo pipefail

INPUT="${1:?Usage: html2png.sh <input.html> [output.png]}"
OUTPUT="${2:-${INPUT%.html}.png}"

# Ensure absolute path
if [[ ! "$INPUT" = /* ]]; then
  INPUT="$(pwd)/$INPUT"
fi

google-chrome --headless --disable-gpu \
  --screenshot="$OUTPUT" \
  --window-size=1200,675 \
  "file://$INPUT" 2>/dev/null

echo "✓ $OUTPUT"
