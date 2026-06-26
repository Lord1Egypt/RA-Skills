#!/usr/bin/env bash
# Shared environment setup for all clawgrid-connector scripts.
# Sources: CLAWGRID_HOME (~/.clawgrid), auto-migrates from legacy skill dir.
#
# Usage (at the top of every script, AFTER set -euo pipefail):
#   SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
#   source "$SKILL_DIR/scripts/_clawgrid_env.sh"
#
# After sourcing, these variables are available:
#   CLAWGRID_HOME, CONFIG, STATE_FILE, LOG_DIR, PENDING_DIR,
#   AUTH_INVALID_FLAG, FAIL_COUNT_FILE, COOLDOWN_FILE, LAST_POLL_FILE,
#   LAST_HOLD_FILE, NO_TASK_COUNT_FILE, CIRCUIT_BREAKER_NOTIFIED_FLAG

CLAWGRID_HOME="${CLAWGRID_HOME:-$HOME/.clawgrid}"

CONFIG="$CLAWGRID_HOME/config.json"
STATE_FILE="$CLAWGRID_HOME/state/runtime.json"
LOG_DIR="$CLAWGRID_HOME/logs"
PENDING_DIR="$CLAWGRID_HOME/pending_artifacts"

AUTH_INVALID_FLAG="$CLAWGRID_HOME/state/.auth_invalid"
FAIL_COUNT_FILE="$CLAWGRID_HOME/state/.fail_count"
COOLDOWN_FILE="$CLAWGRID_HOME/state/.cooldown_until"
LAST_POLL_FILE="$CLAWGRID_HOME/state/.last_poll_epoch"
LAST_HOLD_FILE="$CLAWGRID_HOME/state/.last_hold_reason"
NO_TASK_COUNT_FILE="$CLAWGRID_HOME/state/.no_task_count"
CIRCUIT_BREAKER_NOTIFIED_FLAG="$CLAWGRID_HOME/state/.circuit_breaker_notified"

_clawgrid_ensure_dirs() {
  mkdir -p "$CLAWGRID_HOME"/{state,cache,logs,pending_artifacts}
}

_clawgrid_migrate() {
  # Already migrated — nothing to do
  [ -f "$CONFIG" ] && return 0

  local legacy="$SKILL_DIR/config.json"
  [ ! -f "$legacy" ] && return 1

  echo "[clawgrid] Migrating config to $CLAWGRID_HOME ..." >&2
  _clawgrid_ensure_dirs

  # 1. Copy config.json (identity + connection)
  cp "$legacy" "$CONFIG"

  # 2. Migrate state.json → state/runtime.json
  [ -f "$SKILL_DIR/state.json" ] && \
    cp "$SKILL_DIR/state.json" "$CLAWGRID_HOME/state/runtime.json"

  # 3. Migrate dotfile counters → state/ (keep as individual files for atomicity)
  for f in .fail_count .no_task_count .cooldown_until .auth_invalid \
           .circuit_breaker_notified .last_hold_reason; do
    [ -f "$SKILL_DIR/$f" ] && cp "$SKILL_DIR/$f" "$CLAWGRID_HOME/state/$f"
  done

  # 4. Migrate pending_artifacts
  if [ -d "$SKILL_DIR/pending_artifacts" ]; then
    cp -r "$SKILL_DIR/pending_artifacts/"* "$CLAWGRID_HOME/pending_artifacts/" 2>/dev/null || true
  fi

  # 5. Migrate logs
  if [ -d "$SKILL_DIR/logs" ]; then
    cp -r "$SKILL_DIR/logs/"* "$CLAWGRID_HOME/logs/" 2>/dev/null || true
  fi

  # 6. Leave a marker at the old location
  echo "$CLAWGRID_HOME" > "$SKILL_DIR/.migrated_to"

  echo "[clawgrid] Migration complete → $CLAWGRID_HOME" >&2
}

# Run migration on source, then ensure dirs exist
_clawgrid_migrate || true
_clawgrid_ensure_dirs
