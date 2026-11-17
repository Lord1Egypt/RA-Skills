#!/usr/bin/env bash
# batch-generate.sh - Batch generate images from a prompt file
# Usage: ./batch-generate.sh prompts.txt SIZE [OUTPUT_DIR]
# 
# Prompt file format (one prompt per line):
#   A cat sitting on a windowsill
#   A sunset over the ocean
#   A futuristic city at night

set -euo pipefail

PROMPT_FILE="${1:-}"
SIZE="${2:-1024x768}"
OUTPUT_DIR="${3:-./batch_output}"

if [ -z "$PROMPT_FILE" ]; then
  echo "Usage: $0 <prompt_file> [size] [output_dir]"
  echo "   prompt_file: Text file with one prompt per line"
  echo "   size: Output size (default: 1024x768)"
  echo "   output_dir: Output directory (default: ./batch_output)"
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "ERROR: Prompt file '$PROMPT_FILE' not found"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🎨 Batch Image Generation"
echo "========================"
echo "Prompts: $PROMPT_FILE"
echo "Size: $SIZE"
echo "Output: $OUTPUT_DIR"
echo ""

COUNTER=0
SUCCESS=0
FAILED=0

while IFS= read -r PROMPT || [ -n "$PROMPT" ]; do
  # Skip empty lines and comments
  [[ -z "$PROMPT" || "$PROMPT" =~ ^# ]] && continue
  
  COUNTER=$((COUNTER + 1))
  OUTPUT_FILE="$OUTPUT_DIR/image_${COUNTER}.png"
  
  echo "[$COUNTER] Generating: ${PROMPT:0:60}..."
  
  if ./agnes-image.sh text "$PROMPT" "$SIZE" "$OUTPUT_FILE" 2>&1; then
    SUCCESS=$((SUCCESS + 1))
    echo "   ✓ Saved to: $OUTPUT_FILE"
  else
    FAILED=$((FAILED + 1))
    echo "   ❌ Failed"
  fi
  echo ""
done < "$PROMPT_FILE"

echo "========================"
echo "Batch Complete!"
echo "  Total: $COUNTER"
echo "  Success: $SUCCESS"
echo "  Failed: $FAILED"
echo "  Output: $OUTPUT_DIR"
