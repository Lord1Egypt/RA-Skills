#!/bin/bash
set -euo pipefail

SKILL_PATH="${1:?Usage: run-eval.sh <skill_path> [state_root]}"
STATE_ROOT="${2:-/tmp/autoloop}"

echo "[$(date -Iseconds)] Starting autoloop iteration for ${SKILL_PATH}" >> "${STATE_ROOT}/autoloop.log"

python3 "$(dirname "$0")/autoloop.py" \
  --target "${SKILL_PATH}" \
  --state-root "${STATE_ROOT}" \
  --mode single-run \
  2>&1 | tee -a "${STATE_ROOT}/autoloop.log"

echo "[$(date -Iseconds)] Iteration complete" >> "${STATE_ROOT}/autoloop.log"
