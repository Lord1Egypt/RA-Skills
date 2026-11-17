#!/bin/bash
# cleanup.sh — purge debate archives older than a retention threshold
# Usage: bash cleanup.sh [days]
#   days: retention period in days (default: 90)
#   Set to 0 to preview what would be deleted without removing anything.
#
# Example:
#   bash cleanup.sh 30        # delete debates older than 30 days
#   bash cleanup.sh 0         # dry-run: list what would be deleted

set -euo pipefail

RETENTION_DAYS=${1:-90}
ROOT="$HOME/.hermes/debates"
DRY_RUN=false

if [ "$RETENTION_DAYS" -eq 0 ]; then
  DRY_RUN=true
  echo "[DRY RUN] The following debates would be deleted (retention = preview mode):"
  echo ""
fi

if [ ! -d "$ROOT" ]; then
  echo "No debates directory found at $ROOT. Nothing to do."
  exit 0
fi

# Find debate directories matching conclave-* older than retention period
FOUND=0
while IFS= read -r dir; do
  FOUND=1
  AGE_DAYS=$(( ( $(date +%s) - $(stat -f "%m" "$dir" 2>/dev/null || stat -c "%Y" "$dir" 2>/dev/null) ) / 86400 ))

  if [ "$DRY_RUN" = true ]; then
    echo "  $dir  (age: ${AGE_DAYS}d)"
  else
    echo "Deleting $dir (age: ${AGE_DAYS}d > ${RETENTION_DAYS}d)"
    rm -rf "$dir"
  fi
done < <(find "$ROOT" -maxdepth 1 -type d -name 'conclave-*' -mtime +"$RETENTION_DAYS" 2>/dev/null | sort)

if [ "$FOUND" -eq 0 ]; then
  if [ "$DRY_RUN" = true ]; then
    echo "  (none)"
  else
    echo "No debates older than ${RETENTION_DAYS} days found."
  fi
fi

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "Re-run with a positive number to actually delete."
fi
