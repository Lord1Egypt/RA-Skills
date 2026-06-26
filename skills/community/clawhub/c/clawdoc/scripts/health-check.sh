#!/bin/bash
# health-check.sh — full quality gate for clawdoc
set -euo pipefail
PASS=0; FAIL=0

HC_TMP=$(mktemp /tmp/clawdoc_hc.XXXXXX)
trap 'rm -f "$HC_TMP"' EXIT

run_check() {
  local label="$1"; shift
  echo -n "  Checking: $label ... "
  if "$@" > "$HC_TMP" 2>&1; then
    echo "✅ PASS"
    ((PASS++)) || true
  else
    echo "❌ FAIL"
    tail -20 "$HC_TMP" | sed 's/^/  | /'
    ((FAIL++)) || true
  fi
}

echo ""
echo "🛡️  clawdoc — Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
run_check "Detection tests (57)"  make test
run_check "Shellcheck lint"       make lint
run_check "Dependencies"          make check-deps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: $PASS passed, $FAIL failed"
echo ""
if [ "$FAIL" -gt 0 ]; then
  echo "❌ Health check FAILED — fix the issues above before proceeding."
  exit 1
else
  echo "✅ All checks passed — baseline is healthy."
fi
