#!/bin/bash
# Legacy daily commit report generator.

set -euo pipefail

export PATH="/usr/bin:/bin:/usr/local/bin:/home/linuxbrew/.linuxbrew/bin:${PATH:-}"
export HOME="${HOME:-/root}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$DAILY_DIR")"
export OPENCLAW_WORKSPACE="$WORKSPACE"

REPORT_OUTPUT=$(bash "$SCRIPT_DIR/generate-report.sh" 2>/dev/null)
LOGBOOK_ENTRY=$(echo "$REPORT_OUTPUT" | sed -n '/=== LOGBOOK ENTRY/,$p' | tail -n +2)
PENDING_FILE="$WORKSPACE/pending-logbook-report.txt"

if [ -n "$LOGBOOK_ENTRY" ]; then
    cat > "$PENDING_FILE" << EOF
🌅 Good morning! Here's your daily commit summary for the logbook:

$LOGBOOK_ENTRY

📋 Copy and paste this into your MIS logbook at https://online.mis.pens.ac.id/
EOF
    echo "Report generated and saved to $PENDING_FILE"
else
    cat > "$PENDING_FILE" << EOF
🌅 Good morning! No commits detected for yesterday.

You can still log your planning or coordination activities in the MIS logbook at https://online.mis.pens.ac.id/
EOF
    echo "No-commit report saved to $PENDING_FILE"
fi
