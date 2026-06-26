#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL="$ROOT/SKILL.md"
RUNTIME="$ROOT/references/runtime-contract.md"
EXAMPLES="$ROOT/references/examples.md"
PACKAGING="$ROOT/PACKAGING_CHECKLIST.md"

require_present() {
  local needle="$1" file="$2"
  if ! grep -Fq "$needle" "$file"; then
    echo "[FAIL] missing '$needle' in $file" >&2
    exit 1
  fi
}

require_present '#### Multi-orchestrator alternation contract' "$SKILL"
require_present '`STATE_SNAPSHOT`' "$SKILL"
require_present '`SYNC_POINT`' "$SKILL"
require_present 'If `ORCHESTRATOR_MODE: multi`:' "$RUNTIME"
require_present '`STATE_SNAPSHOT`' "$RUNTIME"
require_present '`SYNC_POINT`' "$EXAMPLES"
require_present 'tests/test_multi_alternation.sh' "$PACKAGING"

if [[ ! -f "$ROOT/.clawhubignore" ]]; then
  echo '[FAIL] missing .clawhubignore' >&2
  exit 1
fi

echo '[OK] multi alternation contract passed'
