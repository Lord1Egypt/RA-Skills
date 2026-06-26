#!/bin/bash
# squad-watchdog.sh — Health check and auto-restart for a squad
# Called by openclaw cron every 5 minutes
# Usage: squad-watchdog.sh <squad-name>

set -euo pipefail

SQUADS_DIR="${HOME}/.openclaw/workspace/agent-squad/squads"
SQUAD_NAME="${1:?Usage: squad-watchdog.sh <squad-name>}"

# --- Validate squad name ---
if [[ ! "$SQUAD_NAME" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: Invalid squad name '$SQUAD_NAME'."
  exit 1
fi

SQUAD_DIR="${SQUADS_DIR}/${SQUAD_NAME}"
TMUX_SESSION="squad-${SQUAD_NAME}"
LOG_FILE="${SQUAD_DIR}/logs/watchdog.log"

# --- Log rotation (max ~5MB, keep 1 backup) ---
if [ -f "$LOG_FILE" ]; then
  LOG_SIZE=$(wc -c < "$LOG_FILE" 2>/dev/null | tr -d ' ')
  if [ "${LOG_SIZE:-0}" -gt 5242880 ]; then
    mv "$LOG_FILE" "${LOG_FILE}.1"
  fi
fi

# --- Check squad directory exists ---
if [ ! -d "$SQUAD_DIR" ]; then
  echo "ERROR: Squad directory not found: $SQUAD_DIR"
  exit 1
fi

# --- Check python3 ---
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found."
  exit 1
fi

# --- Read squad config (safe via sys.argv) ---
SQUAD_JSON="$SQUAD_DIR/squad.json"
if [ ! -f "$SQUAD_JSON" ]; then
  echo "ERROR: squad.json not found in $SQUAD_DIR"
  exit 1
fi

# Read engine_command, engine_path, project_dir, agent_teams from squad.json
eval "$(python3 -c "
import json, sys, shlex
d = json.load(open(sys.argv[1]))
print(f'ENGINE={shlex.quote(d.get(\"engine\", \"\"))}')
print(f'ENGINE_PATH={shlex.quote(d.get(\"engine_path\", \"\"))}')
print(f'ENGINE_CMD={shlex.quote(d.get(\"engine_command\", \"\"))}')
print(f'PROJECT_DIR={shlex.quote(d.get(\"project_dir\", \"\"))}')
print(f'AGENT_TEAMS={\"true\" if d.get(\"agent_teams\") else \"false\"}')
" "$SQUAD_JSON" 2>/dev/null)"

if [ -z "$ENGINE_CMD" ]; then
  echo "ERROR: Could not read engine_command from squad.json"
  exit 1
fi

# Verify the engine binary still exists at the stored path
if [ -n "$ENGINE_PATH" ] && [ ! -x "$ENGINE_PATH" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] WARNING: Engine binary not found at $ENGINE_PATH" >> "$LOG_FILE"
  echo "ERROR: Engine binary not found at stored path: $ENGINE_PATH"
  exit 1
fi

if [ -z "$PROJECT_DIR" ] || [ ! -d "$PROJECT_DIR" ]; then
  PROJECT_DIR="$SQUAD_DIR"
fi

# Build env-prefixed command
TMUX_CMD="env SQUAD_DIR='${SQUAD_DIR}'"
if [ "$AGENT_TEAMS" = "true" ]; then
  TMUX_CMD="$TMUX_CMD CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1"
fi
TMUX_CMD="$TMUX_CMD $ENGINE_CMD"

RESTART_PROMPT="You are ${SQUAD_NAME}, a persistent AI development coordinator. Your coordination directory is ${SQUAD_DIR} — read ${SQUAD_DIR}/PROTOCOL.md immediately for your complete instructions. Read ${SQUAD_DIR}/logs/coordinator-summary.md if it exists to resume. Check ${SQUAD_DIR}/tasks/pending/ and ${SQUAD_DIR}/tasks/in-progress/. Write code in ${PROJECT_DIR}. Continue working."

# --- Consecutive failure tracking ---
FAIL_COUNT_FILE="${SQUAD_DIR}/logs/.restart-failures"
MAX_FAILURES=3

record_failure() {
  local count=0
  [ -f "$FAIL_COUNT_FILE" ] && count=$(cat "$FAIL_COUNT_FILE" 2>/dev/null | tr -d ' \n')
  count=$(( ${count:-0} + 1 ))
  echo "$count" > "$FAIL_COUNT_FILE"
  echo "$count"
}

reset_failures() {
  rm -f "$FAIL_COUNT_FILE"
}

warn_user() {
  local count="$1"
  echo ""
  echo "============================================="
  echo "  ALERT: Squad '${SQUAD_NAME}' keeps crashing"
  echo "============================================="
  echo ""
  echo "The watchdog has restarted '${SQUAD_NAME}' ${count} times in a row"
  echo "but it keeps failing. This usually means:"
  echo ""
  echo "  1. The engine ($ENGINE) has a configuration issue"
  echo "  2. The engine requires interactive input that can't run in tmux"
  echo "  3. The project directory has a problem"
  echo ""
  echo "Suggested actions:"
  echo "  - Check the log: cat ${LOG_FILE}"
  echo "  - Try running the engine manually: cd ${PROJECT_DIR} && ${ENGINE_CMD}"
  echo "  - Stop the squad to prevent further retries: /agent-squad stop ${SQUAD_NAME}"
  echo ""
  echo "IMPORTANT: Please notify the user about this issue."
  echo "============================================="
  echo ""
}

# --- Check tmux session ---
if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
  # Session exists — check if the engine is still running inside
  PANE_PID="$(tmux list-panes -t "$TMUX_SESSION" -F '#{pane_pid}' 2>/dev/null | head -1)"
  if [ -n "$PANE_PID" ]; then
    if pgrep -P "$PANE_PID" >/dev/null 2>&1; then
      # Engine is running, all good
      reset_failures
      exit 0
    fi
  fi

  # tmux session exists but engine has exited — restart engine inside existing session
  FAIL_COUNT=$(record_failure)
  echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] Engine exited in session $TMUX_SESSION. Restarting... (failure #${FAIL_COUNT})" >> "$LOG_FILE"

  if [ "$FAIL_COUNT" -ge "$MAX_FAILURES" ]; then
    echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] ALERT: ${FAIL_COUNT} consecutive failures, notifying user." >> "$LOG_FILE"
    warn_user "$FAIL_COUNT"
    exit 1
  fi

  tmux send-keys -t "$TMUX_SESSION" "$TMUX_CMD" Enter
  sleep 5
  tmux send-keys -t "$TMUX_SESSION" "$RESTART_PROMPT" Enter
  echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] Engine restarted in existing session." >> "$LOG_FILE"
  echo "RESTARTED: Engine was dead inside tmux session. Restarted (attempt #${FAIL_COUNT})."
  exit 0
fi

# --- tmux session does not exist — full restart ---
FAIL_COUNT=$(record_failure)
echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] Session $TMUX_SESSION not found. Full restart... (failure #${FAIL_COUNT})" >> "$LOG_FILE"

if [ "$FAIL_COUNT" -ge "$MAX_FAILURES" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] ALERT: ${FAIL_COUNT} consecutive failures, notifying user." >> "$LOG_FILE"
  warn_user "$FAIL_COUNT"
  exit 1
fi

tmux new-session -d -s "$TMUX_SESSION" -c "$PROJECT_DIR" "$TMUX_CMD"

{
  sleep 5
  tmux send-keys -t "$TMUX_SESSION" "$RESTART_PROMPT" Enter
} &

echo "[$(date -u +%Y-%m-%dT%H:%M:%S+00:00)] Full restart completed." >> "$LOG_FILE"
echo "RESTARTED: tmux session was gone. Created new session and started engine (attempt #${FAIL_COUNT})."
