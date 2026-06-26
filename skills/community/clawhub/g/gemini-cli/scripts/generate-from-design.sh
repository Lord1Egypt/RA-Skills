#!/bin/bash
# Generate code from design images or PDFs using Gemini CLI

set -e

if [ $# -lt 2 ]; then
  echo "Usage: $0 <image-or-pdf-file> <template> [output-dir]"
  echo ""
  echo "Examples:"
  echo "  $0 design.png react                    # Generate React component"
  echo "  $0 design.png vue ./components        # Generate Vue component to directory"
  echo "  $0 api-spec.pdf typescript ./src      # Generate TypeScript API from PDF"
  echo ""
  echo "Templates: react, vue, express, next, svelte, html, typescript, python, etc."
  exit 1
fi

FILE="$1"
TEMPLATE="$2"
OUTPUT_DIR="${3:-.}"

if [ -z "$GEMINI_API_KEY" ]; then
  echo "❌ Error: GEMINI_API_KEY environment variable not set"
  echo "Set it with: export GEMINI_API_KEY='your-key'"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "❌ Error: File not found: $FILE"
  exit 1
fi

# Determine if image or PDF
if [[ "$FILE" == *.pdf ]]; then
  SOURCE_TYPE="PDF"
  SOURCE_FLAG="--from-pdf"
elif [[ "$FILE" == *.png ]] || [[ "$FILE" == *.jpg ]] || [[ "$FILE" == *.jpeg ]] || [[ "$FILE" == *.webp ]]; then
  SOURCE_TYPE="Image"
  SOURCE_FLAG="--from-image"
else
  echo "❌ Error: Unsupported file type. Use .pdf, .png, .jpg, .jpeg, or .webp"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🎨 Generating $TEMPLATE code from $SOURCE_TYPE: $FILE"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Generate code
OUTPUT_FILE="$OUTPUT_DIR/generated-${TEMPLATE}-$(date +%s).code"

echo "⏳ Generating... (this may take a moment)"

if gemini create $SOURCE_FLAG "$FILE" --template "$TEMPLATE" --save "$OUTPUT_FILE" 2>/dev/null; then
  echo "✅ Generation successful!"
  echo ""
  echo "📄 Output file: $OUTPUT_FILE"
  echo ""
  echo "Preview:"
  echo "---"
  head -20 "$OUTPUT_FILE"
  echo "..."
  echo "---"
  echo ""
  echo "Full file: cat $OUTPUT_FILE"
else
  echo "❌ Generation failed"
  exit 1
fi
