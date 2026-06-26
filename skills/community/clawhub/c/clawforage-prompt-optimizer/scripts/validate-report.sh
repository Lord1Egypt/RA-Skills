#!/bin/bash
# validate-report.sh — Validate that a weekly report has all required sections
# Usage: validate-report.sh <report.md>
# Exit 0 if valid, 1 if invalid
set -euo pipefail

REPORT="${1:?Usage: validate-report.sh <report.md>}"

if [ ! -s "$REPORT" ]; then
  echo "ERROR: Report file is empty or missing: $REPORT"
  exit 1
fi

ERRORS=0

check_section() {
  local section="$1"
  if ! grep -q "$section" "$REPORT"; then
    echo "ERROR: Missing required section: $section"
    ERRORS=$((ERRORS + 1))
  fi
}

check_section "# ClawForage Weekly Optimization"
check_section "Repeated Patterns"
check_section "SOUL.md Suggestions"
check_section "Recommended Skills"
check_section "Failure Analysis"

if [ "$ERRORS" -gt 0 ]; then
  echo "Validation failed: $ERRORS missing section(s)"
  exit 1
fi

echo "Report validation passed"
exit 0
