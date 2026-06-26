#!/usr/bin/env bash
set -euo pipefail

# run-stress-tests.sh
# Runs diagnose.sh against all stress fixtures and validates against manifest expectations.
# Exit 0 = all pass. Exit 1 = any fail.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STRESS_DIR="$SCRIPT_DIR/../tests/fixtures/stress"
DIAGNOSE="$SCRIPT_DIR/../scripts/diagnose.sh"
MANIFEST="$STRESS_DIR/manifest.tsv"

if [ ! -f "$MANIFEST" ]; then
  echo "ERROR: No manifest found. Run generate-stress-fixtures.sh first."
  exit 1
fi

PASS=0
FAIL=0

echo "=== clawdoc stress tests ==="
echo ""

# Read manifest into arrays (avoid pipe subshell)
FIXTURES=()
DESCS=()
EXPECTS=()
NOT_EXPECTS=()

while IFS=$'\t' read -r fixture desc expect_patterns expect_not_patterns; do
  FIXTURES+=("$fixture")
  DESCS+=("$desc")
  EXPECTS+=("$expect_patterns")
  NOT_EXPECTS+=("${expect_not_patterns:-}")
done < <(tail -n +2 "$MANIFEST")

for idx in "${!FIXTURES[@]}"; do
  fixture="${FIXTURES[$idx]}"
  desc="${DESCS[$idx]}"
  expect_patterns="${EXPECTS[$idx]}"
  expect_not_patterns="${NOT_EXPECTS[$idx]}"
  file="$STRESS_DIR/$fixture"

  if [ ! -f "$file" ]; then
    echo "FAIL [$fixture]: file not found"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Run diagnose
  findings=$(bash "$DIAGNOSE" "$file" 2>/dev/null || echo "[]")
  detected_ids=$(echo "$findings" | jq -r '[.[].pattern_id] | sort | unique | @csv' 2>/dev/null || echo "")

  ok=1

  # Check expected patterns
  if [ "$expect_patterns" != "none" ] && [ -n "$expect_patterns" ]; then
    IFS=',' read -ra MUST <<< "$expect_patterns"
    for pid in "${MUST[@]}"; do
      pid="${pid// /}"
      if ! echo "$findings" | jq -e --argjson p "$pid" 'any(.[]; .pattern_id == $p)' >/dev/null 2>&1; then
        echo "FAIL [$fixture]: expected pattern $pid but not detected (got: [$detected_ids])"
        ok=0
      fi
    done
  fi

  # Check must-NOT-detect patterns
  if [ -n "$expect_not_patterns" ]; then
    IFS=',' read -ra MUST_NOT <<< "$expect_not_patterns"
    for pid in "${MUST_NOT[@]}"; do
      pid="${pid// /}"
      if echo "$findings" | jq -e --argjson p "$pid" 'any(.[]; .pattern_id == $p)' >/dev/null 2>&1; then
        echo "FAIL [$fixture]: pattern $pid should NOT fire but did (got: [$detected_ids])"
        ok=0
      fi
    done
  fi

  if [ "$ok" -eq 1 ]; then
    echo "PASS [$fixture]: $desc (detected: [$detected_ids])"
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
  fi
done

echo ""
echo "=== Stress results: $PASS passed, $FAIL failed out of ${#FIXTURES[@]} fixtures ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
