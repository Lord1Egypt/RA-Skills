#!/bin/bash
# Extract the MIS-ready activity text from the natural-language section
# of the generated daily report.

set -euo pipefail

REPORT_FILE="${1:-}"

if [ -z "$REPORT_FILE" ] || [ ! -f "$REPORT_FILE" ]; then
    echo "Usage: $0 /path/to/commit-report-YYYY-MM-DD.md" >&2
    exit 1
fi

awk '
    /^### Versi 2/ { in_v2 = 1; next }
    in_v2 && /^\*\*Aktivitas:\*\*/ { capture = 1; next }
    capture && /^\*\*Hasil:\*\*/ { exit }
    capture { print }
' "$REPORT_FILE" \
| sed 's/^\*\*//; s/\*\*$//' \
| sed 's/^-[[:space:]]*//' \
| sed '/^[[:space:]]*$/d' \
| paste -sd ' ' - \
| sed -E 's/[[:space:]]+/ /g; s/[[:space:]]+\././g; s/[[:space:]]+,/,/g; s/^[[:space:]]+//; s/[[:space:]]+$//'

