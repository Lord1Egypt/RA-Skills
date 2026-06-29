#!/bin/bash
# bootstrap.sh — Run one evolution cycle + output brief data
#
# Dual purpose:
#   1. First-time bootstrap: --window-days 7 (look back at history)
#   2. Manual evolution: uses --since from state (incremental, same as auto)
#
# Usage:
#   bash scripts/bootstrap.sh                          # manual (incremental from state)
#   bash scripts/bootstrap.sh --window-days 7          # first-time bootstrap
#   bash scripts/bootstrap.sh --max-si 5               # smaller batch
#   bash scripts/bootstrap.sh --sessions-dir <path>    # custom sessions
#   bash scripts/bootstrap.sh --filter-skill <name>    # only process one skill
#   bash scripts/bootstrap.sh --hint "<text>"          # inject hint into trace prelude
#
# Output (stdout): brief-data for agent to format as natural-language report
# Stderr: pipeline logs
# Exit 0: success (even if no traces found)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVOLVER_DIR="${SCRIPT_DIR}/.."
STATE_FILE="${EVOLVER_DIR}/evolver-state.json"

# Defaults
SESSIONS_DIR=""
MAX_SI=10
EXTRA_ARGS=()

# Parse args — pass through unknown args to run-daily.sh
while [[ $# -gt 0 ]]; do
  case "$1" in
    --sessions-dir) SESSIONS_DIR="$2"; shift 2 ;;
    --max-si)       MAX_SI="$2"; shift 2 ;;
    --window-days)  EXTRA_ARGS+=("--window-days" "$2"); shift 2 ;;
    --since)        EXTRA_ARGS+=("--since" "$2"); shift 2 ;;
    --filter-skill) EXTRA_ARGS+=("--filter-skill" "$2"); shift 2 ;;
    --hint)         EXTRA_ARGS+=("--hint" "$2"); shift 2 ;;
    *) shift ;;
  esac
done

# Build run-daily args
RUN_ARGS="--max-si $MAX_SI --state $STATE_FILE --skip-inline"
[[ -n "$SESSIONS_DIR" ]] && RUN_ARGS="$RUN_ARGS --sessions-dir $SESSIONS_DIR"

# Append extra args (--window-days or --since if provided)
for arg in "${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}"; do
  RUN_ARGS="$RUN_ARGS $arg"
done

# Step 1: Run evolution (stderr only — suppress stdout from notify.js)
echo "[bootstrap] Running evolution (max ${MAX_SI} traces)..." >&2
bash "${SCRIPT_DIR}/run-daily.sh" $RUN_ARGS > /dev/null 2>&1

# Step 2: Output brief data (stdout — for agent to format)
node "${SCRIPT_DIR}/brief-data.js" 2>/dev/null

# Step 3: Update last_brief_ts
node -e "
  const fs = require('fs');
  const p = '${STATE_FILE}';
  const s = JSON.parse(fs.readFileSync(p, 'utf8'));
  s.last_brief_ts = new Date().toISOString();
  fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n');
" 2>/dev/null

echo "[bootstrap] Done." >&2
