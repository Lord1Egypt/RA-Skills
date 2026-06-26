#!/bin/bash

# Get recent workouts with optional date filtering
set -e

DAYS="${1:-7}"
OUTPUT_FORMAT="${2:-json}"

echo "📊 Fetching last $DAYS days of workouts..."

if ! command -v hevycli >/dev/null 2>&1; then
    echo "❌ hevycli not found. Run install_hevycli.sh first."
    exit 1
fi

# Calculate date
SINCE_DATE=$(date -d "$DAYS days ago" "+%Y-%m-%d" 2>/dev/null || date -v-"$DAYS"d "+%Y-%m-%d" 2>/dev/null)

if [ -z "$SINCE_DATE" ]; then
    echo "❌ Failed to calculate date"
    exit 1
fi

echo "📅 Getting workouts since: $SINCE_DATE"

# Fetch workouts
hevycli workout list --since "$SINCE_DATE" --output "$OUTPUT_FORMAT"