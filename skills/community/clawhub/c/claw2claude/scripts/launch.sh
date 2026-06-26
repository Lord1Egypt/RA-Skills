#!/usr/bin/env bash
# claw2claude/scripts/launch.sh
#
# Usage:
#   launch.sh <project_path> discuss    "<prompt>" [<session_key>]
#   launch.sh <project_path> execute    "<prompt>" [<session_key>]
#   launch.sh <project_path> continue   "<prompt>" [<session_key>]
#   launch.sh <project_path> background "<prompt>" [<session_key>]
#
# session_key: OpenClaw session key for result delivery (e.g. "discord:123:456").
#              Defaults to "main". Must match the channel the user is chatting in.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_PATH="${1:-}"
MODE="${2:-execute}"
PROMPT="${3:-}"
SESSION_KEY="${4:-}"

SESSION_FILE=".openclaw-claude-session.json"
TMPDIR_BASE="/tmp/claw2claude-$$"
TIMEOUT_SEC=1800  # 30 minutes
LOGS_DIR="$SKILL_DIR/logs"
mkdir -p "$LOGS_DIR"
LOG_FILE="$LOGS_DIR/$(date +%Y-%m).log"

# ── Logging helper ───────────────────────────────────────────────
log_entry() {
  # Append a JSON line to the monthly log file.
  # Args: <status> [<claude_session_id>]
  local status="${1:-}"
  local claude_session="${2:-}"
  python3 "$SKILL_DIR/scripts/log_entry.py" \
    --log-file    "$LOG_FILE" \
    --status      "$status" \
    --project     "$PROJECT_PATH" \
    --mode        "$MODE" \
    --session-key "$SESSION_KEY" \
    --claude-session "$claude_session" \
    --prompt      "${PROMPT:0:200}" \
    2>/dev/null || true   # never let logging crash the main flow
}

# ── Validate dependencies ────────────────────────────────────────
if ! command -v claude &>/dev/null; then
  echo "❌ claude command not found — please install Claude Code CLI" >&2
  exit 1
fi

# ── Validate MODE ────────────────────────────────────────────────
case "$MODE" in
  discuss|execute|continue|background) ;;
  *)
    echo "❌ Invalid mode: '$MODE' (valid values: discuss | execute | continue | background)" >&2
    exit 1
    ;;
esac

# ── Validate arguments ───────────────────────────────────────────
if [[ -z "$PROJECT_PATH" ]]; then
  echo "❌ Missing project path argument" >&2
  exit 1
fi
PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"

# ── Cleanup on exit ──────────────────────────────────────────────
NOTIFIER_PID_FILE=""
cleanup() {
  # Do NOT kill the notifier here — it is a nohup background process that must
  # outlive launch.sh to deliver results after Claude finishes.
  # Only clean up temp files.
  rm -rf "$TMPDIR_BASE"
}
trap cleanup EXIT
mkdir -p "$TMPDIR_BASE"
SESSION_ID_FILE="$TMPDIR_BASE/session_id"

# ── Create / enter project directory ────────────────────────────
if [[ ! -d "$PROJECT_PATH" ]]; then
  mkdir -p "$PROJECT_PATH"
  echo "📁 Created project directory: $PROJECT_PATH" >&2
  cd "$PROJECT_PATH"
  git init -q
  echo "📦 Initialised Git repository" >&2
  echo ".openclaw-claude-session.json" >> .gitignore
  echo "📝 Added session file to .gitignore" >&2
else
  echo "📂 Using project directory: $PROJECT_PATH" >&2
  cd "$PROJECT_PATH"
  # Add session file to .gitignore if not already excluded
  # (covers both existing .gitignore and the case where none exists yet)
  if ! grep -qF ".openclaw-claude-session.json" .gitignore 2>/dev/null; then
    echo ".openclaw-claude-session.json" >> .gitignore
  fi
fi

# ── Validate and auto-detect session key ─────────────────────────
# A valid session key looks like: agent:<agent>:<platform>:<type>:<id>
# If $4 was provided but contains prompt content (e.g. newlines caused arg
# misparse), it won't match this pattern — discard it and auto-detect instead.
SESSION_KEY_VALID=false
if [[ "$SESSION_KEY" =~ ^agent:[^:]+:[^:]+:[^:]+:.+$ ]]; then
  SESSION_KEY_VALID=true
fi

if [[ "$SESSION_KEY_VALID" != "true" ]]; then
  if [[ -n "$SESSION_KEY" ]]; then
    echo "⚠️  SESSION_KEY looks malformed ('${SESSION_KEY:0:40}…') — ignoring and auto-detecting" >&2
  fi
  # launch.sh runs the moment the AI handles the user's message, so the user's
  # channel has the most recent updatedAt in sessions.json right now.
  DETECTED_KEY=$(python3 "$SKILL_DIR/scripts/find_session.py" 2>/dev/null || true)
  if [[ -n "$DETECTED_KEY" ]]; then
    SESSION_KEY="$DETECTED_KEY"
    echo "🔑 Auto-detected session key: $SESSION_KEY" >&2
  else
    SESSION_KEY="main"
    echo "⚠️  Could not detect session key — falling back to 'main'" >&2
  fi
else
  echo "🔑 Using provided session key: $SESSION_KEY" >&2
fi

# ── Check token health ───────────────────────────────────────────
python3 "$SKILL_DIR/scripts/check_token.py" || true

# ── Register project and print registry for AI reference ────────
PROJECT_NAME="$(basename "$PROJECT_PATH")"
python3 "$SKILL_DIR/scripts/projects.py" register "$PROJECT_PATH" "$PROJECT_NAME" > /dev/null
echo "── Registered projects ──" >&2
python3 "$SKILL_DIR/scripts/projects.py" list >&2
echo "─────────────────────────" >&2

# ── Read previous session state ──────────────────────────────────
LAST_SESSION_ID=""
LAST_MODE=""
if [[ -f "$SESSION_FILE" ]]; then
  LAST_SESSION_ID=$(python3 "$SKILL_DIR/scripts/read_session.py" "$SESSION_FILE" session_id)
  LAST_MODE=$(python3 "$SKILL_DIR/scripts/read_session.py" "$SESSION_FILE" mode)
fi

# ── Background mode: launch detached, return immediately ─────────
if [[ "$MODE" == "background" ]]; then
  if [[ -z "$PROMPT" ]]; then
    echo "❌ Background mode requires a prompt — no instruction provided" >&2
    exit 1
  fi

  BG_LOG="${PROJECT_PATH}/.claude-bg.log"
  echo "🚀 Launching Claude Code in background..." >&2
  echo "📋 Log: $BG_LOG" >&2

  # Background always runs as execute (discuss/continue not supported in detached mode)
  nohup bash "$0" "$PROJECT_PATH" execute "$PROMPT" > "$BG_LOG" 2>&1 &
  BG_PID=$!
  echo "🔧 PID=$BG_PID" >&2

  # Start heartbeat to monitor the background process
  nohup python3 "$SKILL_DIR/scripts/heartbeat.py" \
    --pid "$BG_PID" \
    --log "$BG_LOG" \
    --project "$PROJECT_NAME" \
    --session-key "$SESSION_KEY" \
    > "${BG_LOG%.log}-heartbeat.log" 2>&1 &

  echo "✅ Background task started (PID=$BG_PID) — you will be notified when it completes" >&2
  exit 0
fi

# ── Determine effective mode (used for session label) ────────────
EFFECTIVE_MODE="$MODE"
if [[ "$MODE" == "continue" ]]; then
  EFFECTIVE_MODE="${LAST_MODE:-execute}"
fi
SESSION_LABEL="${PROJECT_NAME}:${EFFECTIVE_MODE}"

# ── Build Claude arguments ───────────────────────────────────────
CLAUDE_ARGS=(--print --output-format stream-json --verbose --name "$SESSION_LABEL")

case "$MODE" in
  discuss)
    CLAUDE_ARGS+=(--dangerously-skip-permissions)
    echo "💬 Discuss mode" >&2
    ;;

  execute)
    CLAUDE_ARGS+=(--dangerously-skip-permissions)
    echo "⚡ Execute mode (all permission prompts skipped)" >&2
    # Always resume the previous session if one exists (discuss or execute)
    if [[ -n "$LAST_SESSION_ID" ]]; then
      CLAUDE_ARGS+=(--resume "$LAST_SESSION_ID")
      if [[ "$LAST_MODE" == "discuss" ]]; then
        echo "🔗 Carrying over discussion context (session: ${LAST_SESSION_ID:0:8}...)" >&2
      else
        echo "🔗 Resuming previous execute session (${LAST_SESSION_ID:0:8}...)" >&2
      fi
    fi
    ;;

  continue)
    if [[ -n "$LAST_SESSION_ID" ]]; then
      CLAUDE_ARGS+=(--resume "$LAST_SESSION_ID")
      CLAUDE_ARGS+=(--dangerously-skip-permissions)
      echo "🔄 Resuming ${LAST_MODE:-execute} session (${LAST_SESSION_ID:0:8}...)" >&2
    else
      CLAUDE_ARGS+=(--dangerously-skip-permissions)
      echo "⚠️  No previous session found — starting a new execute session" >&2
    fi
    ;;
esac

# Appended to every prompt — instructs Claude to end with a structured chat summary
SUMMARY_INSTRUCTION='

---
IMPORTANT: At the very end of your response, write a section in this exact format:

---CHAT_SUMMARY_START---
Write a thorough summary (200–1000 words) of this session to be sent directly to the user as a chat message.

Rules:
1. Language: match the language the user used in their instruction. You may reason in any language, but the summary must be written in the same language as the user'\''s request.
2. Length: do not over-compress. Cover all meaningful outcomes — be specific, not vague.
3. Code & files: if any files were created or modified, list them explicitly (filename + one-line description of what changed or was added).
4. Structure: use short paragraphs or bullet points for readability. No fenced code blocks.
---CHAT_SUMMARY_END---'

# ── Append prompt ────────────────────────────────────────────────
if [[ -n "$PROMPT" ]]; then
  # Prompt provided: pass it directly. Uses --resume (set above) to carry prior context.
  CLAUDE_ARGS+=("${PROMPT}${SUMMARY_INSTRUCTION}")
elif [[ "$MODE" == "continue" ]]; then
  if [[ -n "$LAST_SESSION_ID" ]]; then
    # No new prompt: use --continue to restore the full prior conversation interactively.
    # Rebuilds args from scratch because --continue is mutually exclusive with --resume.
    CLAUDE_ARGS=(--print --output-format stream-json --verbose --name "$SESSION_LABEL" --continue --dangerously-skip-permissions)
  else
    # No previous session and no new prompt — nothing to continue
    echo "⚠️  Cannot continue: no previous session exists for this project and no new instruction was provided" >&2
    echo "💡 Please provide an instruction, or use execute mode to start a new task" >&2
    exit 1
  fi
fi

# ── Log invocation start ─────────────────────────────────────────
log_entry "started" "$LAST_SESSION_ID"

# ── Launch Claude ────────────────────────────────────────────────
echo "🤖 Starting Claude Code..." >&2
echo "📍 $PROJECT_PATH" >&2
echo "─────────────────────────────────" >&2

# Use timeout if available
if command -v timeout &>/dev/null; then
  CMD_PREFIX=(timeout "$TIMEOUT_SEC")
elif command -v gtimeout &>/dev/null; then
  CMD_PREFIX=(gtimeout "$TIMEOUT_SEC")
else
  CMD_PREFIX=()
fi

# Full output is saved to this log file; stdout only returns a summary
RUN_LOG="${PROJECT_PATH}/.claude-last-run.log"
NOTIFY_FILE="${PROJECT_PATH}/.claude-notify.json"

# Remove any stale notify file from a previous run
rm -f "$NOTIFY_FILE"

# Kill any stale notifier from a previous run of this project
NOTIFIER_PID_PERSIST="${PROJECT_PATH}/.claude-notifier.pid"
if [[ -f "$NOTIFIER_PID_PERSIST" ]]; then
  STALE_PID=$(cat "$NOTIFIER_PID_PERSIST" 2>/dev/null || true)
  if [[ -n "$STALE_PID" ]]; then
    kill "$STALE_PID" 2>/dev/null && echo "🧹 Killed stale notifier (PID=$STALE_PID)" >&2 || true
  fi
  rm -f "$NOTIFIER_PID_PERSIST"
fi

# ── Start notifier in background ─────────────────────────────────
# The notifier polls for NOTIFY_FILE (written by parse_stream.py when Claude
# finishes) and sends chunked results directly to the OpenClaw gateway.
# It watches $$ (this shell's PID) so it can detect abnormal exits too.
NOTIFIER_LOG="${PROJECT_PATH}/.claude-notifier.log"
NOTIFIER_PID_FILE="$TMPDIR_BASE/notifier_pid"
nohup python3 "$SKILL_DIR/scripts/notifier.py" \
  --notify-file "$NOTIFY_FILE" \
  --project     "$PROJECT_NAME" \
  --session-key "$SESSION_KEY" \
  --watcher-pid $$ \
  --max-wait    $((TIMEOUT_SEC + 120)) \
  > "$NOTIFIER_LOG" 2>&1 &
NOTIFIER_PID=$!
echo "$NOTIFIER_PID" > "$NOTIFIER_PID_FILE"
echo "$NOTIFIER_PID" > "$NOTIFIER_PID_PERSIST"
echo "🔔 Notifier started (PID=$NOTIFIER_PID)" >&2

# ── Run Claude and pipe output through the stream parser ──────────
set +e
if [ ${#CMD_PREFIX[@]} -gt 0 ]; then
  "${CMD_PREFIX[@]}" claude "${CLAUDE_ARGS[@]}" 2>&1 | python3 -u "$SKILL_DIR/scripts/parse_stream.py" \
    --mode       "$EFFECTIVE_MODE" \
    --project    "$PROJECT_NAME" \
    --session-out "$SESSION_ID_FILE" \
    --notify-out "$NOTIFY_FILE" \
    --log-out    "$RUN_LOG"
else
  claude "${CLAUDE_ARGS[@]}" 2>&1 | python3 -u "$SKILL_DIR/scripts/parse_stream.py" \
    --mode       "$EFFECTIVE_MODE" \
    --project    "$PROJECT_NAME" \
    --session-out "$SESSION_ID_FILE" \
    --notify-out "$NOTIFY_FILE" \
    --log-out    "$RUN_LOG"
fi
PIPE_STATUS=("${PIPESTATUS[@]}")
set -e

CLAUDE_RAW_EXIT=${PIPE_STATUS[0]}
PARSER_EXIT=${PIPE_STATUS[1]}

if [[ "$CLAUDE_RAW_EXIT" -eq 124 ]]; then
  echo "⏰ Claude timed out (>${TIMEOUT_SEC}s) — task was aborted" >&2
fi

# ── Save session state (skip on timeout to avoid saving partial state) ──
if [[ "$CLAUDE_RAW_EXIT" -ne 124 ]] && [[ -f "$SESSION_ID_FILE" ]]; then
  NEW_SESSION_ID=$(cat "$SESSION_ID_FILE")
  if [[ -n "$NEW_SESSION_ID" ]]; then
    if python3 "$SKILL_DIR/scripts/write_session.py" \
      "$SESSION_FILE" "$NEW_SESSION_ID" "$EFFECTIVE_MODE" "$PROJECT_PATH"; then
      echo "💾 Session saved (${NEW_SESSION_ID:0:8}...)" >&2
    else
      echo "⚠️  Failed to save session state — next run will start a new session" >&2
    fi
  fi
fi

# Clean up persisted notifier PID (notifier exits on its own after delivery)
rm -f "$NOTIFIER_PID_PERSIST"

# ── Log completion ────────────────────────────────────────────────
FINAL_SESSION_ID=""
[[ -f "$SESSION_ID_FILE" ]] && FINAL_SESSION_ID=$(cat "$SESSION_ID_FILE" 2>/dev/null || true)

if [[ "$CLAUDE_RAW_EXIT" -eq 124 ]]; then
  log_entry "timeout" "$FINAL_SESSION_ID"
elif [[ "$CLAUDE_RAW_EXIT" -eq 0 && "$PARSER_EXIT" -eq 0 ]]; then
  log_entry "done" "$FINAL_SESSION_ID"
else
  log_entry "error" "$FINAL_SESSION_ID"
fi

[[ "$CLAUDE_RAW_EXIT" -eq 0 && "$PARSER_EXIT" -eq 0 ]] && exit 0 || exit 1
