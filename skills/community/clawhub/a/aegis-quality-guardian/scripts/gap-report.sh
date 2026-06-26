#!/usr/bin/env bash
# gap-report.sh — Generate a report of known gaps from Design Briefs
#
# Usage: bash gap-report.sh /path/to/project
#
# Scans docs/designs/*.md for gap markers and produces a summary.

set -euo pipefail

PROJECT="${1:-.}"
DESIGNS="$PROJECT/docs/designs"

echo "🛡️  Aegis Gap Report: $PROJECT"
echo "══════════════════════════════════════"
echo ""

if [[ ! -d "$DESIGNS" ]]; then
  echo "No designs directory found at: $DESIGNS"
  exit 0
fi

TOTAL=0
BLOCKING=0
OPEN=0

while IFS= read -r file; do
  filename=$(basename "$file")
  gaps=$(grep -n -i "\[.*gap\|known gap\|open question" "$file" 2>/dev/null || true)

  if [[ -n "$gaps" ]]; then
    echo "📄 $filename"
    echo "$gaps" | while IFS= read -r line; do
      echo "   $line"
      TOTAL=$((TOTAL + 1))
    done
    echo ""
  fi
done < <(find "$DESIGNS" -name "*.md" -type f | sort)

# Count blocking vs non-blocking
BLOCKING=$(grep -r -c "\[blocking\]" "$DESIGNS" 2>/dev/null || echo "0")
NON_BLOCKING=$(grep -r -c "\[non-blocking\]" "$DESIGNS" 2>/dev/null || echo "0")
UNCHECKED=$(grep -r -c "\- \[ \]" "$DESIGNS" 2>/dev/null || echo "0")
CHECKED=$(grep -r -c "\- \[x\]" "$DESIGNS" 2>/dev/null || echo "0")

echo "══════════════════════════════════════"
echo "Summary:"
echo "  🔴 Blocking gaps:     $BLOCKING"
echo "  🟡 Non-blocking gaps: $NON_BLOCKING"
echo "  ☐  Open items:        $UNCHECKED"
echo "  ☑  Resolved items:    $CHECKED"
