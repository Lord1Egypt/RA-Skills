#!/usr/bin/env bash
set -euo pipefail

# check-counts.sh — Verify that hardcoded counts in docs match reality.
# Run after adding detectors, tests, or fixtures to catch stale documentation.
# Exit 0 = all consistent. Exit 1 = drift found.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."

FAIL=0

check() {
  local label="$1"
  local expected="$2"
  local actual="$3"
  local file="$4"
  if [ "$expected" != "$actual" ]; then
    echo "FAIL: $label — $file says $expected, actual is $actual"
    FAIL=$((FAIL + 1))
  else
    echo "  OK: $label = $actual ($file)"
  fi
}

echo "clawdoc count consistency check"
echo ""

# Ground truth: count from code
# Count detector functions (definitions like "detect_foo() {"), not calls
ACTUAL_DETECTORS=$(grep -c "^detect_.*() {" "$ROOT/scripts/diagnose.sh")
ACTUAL_TESTS=$(bash "$ROOT/tests/test-detection.sh" 2>&1 | grep "Results:" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+')
ACTUAL_FIXTURES=$(find "$ROOT/tests/fixtures" -name "*.jsonl" -maxdepth 1 | wc -l | tr -d ' ')
ACTUAL_PATTERNS=$(jq 'length' "$ROOT/templates/patterns.json")
ACTUAL_VERSION=$(tr -d '[:space:]' < "$ROOT/VERSION")

echo "Ground truth: $ACTUAL_DETECTORS detectors, $ACTUAL_TESTS tests, $ACTUAL_FIXTURES fixtures, $ACTUAL_PATTERNS patterns, v$ACTUAL_VERSION"
echo ""

# --- Detector count ---
echo "=== Detector counts ==="
DIAGNOSE_HEADER=$(grep -oE 'Detects [0-9]+ anti-patterns' "$ROOT/scripts/diagnose.sh" | grep -oE '[0-9]+')
check "diagnose.sh header" "$ACTUAL_DETECTORS" "$DIAGNOSE_HEADER" "scripts/diagnose.sh"

DIAGNOSE_USAGE=$(grep -oE 'all [0-9]+ pattern detectors' "$ROOT/scripts/diagnose.sh" | grep -oE '[0-9]+')
check "diagnose.sh usage" "$ACTUAL_DETECTORS" "$DIAGNOSE_USAGE" "scripts/diagnose.sh"

SKILL_DESC=$(grep -oE '[0-9]+ pattern detectors' "$ROOT/SKILL.md" | head -1 | grep -oE '[0-9]+')
check "SKILL.md description" "$ACTUAL_DETECTORS" "$SKILL_DESC" "SKILL.md"

SKILL_TABLE=$(grep -c '^| [0-9]' "$ROOT/SKILL.md")
check "SKILL.md pattern table rows" "$ACTUAL_PATTERNS" "$SKILL_TABLE" "SKILL.md"

README_TABLE=$(grep -c '^| [0-9]' "$ROOT/README.md")
check "README.md pattern table rows" "$ACTUAL_PATTERNS" "$README_TABLE" "README.md"

README_HOW=$(grep -oE '[0-9]+ pattern detectors' "$ROOT/README.md" | head -1 | grep -oE '[0-9]+')
check "README.md 'How it works'" "$ACTUAL_DETECTORS" "$README_HOW" "README.md"

# --- Test count ---
echo ""
echo "=== Test counts ==="
MAKEFILE_HELP=$(grep -oE '[0-9]+ tests' "$ROOT/Makefile" | grep -oE '[0-9]+' | head -1)
check "Makefile help" "$ACTUAL_TESTS" "$MAKEFILE_HELP" "Makefile"

README_TESTS=$(grep -oE 'runs [0-9]+ tests' "$ROOT/README.md" | grep -oE '[0-9]+')
check "README.md testing section" "$ACTUAL_TESTS" "$README_TESTS" "README.md"

CONTRIB_TESTS=$(grep -oE 'all [0-9]+ tests' "$ROOT/CONTRIBUTING.md" | grep -oE '[0-9]+')
check "CONTRIBUTING.md" "$ACTUAL_TESTS" "$CONTRIB_TESTS" "CONTRIBUTING.md"

# --- Fixture count ---
echo ""
echo "=== Fixture counts ==="
CI_THRESHOLD=$(grep -oE 'ge [0-9]+' "$ROOT/.github/workflows/ci.yml" | grep -oE '[0-9]+' | tail -1)
if [ "$ACTUAL_FIXTURES" -lt "$CI_THRESHOLD" ]; then
  echo "FAIL: CI fixture threshold ($CI_THRESHOLD) exceeds actual fixtures ($ACTUAL_FIXTURES)"
  FAIL=$((FAIL + 1))
else
  echo "  OK: CI fixture threshold = $CI_THRESHOLD, actual = $ACTUAL_FIXTURES (.github/workflows/ci.yml)"
fi

# --- Version ---
echo ""
echo "=== Version consistency ==="
for script in "$ROOT"/scripts/examine.sh "$ROOT"/scripts/diagnose.sh "$ROOT"/scripts/prescribe.sh "$ROOT"/scripts/cost-waterfall.sh "$ROOT"/scripts/headline.sh "$ROOT"/scripts/history.sh "$ROOT"/dev/generate-demo.sh; do
  SCRIPT_VER=$(bash "$script" --version 2>/dev/null | head -1)
  BASENAME=$(basename "$script")
  check "$BASENAME --version" "$ACTUAL_VERSION" "$SCRIPT_VER" "$BASENAME"
done

SKILL_VER=$(grep '^version:' "$ROOT/SKILL.md" | awk '{print $2}')
check "SKILL.md version" "$ACTUAL_VERSION" "$SKILL_VER" "SKILL.md"

# --- patterns.json vs diagnose.sh ---
echo ""
echo "=== Pattern registry ==="
check "patterns.json entries vs detectors" "$ACTUAL_DETECTORS" "$ACTUAL_PATTERNS" "templates/patterns.json"

echo ""
if [ "$FAIL" -gt 0 ]; then
  echo "FAILED: $FAIL count(s) out of sync. Update the stale files."
  exit 1
else
  echo "All counts consistent."
  exit 0
fi
