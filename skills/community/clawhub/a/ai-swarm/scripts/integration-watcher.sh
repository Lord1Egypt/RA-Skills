#!/usr/bin/env bash
# integration-watcher.sh v2 — Waits for all subteams, reads their work logs, runs integration review
#
# Usage: integration-watcher.sh <project-dir> <description> <session1> <session2> ... <sessionN>
#
# Each session has its own work log at /tmp/worklog-{session}.md
# Integration reviewer reads ALL work logs for cross-subteam context
# Integration reviewer also maintains its own log at /tmp/worklog-integration-{project}.md
# All work logs are persisted to <project>/docs/history/ for orchestrator traceability

# Ensure PATH includes openclaw + node (for cron/detached contexts)
export PATH="$(dirname "$(command -v openclaw 2>/dev/null || echo /usr/local/bin/openclaw)"):/usr/local/bin:/usr/bin:/bin:$PATH"

set -euo pipefail

PROJECT_DIR="${1:?Usage: integration-watcher.sh <project-dir> <description> <session1> [session2] ...}"
DESCRIPTION="${2:?Missing description}"
shift 2
SESSIONS=("$@")

MAX_PARALLEL=10
if [[ ${#SESSIONS[@]} -lt 1 ]]; then
  echo "Error: need at least 1 session" >&2; exit 1
fi
if [[ ${#SESSIONS[@]} -gt $MAX_PARALLEL ]]; then
  echo "Error: max $MAX_PARALLEL parallel (got ${#SESSIONS[@]})" >&2; exit 1
fi

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SWARM_DIR/swarm.conf" ]] && source "$SWARM_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"
POLL_INTERVAL=60
MAX_REVIEW_LOOPS=3
PROJECT_NAME=$(basename "$PROJECT_DIR")
INTEGRATION_LOG="/tmp/worklog-integration-${PROJECT_NAME}.md"

send_telegram() {
  local msg="$1"
  if [[ -z "$NOTIFY_TARGET" ]]; then
    echo "[integration] No NOTIFY_TARGET configured, skipping notification"
    return 0
  fi
  openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$msg" 2>/dev/null || {
    echo "[integration] ⚠️ Notification send failed"
    echo "$msg" >> "$NOTIFY_FILE"
  }
}

echo "[integration] Watching ${#SESSIONS[@]} subteams: ${SESSIONS[*]}"

# ============================================================
# PHASE 1: Wait for all subteams (builder + review chains)
# ============================================================
all_done() {
  # Check that NO tmux sessions exist for any subteam (builder, review, or fix)
  local active_sessions
  active_sessions=$(tmux ls 2>/dev/null | cut -d: -f1 || echo "")
  
  for sess in "${SESSIONS[@]}"; do
    # Check if builder session still exists
    if echo "$active_sessions" | grep -qE "^${sess}$"; then return 1; fi
    # Check if any review/fix chain sessions exist
    if echo "$active_sessions" | grep -qE "^${sess}-review-"; then return 1; fi
    if echo "$active_sessions" | grep -qE "^${sess}-fix-"; then return 1; fi
  done
  
  # Extra safety: wait for notify-on-complete.sh processes to finish
  for sess in "${SESSIONS[@]}"; do
    if ps aux 2>/dev/null | grep "notify-on-complete.sh.*${sess}" | grep -v grep > /dev/null; then
      return 1
    fi
  done
  
  return 0
}

WAIT_START=$(date +%s)
MAX_WAIT=7200

while ! all_done; do
  sleep "$POLL_INTERVAL"
  ELAPSED=$(( $(date +%s) - WAIT_START ))
  if [[ $ELAPSED -gt $MAX_WAIT ]]; then
    send_telegram "⚠️ Integration watcher timed out after 2h."
    exit 1
  fi
done

# Stabilization: wait 30s then re-check (catches late-spawning review sessions)
echo "[integration] All subteams appear done. Stabilization wait (30s)..."
sleep 30
if ! all_done; then
  echo "[integration] Late sessions detected after stabilization, continuing to wait..."
  while ! all_done; do
    sleep "$POLL_INTERVAL"
    ELAPSED=$(( $(date +%s) - WAIT_START ))
    if [[ $ELAPSED -gt $MAX_WAIT ]]; then
      send_telegram "⚠️ Integration watcher timed out after 2h."
      exit 1
    fi
  done
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[integration] ✅ All ${#SESSIONS[@]} subteams fully complete at $TIMESTAMP"

# ============================================================
# PHASE 2: Collect all subteam work logs
# ============================================================
COMBINED_LOGS=""
for sess in "${SESSIONS[@]}"; do
  SUBLOG="/tmp/worklog-${sess}.md"
  if [[ -f "$SUBLOG" ]]; then
    COMBINED_LOGS="$COMBINED_LOGS

========================================
## Subteam: $sess
========================================
$(cat "$SUBLOG")"
  else
    COMBINED_LOGS="$COMBINED_LOGS

========================================
## Subteam: $sess
========================================
(No work log found)"
  fi
done

# Initialize integration log
cat > "$INTEGRATION_LOG" << ILOG
# Integration Log: $DESCRIPTION
**Project:** $PROJECT_NAME
**Subteams:** ${SESSIONS[*]}
**Started:** $TIMESTAMP

## Subteam Summaries
$COMBINED_LOGS

---
## Integration Review
ILOG

send_telegram "🔗 All ${#SESSIONS[@]} subteams done. Starting integration review with work logs..."

# ============================================================
# PHASE 3: Integration review+fix loop (reads all work logs)
# ============================================================
cd "$PROJECT_DIR"
REVIEW_DEPTH=$(( ${#SESSIONS[@]} * 4 ))
[[ $REVIEW_DEPTH -lt 5 ]] && REVIEW_DEPTH=5
SESSION_LIST="${SESSIONS[*]}"

LOOP=0
PASS="False"
while [[ $LOOP -lt $MAX_REVIEW_LOOPS ]]; do
  LOOP=$((LOOP + 1))
  INTEG_SESSION="integration-${LOOP}"
  VERDICT_FILE="/tmp/review-verdict-${INTEG_SESSION}.json"
  rm -f "$VERDICT_FILE"

  send_telegram "🔗 Integration review+fix $LOOP/$MAX_REVIEW_LOOPS..."

  # Write integration reviewer prompt to file (avoids shell quoting issues)
  INTEG_PROMPT_FILE="/tmp/integration-prompt-${INTEG_SESSION}.md"
  INTEG_LOG_CONTENT=$(cat "$INTEGRATION_LOG")

  cat > "$INTEG_PROMPT_FILE" << INTEG_PROMPT_EOF
You are an INTEGRATION REVIEWER at $PROJECT_DIR. Round $LOOP of $MAX_REVIEW_LOOPS.

## CONTEXT — All Subteam Work Logs:

The following work logs were written by builder and reviewer agents. They document exactly what was changed, why, and any concerns flagged. USE THEM to understand the full scope of changes before reviewing code.

$INTEG_LOG_CONTENT

---

## YOUR TASK:

### STEP 1: Understand the scope
Read the work logs above first. They tell you:
- Which files each subteam touched and why
- What decisions/tradeoffs were made
- Any known issues or integration concerns flagged by builders/reviewers

### STEP 2: Review for CROSS-SUBTEAM issues
  git log --oneline -${REVIEW_DEPTH}
  git diff HEAD~${REVIEW_DEPTH} --stat

Focus on issues that arise from MULTIPLE agents working in parallel:
1. DEPENDENCY CONFLICTS — subteams importing/changing the same modules differently
2. DUPLICATE CODE — parallel agents solving the same problem independently
3. IMPORT/BUILD CONFLICTS — conflicting type definitions, missing exports
4. SHARED STATE — incompatible changes to global state, singletons, event buses
5. API CONTRACT BREAKS — one subteam changed an interface another depends on
6. CONFIG COMPATIBILITY — manifest, build config, environment conflicts

### STEP 3: Fix any issues directly
  git add -A && git commit -m "integration fix (round $LOOP): <description>" && git push 2>/dev/null

### STEP 4: Update the integration log
Append your findings to $INTEGRATION_LOG:

cat >> $INTEGRATION_LOG << 'ILOG_EOF'

### Integration Round $LOOP
- **Timestamp:** $(date '+%Y-%m-%d %H:%M:%S')
- **Cross-team conflicts found:** <list or "None">
- **Duplicated code merged:** <list or "None">
- **Build verified:** <pass/fail>
- **Fixes applied:** <describe or "None needed">
- **Remaining concerns:** <anything for the orchestrator>
ILOG_EOF

### STEP 5: Write verdict file (MANDATORY)
  echo '{"pass": true, "summary": "YOUR SUMMARY HERE", "issues_remaining": ""}' > $VERDICT_FILE
Or if issues remain:
  echo '{"pass": false, "summary": "YOUR SUMMARY", "issues_remaining": "DESCRIBE REMAINING"}' > $VERDICT_FILE
INTEG_PROMPT_EOF

  # Use fallback-swap to get the working integrator command (tests primary, swaps if needed)
  SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
  INTEG_CMD=$("$SWARM_DIR/fallback-swap.sh" integrator 2>/dev/null) || INTEG_CMD="claude --model claude-opus-4-6 --permission-mode bypassPermissions --print"

  INTEG_WRAPPER="/tmp/integ-wrapper-${INTEG_SESSION}.sh"
  if echo "$INTEG_CMD" | grep -q "^gemini"; then
    GEMINI_BASE=$(echo "$INTEG_CMD" | sed 's/ *$//')
    cat > "$INTEG_WRAPPER" << IWRAP_EOF
#!/usr/bin/env bash
cd "$PROJECT_DIR"
$GEMINI_BASE -y -p "\$(cat $INTEG_PROMPT_FILE)"
IWRAP_EOF
  else
    cat > "$INTEG_WRAPPER" << IWRAP_EOF
#!/usr/bin/env bash
cd "$PROJECT_DIR"
$INTEG_CMD "\$(cat $INTEG_PROMPT_FILE)"
IWRAP_EOF
  fi
  chmod +x "$INTEG_WRAPPER"
  tmux new-session -d -s "$INTEG_SESSION" -c "$PROJECT_DIR" "bash $INTEG_WRAPPER"

  while tmux has-session -t "$INTEG_SESSION" 2>/dev/null; do
    sleep "$POLL_INTERVAL"
  done

  # Check verdict file; auto-infer if missing (watcher decides)
  if [[ ! -f "$VERDICT_FILE" ]]; then
    LATEST_MSG=$(cd "$PROJECT_DIR" && git log --oneline -1 2>/dev/null | head -1)
    INTEG_LOG_UPDATED=false
    if [[ -f "$INTEGRATION_LOG" ]] && grep -q "Integration Round $LOOP\|integration.*round $LOOP" "$INTEGRATION_LOG" 2>/dev/null; then
      INTEG_LOG_UPDATED=true
    fi

    if echo "$LATEST_MSG" | grep -qi "integration\|review\|fix\|pass\|clean"; then
      send_telegram "✅ Integration review passed (round $LOOP): fixed issues → $LATEST_MSG"
      PASS="True"
    elif [[ "$INTEG_LOG_UPDATED" == "true" ]]; then
      send_telegram "✅ Integration review passed (round $LOOP): no cross-team issues found"
      PASS="True"
    else
      send_telegram "✅ Integration review auto-passed (round $LOOP): clean exit, no issues indicated"
      PASS="True"
    fi
    break
  fi

  PASS=$(python3 -c "import json; print(json.load(open('$VERDICT_FILE')).get('pass', True))" 2>/dev/null || echo "True")
  SUMMARY=$(python3 -c "import json; print(json.load(open('$VERDICT_FILE')).get('summary', 'No summary'))" 2>/dev/null || echo "")

  if [[ "$PASS" == "True" ]]; then
    send_telegram "✅ Integration review PASSED (round $LOOP): $SUMMARY"
    cd "$PROJECT_DIR" && git commit --allow-empty -m "Integration review $LOOP: passed — $SUMMARY" && git push origin main 2>/dev/null || true
    break
  fi

  send_telegram "🔄 Integration round $LOOP: issues remain — $SUMMARY"
done

if [[ "$PASS" != "True" ]]; then
  send_telegram "⚠️ Integration review maxed ($MAX_REVIEW_LOOPS). Manual review needed."
fi

# ============================================================
# PHASE 4: Persist integration log to project history
# ============================================================
HISTORY_DIR="$PROJECT_DIR/docs/history"
mkdir -p "$HISTORY_DIR"
HISTORY_FILE="$HISTORY_DIR/$(date +%Y-%m-%d)-integration.md"

# Append if multiple integrations same day, otherwise create
if [[ -f "$HISTORY_FILE" ]]; then
  echo "" >> "$HISTORY_FILE"
  echo "---" >> "$HISTORY_FILE"
  echo "" >> "$HISTORY_FILE"
  cat "$INTEGRATION_LOG" >> "$HISTORY_FILE"
else
  cp "$INTEGRATION_LOG" "$HISTORY_FILE"
fi

# Also keep a copy in swarm logs
cp "$INTEGRATION_LOG" "$SWARM_DIR/logs/integration-${PROJECT_NAME}-$(date +%Y%m%d-%H%M).md" 2>/dev/null || true

# Persist subteam work logs to history too
for sess in "${SESSIONS[@]}"; do
  SUBLOG="/tmp/worklog-${sess}.md"
  if [[ -f "$SUBLOG" ]]; then
    cp "$SUBLOG" "$HISTORY_DIR/$(date +%Y-%m-%d)-${sess}.md"
  fi
done

# ============================================================
# PHASE 5: Auto-update ESR
# ============================================================
INTEG_SUMMARY="${SUMMARY:-Integration review completed}"
if [[ -x "$SWARM_DIR/esr-log.sh" ]]; then
  "$SWARM_DIR/esr-log.sh" "$PROJECT_DIR" "### Integration Review — $(date '+%Y-%m-%d %H:%M')
**Subteams:** ${SESSIONS[*]}
**Result:** $INTEG_SUMMARY" 2>/dev/null || echo "[integration] ⚠️ ESR update failed (non-fatal)"
fi

# Commit history + ESR together
cd "$PROJECT_DIR"
git add docs/history/ docs/ESR.md 2>/dev/null || true
git commit -m "docs: auto-update ESR + persist integration history ($(date +%Y-%m-%d))" 2>/dev/null || true
git push origin main 2>/dev/null || git push 2>/dev/null || true

echo "[integration] Work logs + ESR persisted to $HISTORY_DIR"

exit 0
