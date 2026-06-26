#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/run-playwright.sh [test-filter]
# Example:
#   ./scripts/run-playwright.sh "@smoke"

FILTER="${1:-}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="test-results/$TS"
mkdir -p "$OUT_DIR"

CMD=(npx playwright test --reporter=line,html --output="$OUT_DIR")
if [[ -n "$FILTER" ]]; then
  CMD+=(--grep "$FILTER")
fi

echo "[run] ${CMD[*]}"
"${CMD[@]}" | tee "$OUT_DIR/run.log"

echo "[done] artifacts: $OUT_DIR"
