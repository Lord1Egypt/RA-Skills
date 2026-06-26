#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL="$ROOT/SKILL.md"
RUNTIME="$ROOT/references/runtime-contract.md"
PACKAGING="$ROOT/PACKAGING_CHECKLIST.md"

require_present() {
  local needle="$1" file="$2"
  if ! grep -Fq "$needle" "$file"; then
    echo "[FAIL] missing '$needle' in $file" >&2
    exit 1
  fi
}

require_present 'retain the diff, and revert to the last passed artifact' "$SKILL"
require_present 'retain the failed diff, and revert to the last passed artifact' "$RUNTIME"
require_present 'tests/test_rollback_on_validation_failure.sh' "$PACKAGING"
require_present 'test -s skills/dual-thinking/PACKAGING_CHECKLIST.md' "$PACKAGING"

echo '[OK] rollback-on-validation-failure contract passed'
