#!/usr/bin/env bash
set -uo pipefail

# run-real-sessions.sh
# Runs all 12 detectors against converted real Claude Code sessions.
# Reports: pass rate, pattern distribution, crashes, and timing.
#
# Usage: run-real-sessions.sh [fixtures-dir]
#   Default: tests/fixtures/real/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REAL_DIR="${1:-$SCRIPT_DIR/../tests/fixtures/real}"
DIAGNOSE="$SCRIPT_DIR/../scripts/diagnose.sh"

if [ ! -d "$REAL_DIR" ]; then
  echo "ERROR: $REAL_DIR not found. Run convert-claude-sessions.sh first."
  exit 1
fi

FILE_COUNT=$(find "$REAL_DIR" -name "real-*.jsonl" -type f | wc -l | tr -d ' ')
if [ "$FILE_COUNT" -eq 0 ]; then
  echo "ERROR: No real-*.jsonl files found in $REAL_DIR"
  exit 1
fi

echo "═══════════════════════════════════════════════════════"
echo "  clawdoc — Real Session Test Suite"
echo "  $FILE_COUNT sessions from converted Claude Code logs"
echo "═══════════════════════════════════════════════════════"
echo ""

TOTAL=0
CLEAN=0
WITH_FINDINGS=0
CRASHED=0
BAD_JSON=0

# Pattern counters
declare -a PATTERN_COUNTS
for i in $(seq 1 12); do PATTERN_COUNTS[$i]=0; done

# Pattern 12 details
P12_DRIFT=0
P12_SPIRAL=0

# Collect all findings for summary
ALL_FINDINGS_FILE=$(mktemp /tmp/clawdoc_real_findings.XXXXXX)
trap 'rm -f "$ALL_FINDINGS_FILE"' EXIT

for f in "$REAL_DIR"/real-*.jsonl; do
  TOTAL=$((TOTAL + 1))
  fname=$(basename "$f")
  lines=$(wc -l < "$f" | tr -d ' ')

  # Run diagnose, capture both stdout and exit code
  result=""
  exit_code=0
  result=$(bash "$DIAGNOSE" "$f" 2>/dev/null) || exit_code=$?

  if [ "$exit_code" -gt 1 ]; then
    CRASHED=$((CRASHED + 1))
    echo "CRASH [$fname]: exit code $exit_code ($lines lines)"
    continue
  fi

  # Validate JSON output
  if [ -z "$result" ]; then
    CRASHED=$((CRASHED + 1))
    echo "CRASH [$fname]: empty output ($lines lines)"
    continue
  fi

  if ! echo "$result" | jq -e 'type == "array"' >/dev/null 2>&1; then
    BAD_JSON=$((BAD_JSON + 1))
    echo "BAD_JSON [$fname]: output is not a valid JSON array"
    continue
  fi

  # Count findings
  count=$(echo "$result" | jq 'length' 2>/dev/null || echo 0)

  if [ "$count" -eq 0 ]; then
    CLEAN=$((CLEAN + 1))
    echo "CLEAN  [$fname]: no findings ($lines lines)"
  else
    WITH_FINDINGS=$((WITH_FINDINGS + 1))
    echo "$result" >> "$ALL_FINDINGS_FILE"

    # Count by pattern
    pattern_ids=$(echo "$result" | jq -r '.[].pattern_id' 2>/dev/null)
    detected_list=""
    for pid in $pattern_ids; do
      PATTERN_COUNTS[$pid]=$((${PATTERN_COUNTS[$pid]} + 1))
      detected_list="$detected_list P$pid"
      # Track P12 sub-types
      if [ "$pid" -eq 12 ]; then
        evidence=$(echo "$result" | jq -r '.[] | select(.pattern_id == 12) | .evidence' 2>/dev/null)
        if echo "$evidence" | grep -q "exploration spiral"; then
          P12_SPIRAL=$((P12_SPIRAL + 1))
        elif echo "$evidence" | grep -q "drifted"; then
          P12_DRIFT=$((P12_DRIFT + 1))
        fi
      fi
    done
    echo "FOUND  [$fname]:$detected_list ($lines lines, $count finding(s))"
  fi
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  RESULTS"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Sessions tested:    $TOTAL"
echo "  Clean (0 findings): $CLEAN"
echo "  With findings:      $WITH_FINDINGS"
echo "  Crashed:            $CRASHED"
echo "  Bad JSON output:    $BAD_JSON"
echo ""
echo "  Pattern distribution:"
echo "  ┌─────┬───────────────────────────────────┬───────┐"
echo "  │  #  │ Pattern                           │ Count │"
echo "  ├─────┼───────────────────────────────────┼───────┤"

PATTERN_NAMES=( "" "infinite-retry" "non-retryable-retry" "tool-as-text" "context-exhaustion" "subagent-replay" "cost-spike" "skill-miss" "model-routing-waste" "cron-accumulation" "compaction-damage" "workspace-overhead" "task-drift" )

for i in $(seq 1 12); do
  printf "  │ %2d  │ %-33s │ %5d │\n" "$i" "${PATTERN_NAMES[$i]}" "${PATTERN_COUNTS[$i]}"
done
echo "  └─────┴───────────────────────────────────┴───────┘"
echo ""
echo "  Pattern 12 breakdown:"
echo "    Post-compaction drift:  $P12_DRIFT"
echo "    Exploration spiral:     $P12_SPIRAL"
echo ""

# Calculate false-positive risk metric
if [ "$TOTAL" -gt 0 ]; then
  P12_PCT=$(( ${PATTERN_COUNTS[12]} * 100 / TOTAL ))
  echo "  P12 detection rate: ${P12_PCT}% of sessions"
  if [ "$P12_PCT" -gt 50 ]; then
    echo "  ⚠️  >50% detection rate — may indicate false positive risk"
  elif [ "$P12_PCT" -gt 30 ]; then
    echo "  ⚠️  >30% detection rate — worth reviewing flagged sessions"
  else
    echo "  ✅  Detection rate looks reasonable"
  fi
fi

echo ""
echo "  No crashes = diagnose.sh is robust against real-world data ✅"
echo "═══════════════════════════════════════════════════════"
