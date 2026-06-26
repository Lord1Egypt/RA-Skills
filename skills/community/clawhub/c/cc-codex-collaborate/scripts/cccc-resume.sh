#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"
ROOT="$(cccc_repo_root)"
cd "$ROOT"
CONFIG="docs/cccc/config.json"
STATE="docs/cccc/state.json"

# ── Pre-flight checks ──

if [[ ! -f "$CONFIG" || ! -f "$STATE" ]]; then
  echo "ERROR: docs/cccc/config.json or state.json not found."
  echo "Run /cc-codex-collaborate setup first."
  exit 1
fi

# ── Parse arguments ──

CONFIRM=""
STRATEGY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --confirm) CONFIRM="yes"; shift ;;
    --strategy)
      STRATEGY="$2"
      shift 2
      ;;
    *) shift ;;
  esac
done

# ── Read current state ──

STATUS="$(jq -r '.status // "UNKNOWN"' "$STATE")"
PAUSE_REASON="$(jq -r '.pause_reason // empty' "$STATE")"
CURRENT_MILESTONE="$(jq -r '.current_milestone_id // empty' "$STATE")"
CODEX_UNAVAILABLE_REASON="$(jq -r '.codex_unavailable_reason // empty' "$STATE")"
PREVIOUS_STATUS="$(jq -r '.previous_status // empty' "$STATE")"

# ── Check if resumable ──

RESUMABLE_STATUSES="PAUSED_FOR_HUMAN NEEDS_HUMAN PAUSED_FOR_SYSTEM PAUSED_FOR_CODEX NEEDS_SECRET SENSITIVE_OPERATION UNSAFE FAIL_UNCLEAR REVIEW_THRESHOLD_EXCEEDED"

is_resumable() {
  local s="$1"
  echo "$RESUMABLE_STATUSES" | grep -qw "$s"
}

if ! is_resumable "$STATUS"; then
  echo "Current status: $STATUS"

  # State repair mode: status is active-ish but missing current_milestone_id
  if [[ -z "$CURRENT_MILESTONE" || "$CURRENT_MILESTONE" == "null" ]]; then
    HAS_PLANNING="$(python3 "$SCRIPT_DIR/cccc-detect-workflow.py" has-planning-docs 2>/dev/null || echo "false")"
    if [[ "$HAS_PLANNING" == "true" ]]; then
      echo ""
      echo "## State repair mode"
      echo ""
      echo "Planning docs exist but state.json is missing current_milestone_id."
      echo ""

      CANDIDATE="$(python3 "$SCRIPT_DIR/cccc-detect-workflow.py" find-milestone 2>/dev/null || echo "null")"
      if [[ "$CANDIDATE" != "null" && "$CANDIDATE" != "" ]]; then
        CANDIDATE_ID="$(echo "$CANDIDATE" | jq -r '.id // empty')"
        CANDIDATE_TITLE="$(echo "$CANDIDATE" | jq -r '.title // empty')"
        if [[ -n "$CANDIDATE_ID" ]]; then
          echo "Detected candidate milestone: $CANDIDATE_ID ${CANDIDATE_TITLE:+— $CANDIDATE_TITLE}"
        fi
      fi

      echo ""
      echo "Options:"
      echo "  A. Continue with detected milestone"
      echo "  B. Choose next milestone from roadmap"
      echo "  C. Enter milestone ID manually"
      echo "  D. Re-plan from scratch"
      echo "  E. Exit"
      echo ""

      # Non-interactive repair
      if [[ -n "$STRATEGY" ]]; then
        case "$STRATEGY" in
          use-detected|recommended)
            if [[ -n "$CANDIDATE_ID" ]]; then
              python3 - "$CANDIDATE_ID" "$STATUS" <<'PYREP'
import json, sys
from pathlib import Path
from datetime import datetime, timezone
mid = sys.argv[1]
old_status = sys.argv[2]
state = json.loads(Path("docs/cccc/state.json").read_text())
state["current_milestone_id"] = mid
state["status"] = "READY_TO_CONTINUE"
state["previous_status"] = old_status
state["resume_reason"] = f"State repair: set current_milestone_id to {mid}"
state["resume_strategy"] = "state-repair"
state["stop_hook_continuations"] = 0
state["pause_reason"] = None
state["last_resumed_at"] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
state["last_state_repaired_at"] = state["last_resumed_at"]
state["last_state_repair_reason"] = f"Recovered milestone {mid} from planning docs"
Path("docs/cccc/state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
print(f"State repaired: current_milestone_id = {mid}")
print("Status: READY_TO_CONTINUE")
print("Do NOT skip Codex gates. Do NOT mark milestones as passed without review.")
PYREP
            else
              echo "No candidate milestone found. Cannot repair automatically."
            fi
            ;;
          *)
            echo "Unknown strategy: $STRATEGY"
            echo "Claude Code must ask the user with brainstorm-style options."
            ;;
        esac
      else
        echo "Claude Code must ask the user to select a milestone before proceeding."
      fi
      exit 0
    fi
  fi

  echo "This status is not resumable via /cc-codex-collaborate resume."
  if [[ "$STATUS" == "DONE" || "$STATUS" == "COMPLETED" ]]; then
    echo "The workflow is already complete. Start a new task with /cc-codex-collaborate \"your task\"."
  elif [[ "$STATUS" == "FAILED" ]]; then
    echo "The workflow has failed. Review docs/cccc/ and start a new task."
  elif [[ "$STATUS" == "NOT_INITIALIZED" || "$STATUS" == "SETUP_COMPLETE" ]]; then
    echo "No active workflow. Start a task with /cc-codex-collaborate \"your task\"."
  elif [[ "$STATUS" == "READY_TO_CONTINUE" ]]; then
    echo "The workflow is already ready to continue. Proceed with the state machine."
  fi
  exit 0
fi

# ── Output current pause info ──

echo "cc-codex-collaborate resume"
echo "==========================="
echo ""
echo "Current status: $STATUS"
echo "Pause reason: ${PAUSE_REASON:-none}"
echo "Current milestone: ${CURRENT_MILESTONE:-none}"

if [[ -n "$CODEX_UNAVAILABLE_REASON" && "$CODEX_UNAVAILABLE_REASON" != "null" ]]; then
  echo "Codex unavailable reason: $CODEX_UNAVAILABLE_REASON"
fi

echo ""

# ── Status-specific resume guidance ──

case "$STATUS" in
  PAUSED_FOR_HUMAN|NEEDS_HUMAN)
    echo "## Resume guidance: PAUSED_FOR_HUMAN"
    echo ""
    echo "This workflow paused because human input was required."
    echo "Before resuming, the open questions must be answered."
    echo ""
    echo "Options:"
    echo "  A. Use the recommended approach and continue"
    echo "  B. Choose a more conservative approach"
    echo "  C. Skip the current milestone"
    echo "  D. Continue but record the risk"
    echo "  E. Free-form input"
    echo ""
    if [[ "$STRATEGY" == "recommended" ]]; then
      echo "Strategy: recommended (option A)"
    elif [[ "$STRATEGY" == "skip" ]]; then
      echo "Strategy: skip (option C)"
    elif [[ "$STRATEGY" == "conservative" ]]; then
      echo "Strategy: conservative (option B)"
    else
      echo "Claude Code must ask the user with brainstorm-style options before proceeding."
    fi
    ;;

  PAUSED_FOR_CODEX)
    echo "## Resume guidance: PAUSED_FOR_CODEX"
    echo ""
    echo "This workflow paused because Codex was unavailable."
    echo "Before resuming, Codex availability must be verified."
    echo ""

    # Check Codex availability
    CODEX_CHECK="$("$SCRIPT_DIR/cccc-codex-check.sh" 2>&1)" || true
    CODEX_AVAILABLE="$(jq -r '.codex_available // "unknown"' "$STATE" 2>/dev/null || echo "unknown")"

    if [[ "$CODEX_AVAILABLE" == "true" ]]; then
      echo "Codex is now AVAILABLE."
      echo ""
      echo "Resume will:"
      echo "  - Clear codex_unavailable_reason"
      echo "  - Set status to READY_TO_CONTINUE"
      echo "  - Next step: re-run the missing Codex gate (plan/milestone/final review)"
    else
      echo "Codex is STILL UNAVAILABLE."
      echo "Cannot resume until Codex is configured and available."
      echo ""
      echo "Please:"
      echo "  1. Install or configure Codex CLI"
      echo "  2. Verify: codex --version"
      echo "  3. Run: /cc-codex-collaborate resume"
      exit 0
    fi
    ;;

  PAUSED_FOR_SYSTEM)
    echo "## Resume guidance: PAUSED_FOR_SYSTEM"
    echo ""
    echo "This workflow paused due to a system or API error."
    echo "Before resuming, confirm the error has been resolved."
    echo ""
    echo "Options:"
    echo "  A. I have checked the logs and the issue is resolved, continue"
    echo "  B. View the recent StopFailure logs first"
    echo "  C. Exit without continuing"
    echo "  D. Free-form input"
    echo ""
    if [[ "$STRATEGY" == "recommended" && "$CONFIRM" == "yes" ]]; then
      echo "Strategy: confirmed continue (option A)"
    else
      echo "Claude Code must ask the user to confirm before proceeding."
    fi
    ;;

  NEEDS_SECRET)
    echo "## Resume guidance: NEEDS_SECRET"
    echo ""
    echo "WARNING: Do NOT send real secrets, API keys, wallet private keys, or seed phrases to Claude."
    echo "Configure secrets locally in your environment instead."
    echo ""
    echo "Options:"
    echo "  A. I have configured the secret locally, continue"
    echo "  B. Use mock / dummy / test fixture instead"
    echo "  C. Skip the milestone that requires the secret"
    echo "  D. Exit"
    echo ""
    if [[ "$STRATEGY" == "mock" ]]; then
      echo "Strategy: mock (option B)"
    elif [[ "$STRATEGY" == "skip" ]]; then
      echo "Strategy: skip (option C)"
    else
      echo "Claude Code must ask the user before proceeding."
      echo "NEVER record secret values in decision-log or state."
    fi
    ;;

  SENSITIVE_OPERATION|UNSAFE)
    echo "## Resume guidance: $STATUS"
    echo ""
    echo "WARNING: This workflow paused because a sensitive or unsafe operation was detected."
    echo ""
    echo "Options:"
    echo "  A. Do not continue, remain paused"
    echo "  B. Switch to a safe alternative approach"
    echo "  C. I confirm this is a safe local test operation"
    echo "  D. Skip the current milestone"
    echo "  E. Free-form input"
    echo ""
    echo "PROHIBITED resume scenarios (must remain paused):"
    echo "  - Real money / mainnet transactions"
    echo "  - Real wallet private keys"
    echo "  - Production deployments"
    echo "  - Deleting production data"
    echo "  - Force push / drop database / terraform destroy"
    echo ""
    if [[ "$STRATEGY" == "recommended" ]]; then
      echo "Strategy: remain paused (option A) — safest default"
    elif [[ "$STRATEGY" == "safe-alternative" ]]; then
      echo "Strategy: safe alternative (option B)"
    else
      echo "Default: remain paused. Claude Code must ask the user for explicit confirmation."
    fi
    ;;

  FAIL_UNCLEAR|REVIEW_THRESHOLD_EXCEEDED)
    echo "## Resume guidance: $STATUS"
    echo ""
    echo "Review threshold was exceeded or review result is unclear."
    echo ""
    echo "Options:"
    echo "  A. Pause for manual intervention"
    echo "  B. Allow 1 more review round and continue"
    echo "  C. Record risk and proceed to next milestone"
    echo "  D. Skip current milestone"
    echo "  E. Free-form input"
    echo ""
    if [[ "$STRATEGY" == "extend-review" ]]; then
      echo "Strategy: extend-review (option B)"
    elif [[ "$STRATEGY" == "skip" ]]; then
      echo "Strategy: skip (option D)"
    elif [[ "$STRATEGY" == "recommended" ]]; then
      echo "Strategy: pause for manual intervention (option A) — safest default"
    else
      echo "Claude Code must ask the user before proceeding."
      echo "P0/P1 security issues cannot be skipped."
    fi
    ;;
esac

echo ""

# ── Apply resume if strategy is provided (non-interactive mode) ──

if [[ -n "$STRATEGY" ]]; then
  python3 - "$STATUS" "$STRATEGY" "$CURRENT_MILESTONE" "$PAUSE_REASON" <<'PY'
import json, sys
from pathlib import Path
from datetime import datetime, timezone

status = sys.argv[1]
strategy = sys.argv[2]
milestone = sys.argv[3]
pause_reason = sys.argv[4]

state_path = Path('docs/cccc/state.json')
state = json.loads(state_path.read_text())

# For SENSITIVE_OPERATION/UNSAFE with "recommended" strategy, stay paused
if status in ('SENSITIVE_OPERATION', 'UNSAFE') and strategy == 'recommended':
    print("Remain paused — safest default for sensitive/unsafe operations.")
    sys.exit(0)

# For FAIL_UNCLEAR/REVIEW_THRESHOLD_EXCEEDED with "recommended" strategy, stay paused
if status in ('FAIL_UNCLEAR', 'REVIEW_THRESHOLD_EXCEEDED') and strategy == 'recommended':
    print("Remain paused — manual intervention recommended.")
    sys.exit(0)

# Record previous status
state['previous_status'] = status
state['resume_reason'] = f"Resumed from {status} with strategy: {strategy}"
state['resume_strategy'] = strategy
state['last_resumed_at'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
state['stop_hook_continuations'] = 0

# Handle specific strategies
if strategy == 'skip':
    if milestone:
        blocked = state.get('blocked_milestones', [])
        if milestone not in blocked:
            blocked.append(milestone)
        state['blocked_milestones'] = blocked
    state['pause_reason'] = None
    state['status'] = 'READY_TO_CONTINUE'
elif strategy == 'extend-review':
    # Will be handled by Claude Code state machine
    state['pause_reason'] = None
    state['status'] = 'READY_TO_CONTINUE'
elif strategy in ('recommended', 'conservative', 'mock', 'safe-alternative'):
    # Clear Codex unavailable reason if resuming from PAUSED_FOR_CODEX
    if status == 'PAUSED_FOR_CODEX':
        state['codex_unavailable_reason'] = None
    state['pause_reason'] = None
    state['status'] = 'READY_TO_CONTINUE'
elif strategy == 'confirmed':
    state['pause_reason'] = None
    state['status'] = 'READY_TO_CONTINUE'

state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')

# Write to decision-log
decision_log = Path('docs/cccc/decision-log.md')
timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
entry = f"\n## Resume at {timestamp}\n- Status: {status}\n- Strategy: {strategy}\n- Milestone: {milestone or 'none'}\n- Pause reason: {pause_reason or 'none'}\n- Result: status → READY_TO_CONTINUE\n"
if decision_log.exists():
    decision_log.write_text(decision_log.read_text() + entry)
else:
    decision_log.write_text(f"# Decision Log{entry}")

print(f"Resumed from {status} with strategy: {strategy}")
print(f"Status: READY_TO_CONTINUE")
print(f"Previous status: {status}")
print(f"Resume reason: {state.get('resume_reason', '')}")
print(f"stop_hook_continuations: 0")
print("")
print("Next: Claude Code must continue the state machine.")
print("Do NOT skip Codex gates. Do NOT mark milestones as passed without review.")
PY
fi
