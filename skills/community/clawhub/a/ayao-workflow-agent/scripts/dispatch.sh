#!/bin/bash
# dispatch.sh — Send a command to a tmux agent session with auto-completion notification
# Usage:
#   dispatch.sh <session> <task_id> <command...>
#   dispatch.sh <session> <task_id> "<legacy shell command string>"
#
# Wraps the agent command so that:
# 1. Task status is updated to "running" before execution
# 2. Agent stdout is captured to a log file for token parsing
# 3. on-complete.sh fires when command finishes (updates status + wakes main session)
# 4. Post-commit force-commit fallback catches agents that forget to commit
#
# Shell compatibility:
#   tmux default-shell on macOS is /bin/zsh.  PIPESTATUS[0] is bash-only; zsh uses
#   pipestatus[1].  The agent command is written to a temp bash script that is
#   executed with `bash` — guarantees bash semantics, avoids send-keys quoting issues.

set -euo pipefail

SESSION="${1:?Usage: dispatch.sh <session> <task_id> <command...>}"
TASK_ID="${2:?}"
shift 2

# Support --prompt-file <file> as first argument after task_id.
# The prompt is copied to a temp file and streamed to the agent command via stdin
# so markdown/code blocks/newlines are preserved without shell-escaping issues.
# Recommended usage:
#   dispatch.sh <session> <task_id> --prompt-file /tmp/prompt.txt codex exec ...
PROMPT_FILE=""
PROMPT_TMP_FILE=""
INJECTED_PROMPT_FILE=""
DISPATCHED=false
MARKED_RUNNING=false
cleanup_prompt_tmp() {
  if [[ "$DISPATCHED" != "true" ]] && [[ -n "${PROMPT_TMP_FILE:-}" ]] && [[ -f "$PROMPT_TMP_FILE" ]]; then
    rm -f "$PROMPT_TMP_FILE"
  fi
  if [[ "$DISPATCHED" != "true" ]] && [[ -n "${INJECTED_PROMPT_FILE:-}" ]] && [[ -f "$INJECTED_PROMPT_FILE" ]]; then
    rm -f "$INJECTED_PROMPT_FILE"
  fi
}
cleanup_dispatch() {
  local ec=$?
  if [[ "$MARKED_RUNNING" == "true" ]] && [[ "$DISPATCHED" != "true" ]]; then
    "$UPDATE_STATUS" "$TASK_ID" "failed" "" "" "$SESSION" >/dev/null 2>&1 || true
  fi
  cleanup_prompt_tmp
  return "$ec"
}
trap cleanup_dispatch EXIT
if [[ "${1:-}" == "--prompt-file" ]]; then
  PROMPT_FILE="${2:?--prompt-file requires a path}"
  shift 2
fi

if [[ ! "$TASK_ID" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "dispatch.sh: TASK_ID must match ^[A-Za-z0-9._-]+$: $TASK_ID" >&2
  exit 1
fi

TASK_SLUG="$TASK_ID"
SESSION_SLUG="$(printf '%s' "$SESSION" | tr -c 'A-Za-z0-9._-' '_')"

make_temp_file() {
  local prefix="$1"
  local tmp_base="${TMPDIR:-/tmp}"
  python3 -c '
import os
import sys
import tempfile

fd, path = tempfile.mkstemp(prefix=sys.argv[1] + ".", dir=sys.argv[2])
os.close(fd)
print(path)
' "$prefix" "${tmp_base%/}"
}

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_DIR="$SKILL_DIR/scripts"

COMMAND_ARGS=()
if [[ "$#" == "1" ]]; then
  while IFS= read -r -d '' _arg; do
    COMMAND_ARGS+=("$_arg")
  done < <(
    python3 - "$1" <<'PY'
import shlex
import sys

try:
    parts = shlex.split(sys.argv[1], posix=True)
except ValueError as exc:
    print(f"dispatch.sh: failed to parse legacy command string: {exc}", file=sys.stderr)
    sys.exit(1)

for part in parts:
    sys.stdout.buffer.write(part.encode("utf-8"))
    sys.stdout.buffer.write(b"\0")
PY
  )
else
  COMMAND_ARGS=("$@")
fi

if [[ "${#COMMAND_ARGS[@]}" == "0" ]]; then
  echo "Usage: dispatch.sh <session> <task_id> [--prompt-file <file>] <command...>" >&2
  exit 1
fi

# Inject optional project context ahead of the planner prompt.
if [[ "$SESSION" == "cc-plan" ]] && [[ -n "$PROMPT_FILE" ]]; then
  _PROMPT_CMD_BIN="$(basename "${COMMAND_ARGS[0]}" 2>/dev/null || true)"
  if [[ "$_PROMPT_CMD_BIN" == "claude" ]]; then
    PROJECT_SLUG=$(
      python3 - <<'PYEOF' 2>/dev/null || echo ""
import json
import os

try:
    tasks_file = os.path.expanduser("~/.openclaw/workspace/swarm/active-tasks.json")
    with open(tasks_file, encoding="utf-8") as f:
        data = json.load(f)
    repo = data.get("repo", "")
    slug = data.get("project") or (os.path.basename(repo.rstrip("/")) if repo else "")
    print(slug)
except Exception:
    pass
PYEOF
    )

    CONTEXT_FILE="$SKILL_DIR/projects/$PROJECT_SLUG/context.md"
    if [[ -n "$PROJECT_SLUG" ]] && [[ -f "$CONTEXT_FILE" ]]; then
      INJECTED_PROMPT_FILE="$(make_temp_file "cc-plan-injected-${TASK_SLUG}")"
      {
        echo "## 项目背景（自动注入）"
        echo ""
        cat "$CONTEXT_FILE"
        echo ""
        echo "---"
        echo ""
        cat "$PROMPT_FILE"
      } > "$INJECTED_PROMPT_FILE"
      PROMPT_FILE="$INJECTED_PROMPT_FILE"
    fi
  fi
fi

if [[ -n "$PROMPT_FILE" ]]; then
  PROMPT_TMP_FILE="$(make_temp_file "agent-swarm-prompt-${TASK_SLUG}-${SESSION_SLUG}")"
  cat "$PROMPT_FILE" > "$PROMPT_TMP_FILE"
  if [[ -n "$INJECTED_PROMPT_FILE" ]] && [[ -f "$INJECTED_PROMPT_FILE" ]]; then
    rm -f "$INJECTED_PROMPT_FILE"
    INJECTED_PROMPT_FILE=""
  fi
fi

ON_COMPLETE="$SCRIPT_DIR/on-complete.sh"
UPDATE_STATUS="$SCRIPT_DIR/update-task-status.sh"
VERBOSE_DISPATCH=$("$SCRIPT_DIR/swarm-config.sh" get notify.verbose_dispatch 2>/dev/null || echo "")

# Log file — human-readable agent output captured by tee
LOG_FILE="/tmp/agent-swarm-${TASK_SLUG}-${SESSION_SLUG}.log"
# JSON sidecar — raw JSON from `claude --output-format json`, used for token parsing
CC_JSON_FILE="/tmp/agent-swarm-${TASK_SLUG}-${SESSION_SLUG}-cc.json"
# Temp bash script executed in the tmux pane
SCRIPT_FILE="$(make_temp_file "agent-swarm-run-${TASK_SLUG}-${SESSION_SLUG}")"

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "❌ tmux session '$SESSION' does not exist" >&2
  exit 1
fi

# ── Detect command mode ──────────────────────────────────────────────────────
_CMD_BIN="$(basename "${COMMAND_ARGS[0]}" 2>/dev/null || true)"
_CC_JSON_MODE=false
if [[ "$_CMD_BIN" == "claude" ]]; then
  for ((i = 1; i < ${#COMMAND_ARGS[@]}; i++)); do
    if [[ "${COMMAND_ARGS[i]}" == "--output-format=json" ]]; then
      _CC_JSON_MODE=true
      break
    fi
    if [[ "${COMMAND_ARGS[i]}" == "--output-format" ]] && (( i + 1 < ${#COMMAND_ARGS[@]} )) && [[ "${COMMAND_ARGS[i + 1]}" == "json" ]]; then
      _CC_JSON_MODE=true
      break
    fi
  done
fi

PROMPT_MODE="none"
if [[ -n "$PROMPT_TMP_FILE" ]]; then
  PROMPT_MODE="stdin"
fi

# ── Build agent runner script ────────────────────────────────────────────────
# The runner script is static; dispatch-specific values are injected via env.
cat > "$SCRIPT_FILE" <<'SCRIPT'
#!/bin/bash
set -uo pipefail

LOG_FILE="${AGENT_SWARM_LOG_FILE:?}"
CC_JSON_FILE="${AGENT_SWARM_CC_JSON_FILE:-}"
ON_COMPLETE="${AGENT_SWARM_ON_COMPLETE:?}"
TASK_ID="${AGENT_SWARM_TASK_ID:?}"
SESSION="${AGENT_SWARM_SESSION:?}"
PROMPT_TMP_FILE="${AGENT_SWARM_PROMPT_TMP_FILE:-}"
PROMPT_MODE="${AGENT_SWARM_PROMPT_MODE:-none}"
CC_JSON_MODE="${AGENT_SWARM_CC_JSON_MODE:-false}"
WORKDIR="$(pwd)"
COMMAND=( "$@" )

cleanup() {
  if [[ -n "${PROMPT_TMP_FILE}" ]] && [[ -f "${PROMPT_TMP_FILE}" ]]; then
    rm -f "${PROMPT_TMP_FILE}"
  fi
}
trap cleanup EXIT

run_agent() {
  case "${PROMPT_MODE}" in
    stdin)
      cat "${PROMPT_TMP_FILE}" | "${COMMAND[@]}"
      ;;
    *)
      "${COMMAND[@]}"
      ;;
  esac
}

if [[ "${#COMMAND[@]}" -eq 0 ]]; then
  echo "dispatch runner: missing command" >&2
  exit 1
fi

if [[ "${CC_JSON_MODE}" == "true" ]]; then
  # stdout only → python intercept → tee to LOG_FILE
  # stderr is not merged so Claude JSON stdout stays parseable
  run_agent 2>/dev/null | python3 -c '
import json
import sys

sidecar = sys.argv[1]
raw = sys.stdin.read()
with open(sidecar, "w", encoding="utf-8") as f:
    f.write(raw)
try:
    obj = json.loads(raw)
    print(obj.get("result") or raw)
except Exception:
    sys.stdout.write(raw)
' "${CC_JSON_FILE}" | tee "${LOG_FILE}"
  EC=${PIPESTATUS[0]}
  COMPLETE_LOG="${CC_JSON_FILE}"
else
  # Standard mode: stdout + stderr piped through tee to LOG_FILE
  run_agent 2>&1 | tee "${LOG_FILE}"
  EC=${PIPESTATUS[0]}
  COMPLETE_LOG="${LOG_FILE}"
fi

# Force-commit any uncommitted changes (catches agents that forget)
FC_EC=0
if [ -n "$(git -C "${WORKDIR}" status --porcelain 2>/dev/null)" ]; then
  git -C "${WORKDIR}" add -- . ':!../../swarm/' ':!../../reports/' ':!../../memory/' \
    2>/dev/null || git -C "${WORKDIR}" add -A
  if [ -n "$(git -C "${WORKDIR}" diff --cached --name-only 2>/dev/null)" ]; then
    git -C "${WORKDIR}" commit -m "feat: ${TASK_ID} auto-commit (agent forgot)" \
      && git -C "${WORKDIR}" push \
      || FC_EC=$?
  fi
fi
[ "${FC_EC}" -ne 0 ] && EC="${FC_EC}"

"${ON_COMPLETE}" "${TASK_ID}" "${SESSION}" "${EC}" "${COMPLETE_LOG}"

SCRIPT

chmod +x "$SCRIPT_FILE"

# ── Mark task as running ─────────────────────────────────────────────────────
# Use if-then-else to capture exit code without triggering set -e on non-zero return.
# update-task-status.sh exits 2 when task is already claimed by another agent.
if "$UPDATE_STATUS" "$TASK_ID" "running" "" "" "$SESSION" 2>&1; then
  CLAIM_EC=0
else
  CLAIM_EC=$?
fi
if [[ "$CLAIM_EC" == "2" ]]; then
  echo "⚠️  $TASK_ID already claimed by another agent — skipping dispatch" >&2
  exit 0
fi
if [[ "$CLAIM_EC" != "0" ]]; then
  exit "$CLAIM_EC"
fi
MARKED_RUNNING=true

# Mark agent as busy in pool
"$SCRIPT_DIR/update-agent-status.sh" "$SESSION" "busy" "$TASK_ID" 2>/dev/null || true

# ── Dispatch to tmux ─────────────────────────────────────────────────────────
# tmux pane only sees `bash /tmp/script.sh` — no quoting issues, no shell compat issues
WRAPPED_ARGS=(
  env
  "AGENT_SWARM_LOG_FILE=$LOG_FILE"
  "AGENT_SWARM_CC_JSON_FILE=$CC_JSON_FILE"
  "AGENT_SWARM_ON_COMPLETE=$ON_COMPLETE"
  "AGENT_SWARM_TASK_ID=$TASK_ID"
  "AGENT_SWARM_SESSION=$SESSION"
  "AGENT_SWARM_PROMPT_TMP_FILE=$PROMPT_TMP_FILE"
  "AGENT_SWARM_PROMPT_MODE=$PROMPT_MODE"
  "AGENT_SWARM_CC_JSON_MODE=$_CC_JSON_MODE"
  bash
  "$SCRIPT_FILE"
  "${COMMAND_ARGS[@]}"
)
printf -v WRAPPED '%q ' "${WRAPPED_ARGS[@]}"
WRAPPED="${WRAPPED% }"

tmux send-keys -t "$SESSION" -l -- "$WRAPPED"
tmux send-keys -t "$SESSION" Enter
DISPATCHED=true

# ── Background heartbeat ─────────────────────────────────────────────────────
# Keeps task.updated_at and agent last_seen fresh every 5 min so health-check.sh doesn't flag us as stuck
HEARTBEAT_PID_FILE="/tmp/agent-swarm-heartbeat-${SESSION}.pid"
(
  while true; do
    sleep 300
    tmux has-session -t "$SESSION" 2>/dev/null || break
    "$UPDATE_STATUS" "$TASK_ID" "running" 2>/dev/null || true
    "$SCRIPT_DIR/update-agent-status.sh" "$SESSION" "busy" "$TASK_ID" 2>/dev/null || true
  done
) >/dev/null 2>&1 &
HEARTBEAT_PID=$!
echo "$HEARTBEAT_PID" > "$HEARTBEAT_PID_FILE"
disown "$HEARTBEAT_PID"

if [[ "$VERBOSE_DISPATCH" == "false" ]]; then
  echo "🚀 $TASK_ID → $SESSION | $(date +%H:%M)"
else
  echo "✅ Dispatched $TASK_ID to $SESSION (script: $SCRIPT_FILE, log: $LOG_FILE)"
fi
