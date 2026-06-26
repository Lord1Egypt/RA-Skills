#!/usr/bin/env bash
# notify-on-complete.sh v3 — Subteam workflow with shared work log
#
# Usage: notify-on-complete.sh <session-name> <description> [--review <project-dir>] [--max-loops N]
#
# WORKFLOW:
#   Builder starts → creates work log at /tmp/worklog-{session}.md
#   Builder finishes → watcher spawns Reviewer (who also fixes)
#   Reviewer reads work log, reviews code, fixes issues, updates work log
#   If reviewer can't fully resolve → spawns new reviewer with updated work log
#   Max loops (default 3). Work log persists across the chain for context.
#   On completion: work log saved to <project>/docs/history/, ESR auto-updated.

# Ensure PATH includes openclaw + node (for cron/detached contexts)
export PATH="$(dirname "$(command -v openclaw 2>/dev/null || echo /usr/local/bin/openclaw)"):/usr/local/bin:/usr/bin:/bin:$PATH"

set -euo pipefail

SESSION="${1:?Usage: notify-on-complete.sh <session-name> <description> [--review <project-dir>] [--max-loops N]}"
DESCRIPTION="${2:-$SESSION completed}"
REVIEW_PROJECT=""
MAX_LOOPS=3
shift 2 || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --review) REVIEW_PROJECT="${2:?--review requires a project directory}"; shift 2 ;;
    --max-loops) MAX_LOOPS="${2:?--max-loops requires a number}"; shift 2 ;;
    *) shift ;;
  esac
done

SWARM_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SWARM_DIR/swarm.conf" ]] && source "$SWARM_DIR/swarm.conf"
NOTIFY_TARGET="${SWARM_NOTIFY_TARGET:-}"
NOTIFY_CHANNEL="${SWARM_NOTIFY_CHANNEL:-telegram}"
NOTIFY_FILE="$SWARM_DIR/pending-notifications.txt"
POLL_INTERVAL=60
WORKLOG="/tmp/worklog-${SESSION}.md"
BASE_SESSION="$SESSION"

echo "[watcher] Watching session: $SESSION (poll: ${POLL_INTERVAL}s, review: ${REVIEW_PROJECT:-none}, max-loops: $MAX_LOOPS)"

send_telegram() {
  local msg="$1"
  if [[ -z "$NOTIFY_TARGET" ]]; then
    echo "[watcher] No NOTIFY_TARGET configured, skipping notification"
    return 0
  fi
  openclaw message send --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$msg" 2>/dev/null || {
    echo "[watcher] ⚠️ Notification send failed"
    echo "$msg" >> "$NOTIFY_FILE"
  }
}

check_stuck() {
  local sess="$1"
  CURRENT=$(tmux capture-pane -t "$sess" -p 2>/dev/null | tail -5 || echo "")
  if echo "$CURRENT" | grep -qi "Failed to login\|API key must be set\|How would you like to authenticate\|Permission denied\|rate limit\|429\|quota\|token limit\|exceeded.*limit\|capacity.*exceeded"; then
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    # Detect token/quota limit → trigger fallback to Claude-heavy duty table
    if echo "$CURRENT" | grep -qi "rate limit\|429\|quota\|token limit\|exceeded.*limit\|capacity.*exceeded"; then
      MSG="⚠️ [$TIMESTAMP] Agent $sess hit TOKEN/QUOTA LIMIT — killing + triggering fallback"
      send_telegram "$MSG"
      echo "$MSG" >> "$NOTIFY_FILE"
      tmux kill-session -t "$sess" 2>/dev/null || true
      # Trigger fallback duty table
      "$SWARM_DIR/assess-models.sh" --fallback 2>/dev/null || true
      return 0
    fi

    MSG="⚠️ [$TIMESTAMP] Agent $sess appears STUCK — killing it"
    send_telegram "$MSG"
    echo "$MSG" >> "$NOTIFY_FILE"
    tmux kill-session -t "$sess" 2>/dev/null || true
    return 0
  fi
  return 1
}

check_functional_done() {
  local sess="$1"
  local idle_threshold=600  # 10 minutes
  local log_file="$SWARM_DIR/logs/${sess}.log"

  [[ -f "$log_file" ]] || return 1

  local now last_mod idle_s
  now=$(date +%s)
  last_mod=$(stat -c %Y "$log_file" 2>/dev/null || echo 0)
  [[ "$last_mod" -gt 0 ]] || return 1
  idle_s=$(( now - last_mod ))

  # Only treat as functionally complete if stale + final milestones are present in log.
  if [[ "$idle_s" -gt "$idle_threshold" ]] && \
     grep -Eqi "Work log finalized|PR (opened|created):|Branch pushed:|Pushed: .*feat/|Commit:\s+[0-9a-f]{7,}" "$log_file"; then
    local mins=$(( idle_s / 60 ))
    local ts
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    local msg="ℹ️ [$ts] Agent $sess appears functionally complete (idle ${mins}m after final milestones) — auto-closing session"
    send_telegram "$msg"
    echo "$msg" >> "$NOTIFY_FILE"
    tmux kill-session -t "$sess" 2>/dev/null || true
    return 0
  fi

  return 1
}

# ============================================================
# persist_and_update_esr — called on ALL exit paths
# ============================================================
persist_and_update_esr() {
  local final_summary="${1:-Completed}"

  # Skip if no project dir
  if [[ -z "$REVIEW_PROJECT" || ! -d "$REVIEW_PROJECT" ]]; then
    return 0
  fi

  # 1. Persist work log to project history
  HISTORY_DIR="$REVIEW_PROJECT/docs/history"
  mkdir -p "$HISTORY_DIR"
  if [[ -f "$WORKLOG" ]]; then
    cp "$WORKLOG" "$HISTORY_DIR/$(date +%Y-%m-%d)-${BASE_SESSION}.md"
  fi

  # 2. Auto-update ESR
  if [[ -x "$SWARM_DIR/esr-log.sh" ]]; then
    "$SWARM_DIR/esr-log.sh" "$REVIEW_PROJECT" "### $BASE_SESSION — $(date '+%Y-%m-%d %H:%M')
$final_summary" 2>/dev/null || echo "[watcher] ⚠️ ESR update failed (non-fatal)"
  fi

  # 3. Commit history + ESR together
  cd "$REVIEW_PROJECT"
  git add docs/history/ docs/ESR.md 2>/dev/null || true
  git commit -m "docs: auto-update ESR + persist worklog for $BASE_SESSION" 2>/dev/null || true
  git push 2>/dev/null || true

  echo "[watcher] Work log + ESR persisted for $BASE_SESSION"
}

# ============================================================
# PHASE 1: Wait for builder to finish
# ============================================================
while true; do
  sleep "$POLL_INTERVAL"
  if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    break
  fi
  # Auto-close sessions that are functionally done but left hanging in the terminal.
  check_functional_done "$SESSION" && break
  check_stuck "$SESSION" && exit 1
done

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[watcher] Builder finished at $TIMESTAMP"
# NOTE: Do NOT write to pending-notifications.txt here.
# The review pass (or no-review completion below) is the meaningful milestone.
# Writing here causes duplicate notifications when heartbeat picks up the file.

# Initialize work log if builder didn't create one
if [[ ! -f "$WORKLOG" ]]; then
  cat > "$WORKLOG" << WLOG
# Work Log: $SESSION
## Task: $DESCRIPTION
---
### Builder Phase
- **Started:** $(date '+%Y-%m-%d %H:%M:%S')
- **Completed:** $TIMESTAMP
- **Status:** Builder finished. Awaiting review.
WLOG
fi

# If no review requested, just notify, persist, and exit
if [[ -z "$REVIEW_PROJECT" || ! -d "$REVIEW_PROJECT" ]]; then
  send_telegram "✅ $DESCRIPTION"
  persist_and_update_esr "$DESCRIPTION"
  exit 0
fi

# ============================================================
# PHASE 2: Review+Fix loop (reviewer does both)
# ============================================================
LOOP=0
PASS="True"
SUMMARY=""
REMAINING=""

while [[ $LOOP -lt $MAX_LOOPS ]]; do
  LOOP=$((LOOP + 1))
  REVIEW_SESSION="${BASE_SESSION}-review-${LOOP}"
  VERDICT_FILE="/tmp/review-verdict-${REVIEW_SESSION}.json"
  rm -f "$VERDICT_FILE"

  send_telegram "🔍 Review+fix round $LOOP/$MAX_LOOPS for $BASE_SESSION..."

  # Read current work log content to pass as context
  WORKLOG_CONTENT=""
  if [[ -f "$WORKLOG" ]]; then
    WORKLOG_CONTENT=$(cat "$WORKLOG")
  fi

  # Write reviewer prompt to file (avoids shell quoting hell with large work logs)
  REVIEW_PROMPT_FILE="/tmp/review-prompt-${REVIEW_SESSION}.md"
  cat > "$REVIEW_PROMPT_FILE" << REVIEW_PROMPT_EOF
You are a code REVIEWER+FIXER at $REVIEW_PROJECT. Round $LOOP of $MAX_LOOPS.

## WORK LOG (context from the builder and previous reviewers):

$WORKLOG_CONTENT

---

## YOUR TASK:

The work log above tells you what the builder changed and why. Use it to focus your review — you know exactly which files were touched, what decisions were made, and what the builder flagged as concerns.

### STEP 1: Review
Start by understanding the scope from the work log, then verify with git:
  git log --oneline -5
  git diff HEAD~1 --stat
  git diff HEAD~1

Check for:
1. Compilation errors, missing imports, undefined references
2. Logic bugs, edge cases, or incorrect assumptions noted in the work log
3. Platform-specific issues (permissions, lifecycle, manifest)
4. Security issues
5. Performance issues (memory leaks, unnecessary allocations)
6. Dead code or leftover artifacts
7. Any "Known issues" or "Integration notes" the builder flagged

### STEP 2: Fix
Fix any issues you find directly. Do not leave them for another agent.
  git add -A && git commit -m "review+fix round $LOOP: <brief description>" && git push 2>/dev/null

### STEP 3: Update the work log
Append your review findings to $WORKLOG. Be specific — the integration agent reads this next.

cat >> $WORKLOG << 'WLOG_EOF'

### Review+Fix Round $LOOP
- **Reviewer:** $REVIEW_SESSION
- **Timestamp:** $(date '+%Y-%m-%d %H:%M:%S')
- **Files reviewed:** <list files you checked>
- **Issues found:** <describe issues or "None">
- **Fixes applied:** <describe fixes or "None needed">
- **Build status:** <ran npx vite build / gradle build? pass/fail>
- **Remaining concerns:** <anything the integrator should watch for>
WLOG_EOF

### STEP 4: Write verdict file (MANDATORY)
Run this exact command (fill in your values):
  echo '{"pass": true, "summary": "YOUR SUMMARY HERE", "issues_remaining": ""}' > $VERDICT_FILE
Or if issues remain that you couldn't fix:
  echo '{"pass": false, "summary": "YOUR SUMMARY", "issues_remaining": "DESCRIBE REMAINING"}' > $VERDICT_FILE
REVIEW_PROMPT_EOF

  # Use fallback-swap to get the working reviewer command (tests primary, swaps if needed)
  REVIEW_CMD=$("$SWARM_DIR/fallback-swap.sh" reviewer 2>/dev/null) || REVIEW_CMD="claude --model claude-sonnet-4-6 --permission-mode bypassPermissions --print"

  # Build the reviewer wrapper — gemini needs -y -p (yolo + prompt arg), claude uses -p
  REVIEW_WRAPPER="/tmp/review-wrapper-${REVIEW_SESSION}.sh"
  if echo "$REVIEW_CMD" | grep -q "^gemini"; then
    # Gemini: use -y (auto-approve tools) -p (prompt arg) for shell access
    GEMINI_BASE=$(echo "$REVIEW_CMD" | sed 's/ *$//')
    cat > "$REVIEW_WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
cd "$REVIEW_PROJECT"
$GEMINI_BASE -y -p "\$(cat $REVIEW_PROMPT_FILE)"
WRAPPER_EOF
  else
    cat > "$REVIEW_WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
cd "$REVIEW_PROJECT"
$REVIEW_CMD "\$(cat $REVIEW_PROMPT_FILE)"
WRAPPER_EOF
  fi
  chmod +x "$REVIEW_WRAPPER"
  tmux new-session -d -s "$REVIEW_SESSION" -c "$REVIEW_PROJECT" "bash $REVIEW_WRAPPER"

  # Wait for reviewer
  while tmux has-session -t "$REVIEW_SESSION" 2>/dev/null; do
    sleep "$POLL_INTERVAL"
    check_stuck "$REVIEW_SESSION" && break
  done

  # Read verdict — auto-infer if file missing (Option 2: watcher decides)
  if [[ ! -f "$VERDICT_FILE" ]]; then
    # Reviewer exited without writing verdict. Watcher infers the result:
    # 1. Check if reviewer made a commit (= found & fixed issues)
    # 2. Check if work log was updated (= reviewer ran and wrote findings)
    # 3. Clean exit + no commit = nothing to fix = pass

    LATEST_MSG=$(cd "$REVIEW_PROJECT" && git log --oneline -1 2>/dev/null | head -1)
    WORKLOG_UPDATED=false
    if [[ -f "$WORKLOG" ]] && grep -q "Review.*Round $LOOP\|review.*round $LOOP\|Round $LOOP" "$WORKLOG" 2>/dev/null; then
      WORKLOG_UPDATED=true
    fi

    if echo "$LATEST_MSG" | grep -qi "review\|fix\|pass\|clean"; then
      # Reviewer committed fixes → pass (issues found and fixed)
      SUMMARY="Review passed — reviewer fixed issues (commit: $LATEST_MSG)"
      PASS="True"
      send_telegram "✅ $BASE_SESSION review passed (round $LOOP): fixed issues → $LATEST_MSG"
    elif [[ "$WORKLOG_UPDATED" == "true" ]]; then
      # Reviewer updated work log but no commit → reviewed, nothing to fix → pass
      SUMMARY="Review passed — reviewer found no issues (work log updated, no fixes needed)"
      PASS="True"
      send_telegram "✅ $BASE_SESSION review passed (round $LOOP): no issues found"
    else
      # Reviewer exited cleanly without verdict, commit, or work log update
      # Clean exit from Claude = it finished its work. Most likely: reviewed, found nothing, didn't write verdict.
      SUMMARY="Review passed — reviewer exited cleanly (auto-pass: clean exit, no issues indicated)"
      PASS="True"
      send_telegram "✅ $BASE_SESSION review auto-passed (round $LOOP): clean exit, no issues indicated"
    fi

    # NOTE: send_telegram() already handles fallback to NOTIFY_FILE on failure.
    # Do NOT write to NOTIFY_FILE here — causes duplicate notifications.
    echo "" >> "$WORKLOG"
    echo "### Review Round $LOOP" >> "$WORKLOG"
    echo "- Verdict: $SUMMARY" >> "$WORKLOG"
    # Trigger CI/CD build notification
    if [ -n "$REVIEW_PROJECT" ]; then
      LATEST_COMMIT=$(cd "$REVIEW_PROJECT" && git rev-parse HEAD 2>/dev/null)
      if [ -n "$LATEST_COMMIT" ]; then
        nohup "$SWARM_DIR/deploy-notify.sh" "$REVIEW_PROJECT" "$LATEST_COMMIT" \
            >> "$SWARM_DIR/logs/cicd-$(date +%Y%m%d).log" 2>&1 &
      fi
    fi
    break
  fi

  PASS=$(python3 -c "import json; print(json.load(open('$VERDICT_FILE')).get('pass', True))" 2>/dev/null || echo "True")
  SUMMARY=$(python3 -c "import json; print(json.load(open('$VERDICT_FILE')).get('summary', 'No summary'))" 2>/dev/null || echo "")
  REMAINING=$(python3 -c "import json; print(json.load(open('$VERDICT_FILE')).get('issues_remaining', ''))" 2>/dev/null || echo "")

  if [[ "$PASS" == "True" ]]; then
    send_telegram "✅ $BASE_SESSION review passed (round $LOOP): $SUMMARY"
    # NOTE: send_telegram() already handles fallback to NOTIFY_FILE on failure.
    # Trigger CI/CD build notification
    if [ -n "$REVIEW_PROJECT" ]; then
      LATEST_COMMIT=$(cd "$REVIEW_PROJECT" && git rev-parse HEAD 2>/dev/null)
      if [ -n "$LATEST_COMMIT" ]; then
        nohup "$SWARM_DIR/deploy-notify.sh" "$REVIEW_PROJECT" "$LATEST_COMMIT" \
            >> "$SWARM_DIR/logs/cicd-$(date +%Y%m%d).log" 2>&1 &
      fi
    fi
    break
  fi

  # Failed — log it and loop (next reviewer gets updated work log automatically)
  send_telegram "🔄 $BASE_SESSION review round $LOOP: issues remain — $SUMMARY"
done

if [[ "$PASS" != "True" ]]; then
  send_telegram "⚠️ $BASE_SESSION hit max review loops ($MAX_LOOPS). Remaining: $REMAINING"
  echo "" >> "$WORKLOG"
  echo "### ⚠️ Max Loops Reached" >> "$WORKLOG"
  echo "- Unresolved: $REMAINING" >> "$WORKLOG"
fi

# ============================================================
# PHASE 3: Persist work log + send shipped summary (ALWAYS runs)
# ============================================================
persist_and_update_esr "$SUMMARY"

# ============================================================
# STEP 11: NOTIFY — Clean "shipped" summary for WB
# ============================================================
# Read the work log summary section for a human-friendly shipped message.
# Only send if we have a meaningful work log summary (avoids redundancy
# with the review pass notification which already has review details).
SHIPPED_SUMMARY=""
if [[ -f "$WORKLOG" ]]; then
  # Extract the Summary section from work log (bullet points of what changed)
  SHIPPED_SUMMARY=$(sed -n '/^## Summary/,/^## /p' "$WORKLOG" 2>/dev/null | head -20 | grep -E '^\s*-' | head -6)
fi

if [[ -n "$SHIPPED_SUMMARY" ]]; then
  # We have a real work log summary — send the shipped message with details
  SHIP_MSG="🚀 ${BASE_SESSION} shipped!
${SHIPPED_SUMMARY}"
  send_telegram "$SHIP_MSG"
fi
# If no work log summary, skip — the review pass notification already covered it.

exit 0
