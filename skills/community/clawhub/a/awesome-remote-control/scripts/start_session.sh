#!/usr/bin/env bash
# Start a Claude Code remote control session in tmux with bypass permissions.
# Supports multiple concurrent sessions — each gets a friendly animal name.
#
# Usage: start_session.sh <working-dir> [--resume [uuid]]

WORKDIR="${1:?Usage: start_session.sh <working-dir> [--resume [uuid]]}"
RESUME=""
RESUME_UUID=""

shift 2>/dev/null || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --resume)
      RESUME="--resume"
      shift
      # Accept optional UUID (next arg that doesn't start with --)
      if [[ -n "${1:-}" && ! "$1" =~ ^-- ]]; then
        RESUME_UUID="$1"; shift
      fi
      ;;
    *) shift ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Idle timeout from single source of truth (#24) ──────────────────────────
IDLE_TIMEOUT=$(python3 "$SCRIPT_DIR/registry.py" idle-timeout)

STATE_DIR="$HOME/.local/share/claude-rc"
NAME_LOCK="$STATE_DIR/name.lock"

# Create state dir with restricted permissions (#7)
python3 "$SCRIPT_DIR/registry.py" ensure-dir

# ── Animal name generator ────────────────────────────────────────────────────

ANIMALS=(
  "🦊 Fox" "🐻 Bear" "🐼 Panda" "🐨 Koala" "🦁 Lion"
  "🐯 Tiger" "🐺 Wolf" "🦝 Raccoon" "🦦 Otter" "🦔 Hedgehog"
  "🐸 Frog" "🦋 Moth" "🐙 Octopus" "🦈 Shark" "🐊 Croc"
  "🦜 Parrot" "🦚 Peacock" "🦩 Flamingo" "🦉 Owl" "🐧 Penguin"
  "🦭 Seal" "🦬 Bison" "🦌 Deer" "🐐 Goat" "🦘 Kangaroo"
  "🐘 Elephant" "🦏 Rhino" "🦛 Hippo" "🐪 Camel" "🦒 Giraffe"
)

pick_animal() {
  echo "${ANIMALS[$((RANDOM % ${#ANIMALS[@]}))]}"
}

# ── Prune stale entries on startup ───────────────────────────────────────────
python3 "$SCRIPT_DIR/registry.py" prune

# ── Pre-trust workspace with flock (#5) ──────────────────────────────────────
python3 "$SCRIPT_DIR/registry.py" trust-workspace "$WORKDIR"

# ── Derive dir basename — sanitised to safe chars (#9) ───────────────────────

DIRBASE=$(basename "$WORKDIR")
DIRBASE=$(echo "$DIRBASE" | tr -cd '[:alnum:]._-')

# ── Pick a unique animal name + create tmux (locked for parallel safety) ─────

MAX_NAME_ATTEMPTS=60

(
  flock 8

  ATTEMPTS=0
  while true; do
    ANIMAL=$(pick_animal)
    ANIMAL_SLUG=$(echo "$ANIMAL" | sed 's/[^ ]* //' | tr '[:upper:]' '[:lower:]')
    SESSION_LABEL="$ANIMAL | $DIRBASE"
    TMUX_NAME="cc-$ANIMAL_SLUG-$DIRBASE"
    TMUX_NAME=$(echo "$TMUX_NAME" | tr ' ' '-' | tr -cd '[:alnum:]-')
    if ! tmux has-session -t "$TMUX_NAME" 2>/dev/null; then
      break
    fi
    ATTEMPTS=$((ATTEMPTS + 1))
    if [[ $ATTEMPTS -ge $MAX_NAME_ATTEMPTS ]]; then
      echo "Error: could not find an available session name after $MAX_NAME_ATTEMPTS attempts." >&2
      echo "All animal names may be in use for '$DIRBASE'." >&2
      exit 1
    fi
  done

  # Create tmux session while still holding the lock — prevents another
  # process from picking the same name before the session exists.
  if ! tmux new-session -d -s "$TMUX_NAME" -c "$WORKDIR"; then
    echo "Error: failed to create tmux session '$TMUX_NAME'." >&2
    exit 1
  fi

  # Export chosen names for the outer shell
  echo "$ANIMAL" > "$STATE_DIR/.name_$$"
  echo "$ANIMAL_SLUG" >> "$STATE_DIR/.name_$$"
  echo "$SESSION_LABEL" >> "$STATE_DIR/.name_$$"
  echo "$TMUX_NAME" >> "$STATE_DIR/.name_$$"

) 8>"$NAME_LOCK"
subshell_rc=$?

if [[ $subshell_rc -ne 0 ]]; then
  exit 1
fi

# Read back the names chosen under lock
{
  read -r ANIMAL
  read -r ANIMAL_SLUG
  read -r SESSION_LABEL
  read -r TMUX_NAME
} < "$STATE_DIR/.name_$$"
rm -f "$STATE_DIR/.name_$$"

echo "Starting session: $SESSION_LABEL  (tmux: $TMUX_NAME)"

# ── Cleanup trap: kill orphaned tmux session if interrupted during setup ─────
cleanup_session() {
  echo "Interrupted — killing unregistered tmux session $TMUX_NAME" >&2
  tmux kill-session -t "$TMUX_NAME" 2>/dev/null || true
  exit 130
}
trap cleanup_session INT TERM

# ── Start claude in tmux ─────────────────────────────────────────────────────
# CLAUDE_CODE_EXIT_AFTER_STOP_DELAY makes Claude auto-exit after being idle at
# the prompt for IDLE_TIMEOUT. This is the primary idle-kill mechanism — Claude
# handles the timer internally and fires SessionEnd on exit (which triggers
# on_session_end.sh for registry update).

IDLE_DELAY_MS=$((IDLE_TIMEOUT * 1000))

CLAUDE_ARGS="--dangerously-skip-permissions --remote-control --name \"$SESSION_LABEL\""
if [[ "$RESUME" == "--resume" ]]; then
  if [[ -n "$RESUME_UUID" ]]; then
    CLAUDE_ARGS="-r \"$RESUME_UUID\" $CLAUDE_ARGS"
  else
    CLAUDE_ARGS="--continue $CLAUDE_ARGS"
  fi
fi

CMD="CLAUDE_CODE_EXIT_AFTER_STOP_DELAY=$IDLE_DELAY_MS claude $CLAUDE_ARGS"

tmux send-keys -t "$TMUX_NAME" "$CMD" Enter

# ── Capture URL ───────────────────────────────────────────────────────────────
# URL appears in tmux pane within ~2-3s (Claude Code prints it immediately).
# UUID is captured by on_session_end.sh when the session dies (SessionEnd hook).

URL=""

for i in {1..15}; do
  sleep 1
  PANE_URL=$(tmux capture-pane -t "$TMUX_NAME" -p 2>/dev/null | grep -o 'https://claude\.ai/code/session_[A-Za-z0-9]*' | tail -1)
  if [[ -n "$PANE_URL" ]]; then
    URL="$PANE_URL"
    break
  fi
done

# Register session (UUID filled in by on_session_end.sh when session stops)
python3 "$SCRIPT_DIR/registry.py" add "$SESSION_LABEL" "${URL:-}" "$WORKDIR" ""

# Session is now registered — disarm the cleanup trap
trap - INT TERM

IDLE_MINS=$((IDLE_TIMEOUT / 60))

echo ""
echo "✅ $SESSION_LABEL"
echo "   URL:        ${URL:-<not captured yet>}"
echo "   local UUID: <capturing in background>"
echo "   resume:     claude -r \"<uuid>\" --dangerously-skip-permissions --remote-control"
echo "   tmux:       tmux attach -t $TMUX_NAME"
echo "   State:      $HOME/.local/share/claude-rc/sessions.json"
echo "   Auto-closes after ${IDLE_MINS}m idle."
