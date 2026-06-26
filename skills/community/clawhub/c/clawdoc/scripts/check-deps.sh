#!/usr/bin/env bash
set -euo pipefail

# check-deps.sh
# Verifies all required dependencies for clawdoc are present and meet minimum versions.
# Exits 0 if all deps are satisfied, 1 if any are missing or outdated.

PASS=0
FAIL=0

check_bin() {
  local name="$1"
  local min_ver="$2"  # informational only
  if command -v "$name" >/dev/null 2>&1; then
    echo "  ✓ $name found ($(command -v "$name"))"
    PASS=$((PASS + 1))
  else
    echo "  ✗ $name not found — required (min version: $min_ver)"
    FAIL=$((FAIL + 1))
  fi
}

check_jq_version() {
  if ! command -v jq >/dev/null 2>&1; then
    return  # already reported as missing
  fi
  local ver
  ver=$(jq --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -1)
  local major minor
  major=$(echo "$ver" | cut -d. -f1)
  minor=$(echo "$ver" | cut -d. -f2)
  if [ "${major:-0}" -gt 1 ] || { [ "${major:-0}" -eq 1 ] && [ "${minor:-0}" -ge 6 ]; }; then
    echo "  ✓ jq version $ver (>= 1.6 required)"
  else
    echo "  ✗ jq version $ver is too old — 1.6+ required"
    FAIL=$((FAIL + 1))
    PASS=$((PASS - 1))  # undo the check_bin pass
  fi
}

check_bash_version() {
  local ver="${BASH_VERSION:-}"
  local major
  major=$(echo "$ver" | cut -d. -f1)
  if [ "${major:-0}" -ge 3 ]; then
    echo "  ✓ bash version $ver (>= 3.2 required)"
    PASS=$((PASS + 1))
  else
    echo "  ✗ bash version $ver is too old — 3.2+ required"
    FAIL=$((FAIL + 1))
  fi
}

echo "clawdoc dependency check"
echo ""
echo "Required:"
check_bin "jq"   "1.6+"
check_jq_version
check_bash_version

check_bin "bc"   "any"

echo ""
echo "Standard POSIX (should be present on any system):"
check_bin "awk"  "any"
check_bin "sed"  "any"
check_bin "grep" "any"
check_bin "sort" "any"
check_bin "uniq" "any"
check_bin "wc"   "any"
check_bin "find" "any"
check_bin "date" "any"

echo ""
echo "Optional (enables make lint):"
if command -v shellcheck >/dev/null 2>&1; then
  echo "  ✓ shellcheck found"
else
  echo "  - shellcheck not found (install with: brew install shellcheck)"
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "All required dependencies satisfied."
  exit 0
else
  echo "$FAIL required dependency/dependencies missing or outdated."
  exit 1
fi
