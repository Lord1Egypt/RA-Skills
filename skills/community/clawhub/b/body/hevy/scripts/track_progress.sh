#!/bin/bash

# Track progress for a specific exercise
set -e

EXERCISE="${1:-}"
METRIC="${2:-weight}"
OUTPUT_FORMAT="${3:-json}"

if [ -z "$EXERCISE" ]; then
    echo "❌ Usage: $0 '<exercise-name>' [weight|1rm] [json|table]"
    echo "💡 Example: $0 'Bench Press' weight json"
    exit 1
fi

echo "📈 Tracking progress for: $EXERCISE"

if ! command -v hevycli >/dev/null 2>&1; then
    echo "❌ hevycli not found. Run install_hevycli.sh first."
    exit 1
fi

# Track progress
if [ "$METRIC" = "1rm" ]; then
    hevycli stats progress "$EXERCISE" --metric 1rm --output "$OUTPUT_FORMAT"
else
    hevycli stats progress "$EXERCISE" --output "$OUTPUT_FORMAT"
fi