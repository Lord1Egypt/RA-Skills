#!/bin/bash
# full_run.sh — Orchestrator: fetch trends + analyze in one command
# Usage: bash full_run.sh
# Env overrides: same as fetch_trends.sh (SUBMOLTS, TIMEFRAMES, PAGES, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SNAPSHOT_DIR="${SNAPSHOT_DIR:-$SKILL_ROOT/data/snapshots}"

log()  { echo "[full_run] $(date -u +%H:%M:%S) $*"; }

echo ""
echo "================================================================"
echo "  MOLTBOOK TREND ANALYSIS — FULL RUN"
echo "  $(date -u +'%Y-%m-%d %H:%M UTC')"
echo "================================================================"
echo ""

# ---------- Step 1: Fetch ----------
log "Step 1/2: Fetching live trends..."
echo ""

FETCH_OK=true
SNAPSHOT_DIR="$SNAPSHOT_DIR" bash "$SCRIPT_DIR/fetch_trends.sh" || {
  log "WARNING: Fetch failed or partially failed."
  FETCH_OK=false
}

echo ""

# ---------- Step 2: Analyze ----------
log "Step 2/2: Analyzing snapshots..."
echo ""

# Find snapshot files to analyze — prefer today's files, fall back to most recent
TODAY="$(date -u +%Y-%m-%d)"
TODAY_FILES=()
while IFS= read -r -d '' file; do
  TODAY_FILES+=("$file")
done < <(find "$SNAPSHOT_DIR" -maxdepth 1 -name "${TODAY}*.json" -print0 2>/dev/null || true)

if [[ ${#TODAY_FILES[@]} -gt 0 ]]; then
  log "Found ${#TODAY_FILES[@]} snapshot(s) from today."
  python3 "$SCRIPT_DIR/analyze_trends.py" "${TODAY_FILES[@]}"
else
  # Fall back to most recent files (any date)
  log "No snapshots from today. Looking for most recent..."
  RECENT_FILES=()
  while IFS= read -r file; do
    RECENT_FILES+=("$file")
  done < <(ls -t "$SNAPSHOT_DIR"/*.json 2>/dev/null || true)

  if [[ ${#RECENT_FILES[@]} -gt 0 ]]; then
    # Take up to 6 most recent
    ANALYZE_FILES=("${RECENT_FILES[@]:0:6}")
    log "Using ${#ANALYZE_FILES[@]} most recent snapshot(s)."
    python3 "$SCRIPT_DIR/analyze_trends.py" "${ANALYZE_FILES[@]}"
  else
    log "ERROR: No snapshot files found in $SNAPSHOT_DIR"
    log "Cannot generate analysis without data."
    exit 1
  fi
fi

echo ""
echo "================================================================"
echo "  FULL RUN COMPLETE"
if [[ "$FETCH_OK" == "true" ]]; then
  echo "  Status: SUCCESS"
else
  echo "  Status: PARTIAL (fetch had errors, analysis used available data)"
fi
echo "  $(date -u +'%Y-%m-%d %H:%M UTC')"
echo "================================================================"
echo ""
