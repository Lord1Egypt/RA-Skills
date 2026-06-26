#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL="$ROOT/SKILL.md"
LENS="$ROOT/references/self-evolution-lens.md"
SCENARIOS="$ROOT/references/reference-scenarios.md"
MODES="$ROOT/references/modes.md"
EXAMPLES="$ROOT/references/examples.md"
CHANGE_POLICY="$ROOT/references/change-policy.md"
RUNTIME="$ROOT/references/runtime-contract.md"

require_present() {
  local needle="$1" file="$2"
  if ! grep -Fq "$needle" "$file"; then
    echo "[FAIL] missing '$needle' in $file" >&2
    exit 1
  fi
}

require_present 'self-evolution lens' "$SKILL"
require_present 'Governance and release-policy detail is non-runtime and lives in `GOVERNANCE.md`.' "$SKILL"
if ! grep -Eq '`v(7\.9\.14|8\.3\.1|8\.5\.0|8\.5\.1|8\.5\.2|8\.5\.5|8\.5\.6|8\.5\.7|8\.5\.9)` is the frozen prior reference-release line\.' "$ROOT/GOVERNANCE.md"; then
  echo "[FAIL] missing accepted frozen-prior reference-release line in $ROOT/GOVERNANCE.md" >&2
  exit 1
fi
require_present 'Reference-line validation states:' "$ROOT/GOVERNANCE.md"
require_present 'self-evolution lens' "$LENS"
require_present 'self-review-dual-thinking' "$SCENARIOS"
require_present 'freeze-compatibility' "$SCENARIOS"
require_present 'current-date-trend-grounding' "$SCENARIOS"
require_present 'live public trend, architecture, implementation, benchmark, and maintainer evidence' "$LENS"
require_present 'The self-evolution lens is stance logic inside the routed mode, not a new public mode.' "$MODES"
require_present 'challenge-heavy consultant prompt under self-evolution' "$EXAMPLES"
require_present 'self-review stance changes' "$CHANGE_POLICY"
require_present 'The self-evolution lens does not add a fourth public stage or a new public mode.' "$RUNTIME"
require_present 'current-date trend grounding constraints' "$RUNTIME"

echo '[OK] self-evolution alignment passed'
