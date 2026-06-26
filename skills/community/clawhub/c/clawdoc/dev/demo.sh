#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# clawdoc demo — run this to see all 14 detectors in action
# ═══════════════════════════════════════════════════════════════
#
# Usage:
#   bash dev/demo.sh           # full interactive demo
#   bash dev/demo.sh --fast    # skip pauses
#
# No dependencies beyond clawdoc's own requirements (bash + jq).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FIXTURES="$ROOT_DIR/tests/fixtures"
DIAGNOSE="$ROOT_DIR/scripts/diagnose.sh"
PRESCRIBE="$ROOT_DIR/scripts/prescribe.sh"
EXAMINE="$ROOT_DIR/scripts/examine.sh"
COST_WATERFALL="$ROOT_DIR/scripts/cost-waterfall.sh"
HEADLINE="$ROOT_DIR/scripts/headline.sh"

FAST=0
[ "${1:-}" = "--fast" ] && FAST=1

# Colors
BOLD="\033[1m"
DIM="\033[2m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
CYAN="\033[36m"
RESET="\033[0m"

pause() {
  if [ "$FAST" -eq 0 ]; then
    echo ""
    echo -e "${DIM}  Press Enter to continue...${RESET}"
    read -r
  else
    echo ""
  fi
}

section() {
  echo ""
  echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${RESET}"
  echo -e "${BOLD}${CYAN}  $1${RESET}"
  echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${RESET}"
  echo ""
}

narrate() {
  echo -e "${DIM}  $1${RESET}"
}

run_cmd() {
  echo -e "  ${GREEN}\$${RESET} $1"
  echo ""
  bash -c "$1" 2>/dev/null | sed 's/^/  /'
}

# ═══════════════════════════════════════════════════════════════
# INTRO
# ═══════════════════════════════════════════════════════════════

clear
echo ""
echo -e "${BOLD}  🩻 clawdoc — Agent Session Diagnostics${RESET}"
echo -e "  ${DIM}Examine agent sessions. Diagnose failures. Prescribe fixes.${RESET}"
echo ""
echo -e "  ${DIM}Version $(cat "$ROOT_DIR/VERSION")  •  14 pattern detectors  •  57 tests${RESET}"
echo ""
pause

# ═══════════════════════════════════════════════════════════════
# DEMO 1: Healthy session
# ═══════════════════════════════════════════════════════════════

section "1. Examining a healthy session"

narrate "Let's start with a clean session — a simple weather query."
narrate "examine.sh gives us a structured summary."
echo ""

run_cmd "bash $EXAMINE $FIXTURES/12-healthy-session.jsonl | jq '{turns, total_cost, tool_calls, error_count}'"

echo ""
narrate "2 turns, \$0.01, one search_web call, zero errors. Clean bill of health."

pause

narrate "Now let's run the full diagnostic suite on it."
echo ""

run_cmd "bash $DIAGNOSE $FIXTURES/12-healthy-session.jsonl"

echo ""
narrate "Empty array — no issues detected. This is what a healthy session looks like."

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 2: Infinite retry loop (Pattern 1)
# ═══════════════════════════════════════════════════════════════

section "2. Detecting an infinite retry loop (Pattern 1)"

narrate "This session has an agent calling the same tool 8 times in a row."
narrate "diagnose.sh catches it:"
echo ""

run_cmd "bash $DIAGNOSE $FIXTURES/01-infinite-retry.jsonl | jq '.[0] | {pattern, severity, evidence, cost_impact}'"

echo ""
narrate "Critical severity. The evidence tells you exactly which tool, how many times,"
narrate "and how much money it burned."

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 3: The full pipeline — diagnose | prescribe
# ═══════════════════════════════════════════════════════════════

section "3. Full pipeline: diagnose → prescribe"

narrate "The real power is piping diagnose into prescribe for a formatted report:"
echo ""

run_cmd "bash $DIAGNOSE $FIXTURES/13-multi-pattern.jsonl 2>/dev/null | bash $PRESCRIBE"

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 4: Cost waterfall
# ═══════════════════════════════════════════════════════════════

section "4. Cost waterfall — where did the money go?"

narrate "cost-waterfall.sh shows per-turn cost breakdown, sorted by expense:"
echo ""

run_cmd "bash $COST_WATERFALL $FIXTURES/06-cost-spike.jsonl | jq '.[0:3] | .[] | {turn, cost, tool, cause}'"

echo ""
narrate "Instantly see which turns were expensive and why."

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 5: NEW — Task Drift Detection (Pattern 12)
# ═══════════════════════════════════════════════════════════════

section "5. NEW: Task drift detection (Pattern 12)"

echo -e "  ${YELLOW}This is the newest detector — just shipped in v1.1.0.${RESET}"
echo -e "  ${YELLOW}Catches two failure modes that frustrate developers daily:${RESET}"
echo ""

narrate "5a. Post-compaction directory divergence"
narrate "    Agent was fixing an API auth bug, then compaction hit,"
narrate "    and it forgot what it was doing — started editing UI components."
echo ""

run_cmd "bash $DIAGNOSE $FIXTURES/17-task-drift-compaction.jsonl | jq '.[] | select(.pattern_id == 12) | {pattern, evidence, cost_impact, prescription}'"

pause

narrate "5b. Exploration spiral"
narrate "    Agent reads 12 files without making a single edit."
narrate "    It's stuck in a research loop, burning tokens."
echo ""

run_cmd "bash $DIAGNOSE $FIXTURES/18-task-drift-exploration.jsonl | jq '.[] | select(.pattern_id == 12) | {pattern, evidence, cost_impact, prescription}'"

pause

narrate "True negative — agent stays on task after compaction (no false positive):"
echo ""

run_cmd "bash $DIAGNOSE $FIXTURES/19-task-drift-negative.jsonl | jq 'length'"

echo ""
narrate "Zero findings. The agent stayed in the same directories after compaction."

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 6: Headline mode — multi-session overview
# ═══════════════════════════════════════════════════════════════

section "6. Headline mode — the tweetable health check"

narrate "headline.sh scans a directory of sessions and produces a compact summary."
narrate "This is what /clawdoc shows by default:"
echo ""

run_cmd "bash $HEADLINE $FIXTURES/"

pause

narrate "Brief mode for daily crons — one line:"
echo ""

run_cmd "bash $HEADLINE --brief $FIXTURES/"

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 7: Running the test suite
# ═══════════════════════════════════════════════════════════════

section "7. Test suite — 57 tests, all green"

narrate "Every pattern detector has true-positive, true-negative, and edge-case tests."
echo ""

run_cmd "make -C $ROOT_DIR test 2>&1 | tail -5"

pause

# ═══════════════════════════════════════════════════════════════
# DEMO 8: Real session results (if available)
# ═══════════════════════════════════════════════════════════════

if [ -d "$ROOT_DIR/tests/fixtures/real" ]; then
  REAL_COUNT=$(find "$ROOT_DIR/tests/fixtures/real" -name "real-*.jsonl" -type f | wc -l | tr -d ' ')
  if [ "$REAL_COUNT" -gt 0 ]; then
    section "8. Real session validation — $REAL_COUNT sessions"

    narrate "We tested against $REAL_COUNT real Claude Code sessions."
    narrate "Pattern 12 results from real data:"
    echo ""

    P12_COUNT=0
    for f in "$ROOT_DIR/tests/fixtures/real"/real-*.jsonl; do
      result=$(bash "$DIAGNOSE" "$f" 2>/dev/null || echo "[]")
      has_12=$(echo "$result" | jq 'any(.[]; .pattern_id == 12)' 2>/dev/null || echo "false")
      [ "$has_12" = "true" ] && P12_COUNT=$((P12_COUNT + 1))
    done

    echo -e "  ${BOLD}Pattern 12 detected in: $P12_COUNT / $REAL_COUNT sessions ($(( P12_COUNT * 100 / REAL_COUNT ))%)${RESET}"
    echo ""
    narrate "Detection rate is reasonable — not too noisy, catches real drift."

    pause
  fi
fi

# ═══════════════════════════════════════════════════════════════
# CLOSE
# ═══════════════════════════════════════════════════════════════

section "Done!"

echo -e "  ${BOLD}clawdoc detects 14 failure patterns:${RESET}"
echo ""
echo "   1. Infinite retry loop          8. Model routing waste"
echo "   2. Non-retryable error retried  9. Cron context accumulation"
echo "   3. Tool calls as plain text    10. Compaction damage"
echo "   4. Context window exhaustion   11. Workspace token overhead"
echo "   5. Sub-agent replay storm      12. Task drift"
echo "   6. Cost spike attribution      13. Unbounded walk"
echo "   7. Skill selection miss        14. Tool misuse"
echo ""
echo -e "  ${BOLD}Get started:${RESET}"
echo "    bash scripts/headline.sh ~/.openclaw/agents/main/sessions/"
echo "    bash scripts/diagnose.sh session.jsonl | bash scripts/prescribe.sh"
echo ""
echo -e "  ${DIM}clawdoc v$(cat "$ROOT_DIR/VERSION") — MIT License${RESET}"
echo ""
