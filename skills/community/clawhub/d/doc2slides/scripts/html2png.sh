#!/usr/bin/env bash
# Part of doc2slides skill.
# Usage: html2png.sh <input.html> [output.png]
set -euo pipefail

INPUT="${1:?Usage: html2png.sh <input.html> [output.png]}"
OUTPUT="${2:-${INPUT%.html}.png}"

# Ensure absolute path
if [[ ! "$INPUT" = /* ]]; then
  INPUT="$(pwd)/$INPUT"
fi

# Try Chrome first, then Chromium
if command -v google-chrome &> /dev/null; then
  CMD="google-chrome"
elif command -v chromium &> /dev/null; then
  CMD="chromium"
elif command -v chromium-browser &> /dev/null; then
  CMD="chromium-browser"
else
  echo "Error: Chrome/Chromium not found. Please install Chrome or Chromium."
  exit 1
fi

# HD rendering matching HTML container (1920x1080)
# Use 2x scale for high-quality PPT (3840x2160 output)
SCALE="${3:-2}"  # Default 2x, can override with 3rd arg

"$CMD" --headless --disable-gpu --no-sandbox \
  --screenshot="$OUTPUT" \
  --window-size=1920,1080 \
  --force-device-scale-factor=$SCALE \
  "file://$INPUT" 2>/dev/null

echo "✓ Generated: $OUTPUT"
