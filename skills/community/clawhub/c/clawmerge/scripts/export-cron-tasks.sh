#!/bin/bash
#
# Export OpenClaw Cron Tasks to JSON
# Usage: ./export-cron-tasks.sh [output_file]
#

set -e

OUTPUT_FILE="${1:-$HOME/.openclaw/workspace/cron-tasks-export.json}"

echo "Exporting OpenClaw cron tasks..."

# Use clawhub cron list to get all jobs
# Note: This requires the cron tool to be available
if command -v clawhub &> /dev/null; then
    # Try to export via clawhub
    clawhub cron list --include-disabled > "$OUTPUT_FILE" 2>/dev/null || echo '{"jobs":[]}' > "$OUTPUT_FILE"
else
    # Fallback: create empty export
    echo '{"jobs":[],"note":"No cron tool available"}' > "$OUTPUT_FILE"
fi

echo "Cron tasks exported to: $OUTPUT_FILE"
echo ""
cat "$OUTPUT_FILE"
