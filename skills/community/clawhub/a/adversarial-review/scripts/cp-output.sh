#!/bin/bash
# adversarial-review: Copy final output document to a destination
#
# Usage: cp-output.sh <session-name> <destination-path>
#
# Finds the most recent .md file in {session}/output/
# Copies it to destination (creates directory if needed)
# Prints full destination path on completion
#
# Examples:
#   cp-output.sh 2026-03-06-bitwage-taxonomy ~/Desktop
#   cp-output.sh 2026-03-06-bitwage-taxonomy ~/Projects/bitwage-intelligence/docs/
#   cp-output.sh 2026-03-06-bitwage-taxonomy /tmp/for-team-review/

set -e

REVIEWS_DIR=~/.openclaw/workspace/reviews

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: cp-output.sh <session-name> <destination-path>"
  echo ""
  echo "Available sessions:"
  ls "$REVIEWS_DIR" 2>/dev/null | while read -r s; do
    count=$(ls "$REVIEWS_DIR/$s/output/" 2>/dev/null | wc -l | tr -d ' ')
    echo "  $s ($count output file(s))"
  done
  exit 1
fi

SESSION_NAME="$1"
DESTINATION="$2"
SESSION_DIR="${REVIEWS_DIR}/${SESSION_NAME}"
OUTPUT_DIR="${SESSION_DIR}/output"

if [ ! -d "$SESSION_DIR" ]; then
  echo "Error: Session not found: $SESSION_DIR"
  echo ""
  echo "Available sessions:"
  ls "$REVIEWS_DIR" 2>/dev/null
  exit 1
fi

if [ ! -d "$OUTPUT_DIR" ]; then
  echo "Error: Output directory not found: $OUTPUT_DIR"
  echo "Has v2 been written yet? Write output/{slug}-v2.md first."
  exit 1
fi

# Find the most recent .md file in output/
LATEST=$(ls -t "$OUTPUT_DIR"/*.md 2>/dev/null | head -1)

if [ -z "$LATEST" ]; then
  echo "Error: No .md files found in $OUTPUT_DIR"
  echo "Has v2 been written yet?"
  exit 1
fi

FILENAME=$(basename "$LATEST")

# Expand destination path
DEST=$(eval echo "$DESTINATION")

# Create destination if it doesn't exist
mkdir -p "$DEST"

cp "$LATEST" "$DEST/$FILENAME"

echo ""
echo "✓ Copied: $FILENAME"
echo "  From: $LATEST"
echo "  To:   $DEST/$FILENAME"
echo ""
