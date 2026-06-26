#!/bin/bash
# html-to-pdf.sh — Convert an HTML file to PDF using Chrome headless
# Usage: ./html-to-pdf.sh <input.html> [output.pdf]

set -e

INPUT="$1"
OUTPUT="${2:-${INPUT%.html}.pdf}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <input.html> [output.pdf]"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT"
  exit 1
fi

# Find Chrome
CHROME=""
for candidate in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  "$(which google-chrome 2>/dev/null)" \
  "$(which chromium 2>/dev/null)"; do
  if [ -x "$candidate" ] 2>/dev/null; then
    CHROME="$candidate"
    break
  fi
done

if [ -z "$CHROME" ]; then
  echo "Error: No Chrome/Chromium browser found"
  exit 1
fi

# Convert relative path to absolute for file:// URL
INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

# Run Chrome headless to generate PDF
"$CHROME" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --print-to-pdf="$OUTPUT" \
  --print-to-pdf-no-header \
  --run-all-compositor-stages-before-draw \
  --virtual-time-budget=5000 \
  "file://$INPUT_ABS" \
  2>/dev/null

if [ -f "$OUTPUT" ]; then
  echo "PDF generated: $OUTPUT"
  echo "Size: $(du -h "$OUTPUT" | cut -f1)"
else
  echo "Error: PDF generation failed"
  exit 1
fi
