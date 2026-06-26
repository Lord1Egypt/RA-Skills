#!/usr/bin/env bash
set -euo pipefail

INPUT="$(cat)"
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

CONFIG="$ROOT/docs/cccc/config.json"
STATE="$ROOT/docs/cccc/state.json"
LOG_DIR="$ROOT/docs/cccc/logs"
mkdir -p "$LOG_DIR"

# Log stop hook input for debugging
STAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
echo "$INPUT" > "$LOG_DIR/stop-$STAMP.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "[cccc-stop] EXIT: jq not available" >&2
  exit 0
fi

# Avoid infinite recursion inside the same Stop hook chain.
# The main skill must run its own internal state-machine loop.
STOP_HOOK_ACTIVE="$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo false)"

if [[ ! -f "$CONFIG" || ! -f "$STATE" ]]; then
  echo "[cccc-stop] EXIT: config.json or state.json not found" >&2
  exit 0
fi

# ── Read from config.json (project-level configuration) ──

LOOP_ENABLED="$(jq -r '.automation.stop_hook_loop_enabled // false' "$CONFIG")"
MODE="$(jq -r '.mode // "supervised-auto"' "$CONFIG")"
MAX_CONTINUATIONS="$(jq -r '.automation.max_stop_hook_continuations // 10' "$CONFIG")"

# ── Read from state.json (runtime state only) ──

STATUS="$(jq -r '.status // "UNKNOWN"' "$STATE")"
CONTINUATIONS="$(jq -r '.stop_hook_continuations // 0' "$STATE")"
PAUSE_REASON="$(jq -r '.pause_reason // empty' "$STATE")"
CURRENT_MILESTONE="$(jq -r '.current_milestone_id // empty' "$STATE")"

# ── Guard conditions ──

if [[ "$LOOP_ENABLED" != "true" ]]; then
  echo "[cccc-stop] EXIT: loop not enabled (automation.stop_hook_loop_enabled = false)" >&2
  exit 0
fi

if [[ "$MODE" != "full-auto-safe" ]]; then
  echo "[cccc-stop] EXIT: mode is '$MODE' (not full-auto-safe)" >&2
  exit 0
fi

case "$STATUS" in
  DONE|COMPLETED|FAILED|PAUSED_FOR_HUMAN|NEEDS_HUMAN|NEEDS_SECRET|SENSITIVE_OPERATION|UNSAFE|PAUSED_FOR_SYSTEM|PAUSED_FOR_CODEX)
    echo "[cccc-stop] EXIT: terminal/pause status = $STATUS" >&2
    exit 0
    ;;
esac

if [[ -n "$PAUSE_REASON" && "$PAUSE_REASON" != "null" ]]; then
  echo "[cccc-stop] EXIT: pause_reason = '$PAUSE_REASON'" >&2
  exit 0
fi

if [[ "$STOP_HOOK_ACTIVE" == "true" ]]; then
  echo "[cccc-stop] EXIT: recursion guard (stop_hook_active = true)" >&2
  exit 0
fi

if [[ "$CONTINUATIONS" -ge "$MAX_CONTINUATIONS" ]]; then
  echo "[cccc-stop] EXIT: continuation budget exhausted ($CONTINUATIONS >= $MAX_CONTINUATIONS)" >&2
  exit 0
fi

# Prevent empty spin: SETUP_COMPLETE with no milestone and no backlog
if [[ "$STATUS" == "SETUP_COMPLETE" ]]; then
  HAS_MILESTONE="no"
  if [[ -n "$CURRENT_MILESTONE" && "$CURRENT_MILESTONE" != "null" ]]; then
    HAS_MILESTONE="yes"
  fi
  HAS_BACKLOG="no"
  if [[ -f "$ROOT/docs/cccc/roadmap.md" || -f "$ROOT/docs/cccc/milestone-backlog.md" ]]; then
    HAS_BACKLOG="yes"
  fi
  if [[ "$HAS_MILESTONE" == "no" && "$HAS_BACKLOG" == "no" ]]; then
    echo "[cccc-stop] EXIT: SETUP_COMPLETE with no milestone or backlog (would empty-spin)" >&2
    exit 0
  fi
fi

# ── Increment continuation counter ──

python3 "$ROOT/.claude/skills/cc-codex-collaborate/scripts/cccc-update-state.py" \
  --set "stop_hook_continuations=$((CONTINUATIONS + 1))" \
  >/dev/null 2>&1 || true

# ── Block the stop and instruct Claude to continue ──

echo "[cccc-stop] BLOCK: continuing loop (status=$STATUS, milestone=$CURRENT_MILESTONE, continuations=$((CONTINUATIONS + 1))/$MAX_CONTINUATIONS)" >&2

jq -n \
  --arg status "$STATUS" \
  --arg milestone "$CURRENT_MILESTONE" \
  --argjson next_continuations "$((CONTINUATIONS + 1))" \
  --argjson max_continuations "$MAX_CONTINUATIONS" \
  '{
    decision: "block",
    reason: (
      "Continue the cc-codex-collaborate state machine. " +
      "The stop-hook is NOT a background worker — it only prevents Claude Code from stopping prematurely. " +
      "You must execute multiple state-machine steps within this continuation. " +
      "Do not stop after a single small step. " +
      "Loop mode is enabled in docs/cccc/config.json (automation.stop_hook_loop_enabled = true, mode = full-auto-safe). " +
      "Current status: " + $status + ". " +
      "Current milestone: " + ($milestone // "") + ". " +
      "Stop-hook continuation budget: " + ($next_continuations|tostring) + "/" + ($max_continuations|tostring) + ". " +
      "Continue executing safe state-machine steps until one of these conditions is reached: DONE, COMPLETED, FAILED, PAUSED_FOR_HUMAN, NEEDS_HUMAN, NEEDS_SECRET, SENSITIVE_OPERATION, UNSAFE, PAUSED_FOR_SYSTEM, PAUSED_FOR_CODEX, Codex review threshold exceeded, or continuation budget exhausted. " +
      "Do not bypass human-intervention, secret, production, wallet, real-money, destructive-operation, or threshold pause conditions."
    )
  }'

exit 0
