#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"

if [[ -f "$REPO_ROOT/scripts/validate_skill_repo.py" && -d "$REPO_ROOT/skills/claws-temple-bounty" ]]; then
  VALIDATOR_PATH="$REPO_ROOT/scripts/validate_skill_repo.py"
  SMOKE_SCRIPT="$SKILL_ROOT/scripts/smoke-check.sh"
  PROBE_SCRIPT="$SKILL_ROOT/scripts/task4-live-skill-probe.sh"
  VALIDATOR_MODE="repo"
else
  VALIDATOR_PATH="$SKILL_ROOT/scripts/validate_clawhub_bundle.py"
  SMOKE_SCRIPT="$SKILL_ROOT/scripts/smoke-check.sh"
  PROBE_SCRIPT="$SKILL_ROOT/scripts/task4-live-skill-probe.sh"
  VALIDATOR_MODE="bundle"
fi

echo "[test-rollout-gate] running repository validation"
if [[ "$VALIDATOR_MODE" == "repo" ]]; then
  python3 "$VALIDATOR_PATH"
else
  python3 "$VALIDATOR_PATH" "$SKILL_ROOT"
fi

echo "[test-rollout-gate] running strict local dependency checks"
STRICT_DEPS=1 bash "$SMOKE_SCRIPT"

echo "[test-rollout-gate] probing Task 4 live skill in strict mode"
PROBE_MODE=strict bash "$PROBE_SCRIPT"

echo "[test-rollout-gate] OK"
