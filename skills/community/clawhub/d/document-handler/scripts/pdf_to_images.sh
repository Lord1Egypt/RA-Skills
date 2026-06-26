#!/bin/bash
# Convert PDF pages to images

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <pdf> <output_dir> [dpi=150]"
    exit 1
fi

PDF="$1"
OUTPUT_DIR="$2"
DPI="${3:-150}"

if [[ ! -f "$PDF" ]]; then
    echo "Error: PDF not found: $PDF" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

BASENAME=$(basename "$PDF" .pdf)

echo "Converting $PDF to images at ${DPI} DPI..."

pdftoppm -png -r "$DPI" "$PDF" "${OUTPUT_DIR}/${BASENAME}"

echo "Done! Images saved to: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"