#!/bin/bash
# Batch analyze files with Gemini CLI

set -e

OPERATION="${1:-explain}"  # explain, review, fix, test
INPUT_DIR="${2:-.}"        # Directory to analyze
OUTPUT_DIR="${3:-./analysis}"

if [ -z "$GEMINI_API_KEY" ]; then
  echo "❌ Error: GEMINI_API_KEY environment variable not set"
  echo "Set it with: export GEMINI_API_KEY='your-key'"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🔍 Batch analyzing files in: $INPUT_DIR"
echo "📋 Operation: $OPERATION"
echo "📁 Output directory: $OUTPUT_DIR"
echo ""

# Find all code files
FILES=$(find "$INPUT_DIR" -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" \) | grep -v node_modules | sort)

TOTAL=$(echo "$FILES" | wc -l)
COUNT=0

if [ "$TOTAL" -eq 0 ]; then
  echo "⚠️  No code files found in $INPUT_DIR"
  exit 1
fi

echo "📊 Found $TOTAL files to analyze"
echo ""

# Process each file
for file in $FILES; do
  COUNT=$((COUNT + 1))
  
  # Create output filename
  SAFE_NAME=$(echo "$file" | sed 's/[^a-zA-Z0-9_.-]/-/g')
  OUTPUT_FILE="$OUTPUT_DIR/${SAFE_NAME}.md"
  
  echo "[$COUNT/$TOTAL] Analyzing: $file"
  
  case "$OPERATION" in
    explain)
      gemini code --explain "$file" --format markdown > "$OUTPUT_FILE" 2>/dev/null
      ;;
    review)
      gemini code --review "$file" --format markdown > "$OUTPUT_FILE" 2>/dev/null
      ;;
    fix)
      gemini code --fix "$file" --format markdown > "$OUTPUT_FILE" 2>/dev/null
      ;;
    test)
      gemini code --test "$file" --format markdown > "$OUTPUT_FILE" 2>/dev/null
      ;;
    *)
      echo "❌ Unknown operation: $OPERATION"
      exit 1
      ;;
  esac
  
  echo "       ✅ Saved to: $OUTPUT_FILE"
done

echo ""
echo "✨ Analysis complete!"
echo "📊 Results saved to: $OUTPUT_DIR"
echo ""
echo "View results:"
echo "  ls -la $OUTPUT_DIR"
echo "  cat $OUTPUT_DIR/*.md"
