#!/bin/bash

# Get workout statistics and summaries
set -e

PERIOD="${1:-month}"
OUTPUT_FORMAT="${2:-json}"

echo "📊 Getting workout stats for period: $PERIOD"

if ! command -v hevycli >/dev/null 2>&1; then
    echo "❌ hevycli not found. Run install_hevycli.sh first."
    exit 1
fi

echo "=== Workout Summary ==="
hevycli stats summary --period "$PERIOD" --output "$OUTPUT_FORMAT"

echo ""
echo "=== Personal Records ==="
hevycli stats records --output "$OUTPUT_FORMAT"

echo ""
echo "=== Workout Count ==="
hevycli workout count --output "$OUTPUT_FORMAT"