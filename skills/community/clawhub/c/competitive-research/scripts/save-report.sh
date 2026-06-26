#!/usr/bin/env bash
# save-report.sh
# Saves a competitive intel report to the workspace research directory.
#
# Usage:
#   ./save-report.sh <slug> <report_content_file>
#   ./save-report.sh klaviyo /tmp/report.md
#
# Or pipe content:
#   echo "$REPORT_CONTENT" | ./save-report.sh klaviyo
#
# Output: workspace/research/competitive-intel/YYYY-MM-DD-<slug>.md

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
OUTPUT_DIR="$WORKSPACE/research/competitive-intel"
DATE=$(date +%Y-%m-%d)

# Validate slug argument
if [[ $# -lt 1 ]]; then
  echo "Usage: save-report.sh <slug> [input_file]" >&2
  echo "  slug: short lowercase identifier, e.g. 'klaviyo' or 'dtc-email'" >&2
  exit 1
fi

SLUG="$1"
# Normalize slug: lowercase, replace spaces with hyphens, strip non-alphanumeric except hyphens
SLUG=$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

if [[ -z "$SLUG" ]]; then
  echo "Error: slug is empty after normalization." >&2
  exit 1
fi

OUTPUT_FILE="$OUTPUT_DIR/${DATE}-${SLUG}.md"

# Create output directory if needed
mkdir -p "$OUTPUT_DIR"

# Check for collision
if [[ -f "$OUTPUT_FILE" ]]; then
  echo "Warning: $OUTPUT_FILE already exists. Overwriting." >&2
fi

# Read content from file argument or stdin
if [[ $# -ge 2 ]]; then
  INPUT_FILE="$2"
  if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: input file '$INPUT_FILE' not found." >&2
    exit 1
  fi
  cp "$INPUT_FILE" "$OUTPUT_FILE"
else
  # Read from stdin
  cat > "$OUTPUT_FILE"
fi

echo "Saved: $OUTPUT_FILE"
