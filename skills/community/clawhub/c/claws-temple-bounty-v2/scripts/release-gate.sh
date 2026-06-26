#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"

if [[ -f "$REPO_ROOT/scripts/validate_skill_repo.py" && -d "$REPO_ROOT/skills/claws-temple-bounty" ]]; then
  VALIDATOR_PATH="$REPO_ROOT/scripts/validate_skill_repo.py"
  SMOKE_SCRIPT="$SKILL_ROOT/scripts/smoke-check.sh"
  VALIDATOR_MODE="repo"
else
  VALIDATOR_PATH="$SKILL_ROOT/scripts/validate_clawhub_bundle.py"
  SMOKE_SCRIPT="$SKILL_ROOT/scripts/smoke-check.sh"
  VALIDATOR_MODE="bundle"
fi

echo "[release-gate] running strict repository validation"
if [[ "$VALIDATOR_MODE" == "repo" ]]; then
  python3 "$VALIDATOR_PATH"
else
  python3 "$VALIDATOR_PATH" "$SKILL_ROOT"
fi

echo "[release-gate] running strict dependency and remote checks"
STRICT_DEPS=1 CHECK_REMOTE_SKILL=1 REMOTE_PROBE_MODE=strict \
  bash "$SMOKE_SCRIPT"

echo "[release-gate] OK"
