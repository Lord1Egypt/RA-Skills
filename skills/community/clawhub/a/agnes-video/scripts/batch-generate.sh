#!/usr/bin/env bash
# batch-generate.sh - Batch generate videos from a prompt file
# Usage: ./batch-generate.sh prompts.txt [OUTPUT_DIR]
# 
# Prompt file format (one prompt per line):
#   A cat walking on the beach at sunset
#   A spaceship flying through nebula
#   A flower blooming in time-lapse

set -euo pipefail

PROMPT_FILE="${1:-}"
OUTPUT_DIR="${2:-./batch_output}"

if [ -z "$PROMPT_FILE" ]; then
  echo "Usage: $0 <prompt_file> [output_dir]"
  echo "   prompt_file: Text file with one prompt per line"
  echo "   output_dir: Output directory (default: ./batch_output)"
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: Prompt file '$PROMPT_FILE' not found"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🎬 Batch Video Generation"
echo "========================="
echo "Prompts: $PROMPT_FILE"
echo "Output: $OUTPUT_DIR"
echo ""

COUNTER=0
SUCCESS=0
FAILED=0

while IFS= read -r PROMPT || [ -n "$PROMPT" ]; do
  # Skip empty lines and comments
  [[ -z "$PROMPT" || "$PROMPT" =~ ^# ]] && continue
  
  COUNTER=$((COUNTER + 1))
  OUTPUT_FILE="$OUTPUT_DIR/video_${COUNTER}.mp4"
  
  echo "[$COUNTER] Generating: ${PROMPT:0:60}..."
  
  if ./agnes-video.sh text "$PROMPT" "$OUTPUT_FILE" 2>&1; then
    SUCCESS=$((SUCCESS + 1))
    echo "   ✓ Saved to: $OUTPUT_FILE"
  else
    FAILED=$((FAILED + 1))
    echo "   ❌ Failed"
  fi
  echo ""
done < "$PROMPT_FILE"

echo "========================="
echo "Batch Complete!"
echo "  Total: $COUNTER"
echo "  Success: $SUCCESS"
echo "  Failed: $FAILED"
echo "  Output: $OUTPUT_DIR"
