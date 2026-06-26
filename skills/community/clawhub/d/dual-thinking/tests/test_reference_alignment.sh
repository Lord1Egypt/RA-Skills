#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL="$ROOT/SKILL.md"
MODES="$ROOT/references/modes.md"
EXAMPLES="$ROOT/references/examples.md"

require_present() {
  local needle="$1" file="$2"
  if ! grep -Fq "$needle" "$file"; then
    echo "[FAIL] missing '$needle' in $file" >&2
    exit 1
  fi
}

require_absent() {
  local needle="$1" file="$2"
  if grep -Fq "$needle" "$file"; then
    echo "[FAIL] unexpected stale '$needle' in $file" >&2
    exit 1
  fi
}

require_present 'set `ORCHESTRATOR_MODE: multi`' "$SKILL"
require_present 'set `ORCHESTRATOR_MODE: multi`' "$MODES"
require_present '`ORCHESTRATOR_MODE: multi`' "$EXAMPLES"
require_present 'MODE:` stays the semantic task mode' "$EXAMPLES"
require_present '#### Round-Limit & Stop Precedence' "$SKILL"
require_present '### Round-Limit & Stop Precedence' "$ROOT/references/runtime-contract.md"
require_present 'If the user explicitly authorized a higher round count' "$SKILL"
require_present 'If the user explicitly authorized a higher round count' "$ROOT/references/runtime-contract.md"
require_present 'do not emit a user-facing progress reply between cycles' "$SKILL"
require_present 'do not emit a user-facing progress reply between cycles' "$ROOT/references/runtime-contract.md"
require_present 'continue immediately into that `NEXT_ACTION`' "$SKILL"
require_present 'continue immediately into that `NEXT_ACTION`' "$ROOT/references/runtime-contract.md"
require_present 'Current-date Internet Trend Grounding Lock' "$SKILL"
require_present 'Current-date Internet Trend Grounding Stability Lock' "$SKILL"
require_present 'Current-date Internet Trend Grounding Anti-Patterns' "$SKILL"
require_present 'Baseline Visibility Fail-Closed Lock' "$SKILL"
require_present 'Baseline Visibility Stability Lock' "$SKILL"
require_present 'BLOCKED_STATE: current-date-trend-not-grounded' "$SKILL"
require_present 'BLOCKED_STATE: current-date-trend-not-grounded' "$ROOT/references/runtime-contract.md"
require_present 'BLOCKED_STATE: current-date-trend-not-grounded' "$ROOT/references/failure-handling.md"
require_present 'current-date-trend-grounding' "$ROOT/references/reference-scenarios.md"
require_present 'live public trend, architecture, implementation, benchmark, and maintainer evidence' "$ROOT/references/self-evolution-lens.md"
require_present 'Current-date Internet Trend Grounding Lock' "$ROOT/references/reference-release-checklist.md"
require_present 'GROUNDING_EVIDENCE:' "$SKILL"
require_present 'GROUNDING_EVIDENCE:' "$ROOT/references/runtime-contract.md"
require_present 'GROUNDING_EVIDENCE:' "$ROOT/references/reference-scenarios.md"
require_present 'GROUNDING_EVIDENCE:' "$ROOT/references/reference-release-checklist.md"
require_present 'grounding-evidence-not-labeled' "$SKILL"
require_present 'grounding-evidence-not-labeled' "$ROOT/references/runtime-contract.md"
require_present 'grounding-evidence-not-labeled' "$ROOT/references/reference-release-checklist.md"
require_present 'grounding-evidence-not-labeled' "$ROOT/references/verification-evidence.md"
require_present 'grounding-evidence-not-labeled' "$ROOT/references/reference-test-log.md"
require_present 'current-date trend-grounding hard-lock family' "$ROOT/references/verification-evidence.md"
require_present 'current-date trend-grounding' "$ROOT/references/reference-test-log.md"
require_present 'multi-cycle-no-intercycle-reply' "$ROOT/references/reference-scenarios.md"
require_present 'baseline-visibility-fail-closed' "$ROOT/references/reference-scenarios.md"
require_present 'no-idle-after-completed-step' "$ROOT/references/reference-scenarios.md"
require_present 'fresh/recovery/replacement consultant sessions have no excerpt rights until visible baseline repaste is proven in that same session' "$ROOT/references/runtime-contract.md"
require_present 'STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, accepted-state summaries, patch summaries, and intent-to-repaste notes are continuity aids only; they do not satisfy baseline visibility or create excerpt rights by themselves' "$ROOT/references/runtime-contract.md"
require_present 'fresh/recovery/replacement consultant session is using excerpts without proven visible baseline repaste in that same session' "$ROOT/references/failure-handling.md"
require_present 'a fresh/recovery/replacement consultant session is about to receive only `STATE_SNAPSHOT`, `SYNC_POINT`, `RESUME_SNIPPET`, an accepted-state summary, a patch summary, or a narrow delta without the real baseline artifact body in that same outbound payload' "$ROOT/references/failure-handling.md"
require_absent 'MODE: alternating-multi-orchestrator' "$EXAMPLES"
require_absent '`alternating-multi-orchestrator` when the user explicitly requested alternation before round 1.' "$MODES"

echo '[OK] reference alignment passed'
