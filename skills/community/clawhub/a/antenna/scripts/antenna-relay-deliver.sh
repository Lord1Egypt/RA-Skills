#!/usr/bin/env bash
# antenna-relay-deliver.sh — Single-call relay for Antenna inbound (stdin path).
# Agent pipes the raw envelope directly here; wrapper handles the rest.
#
# Usage:
#   cat <raw_envelope> | bash antenna-relay-deliver.sh
#   bash antenna-relay-deliver.sh /path/to/envelope-file   # backward compat
#
# No shell metacharacters in the exec path. Single allowed exec shape:
#   bash <script> <arg>
# No heredocs, here-strings, command substitution, or chaining.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# ── Determine input ─────────────────────────────────────────────────────────

if [[ $# -ge 1 && -f "${1:-}" ]]; then
  INPUT_MODE="file"
  INPUT_PATH="$1"
else
  INPUT_MODE="stdin"
fi

# ── Logging ────────────────────────────────────────────────────────────────

# Source config helpers (CONFIG_FILE must be set before sourcing)
CONFIG_FILE="$SKILL_DIR/antenna-config.json"
# shellcheck source=../lib/config.sh
source "$SKILL_DIR/lib/config.sh"

_antenna_deliver_warned=0

log_msg() {
  local level="${1:-INFO}"
  local msg="${2:-}"

  local log_enabled; log_enabled=$(config_log_enabled)
  [[ "$log_enabled" != "true" ]] && return 0

  local log_path; log_path=$(config_log_path)
  if [[ "$log_path" != /* ]]; then
    log_path="$SKILL_DIR/$log_path"
  fi

  local ts; ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "[$ts] DELIVER | $level | $msg" >> "$log_path"
}

# ── Read stdin to temp file (stdin path only) ─────────────────────────────

TMPDIR="${TMPDIR:-/tmp}"
ANTENNA_TMPDIR="$TMPDIR/antenna-relay"
mkdir -p "$ANTENNA_TMPDIR"
chmod 0700 "$ANTENNA_TMPDIR" 2>/dev/null || true

TMPFILE=""
cleanup() {
  if [[ -n "$TMPFILE" && -f "$TMPFILE" ]]; then
    # shred if available, else truncate + unlink
    if command -v shred >/dev/null 2>&1; then
      shred -u "$TMPFILE" 2>/dev/null || true
    else
      : > "$TMPFILE" 2>/dev/null || true
      rm -f "$TMPFILE" 2>/dev/null || true
    fi
  fi
}
trap cleanup EXIT

if [[ "$INPUT_MODE" == "stdin" ]]; then
  TMPFILE=$(mktemp "$ANTENNA_TMPDIR/msg.XXXXXX")
  chmod 0600 "$TMPFILE"
  cat > "$TMPFILE"
else
  TMPFILE="$INPUT_PATH"
fi

# ── Relay via existing scripts ─────────────────────────────────────────────

RELAY_FILE_SCRIPT="$SCRIPT_DIR/antenna-relay-file.sh"
RELAY_SCRIPT="$SCRIPT_DIR/antenna-relay.sh"

# Verify expected relay scripts exist
if [[ ! -x "$RELAY_FILE_SCRIPT" ]]; then
  echo "Error: relay file script not found: $RELAY_FILE_SCRIPT"
  log_msg "ERROR" "relay file script missing"
  exit 1
fi
if [[ ! -x "$RELAY_SCRIPT" ]]; then
  echo "Error: relay script not found: $RELAY_SCRIPT"
  log_msg "ERROR" "relay script missing"
  exit 1
fi

# Run relay: antenna-relay-file.sh reads the file and calls antenna-relay.sh
RELAY_JSON=$(bash "$RELAY_FILE_SCRIPT" "$TMPFILE")

RELAY_STATUS=$(printf '%s' "$RELAY_JSON" | jq -r '.status // empty')
RELAY_ACTION=$(printf '%s' "$RELAY_JSON" | jq -r '.action // empty')

if [[ "$RELAY_STATUS" != "ok" || "$RELAY_ACTION" != "relay" ]]; then
  # Not a successful relay — relay script already logged and the JSON
  # describes the rejection. Mirror that output for the agent.
  printf '%s\n' "$RELAY_JSON"
  exit 0
fi

# Successful relay — extract and call gateway RPC
SESSION_KEY=$(printf '%s' "$RELAY_JSON" | jq -r '.sessionKey')
MESSAGE=$(printf '%s' "$RELAY_JSON" | jq -r '.message')

if [[ -z "$SESSION_KEY" || -z "$MESSAGE" ]]; then
  echo "Error: missing sessionKey or message from relay"
  log_msg "ERROR" "relay returned incomplete data"
  exit 1
fi

# Escape message for JSON (handle newlines, quotes, backslashes)
ESCAPED_MESSAGE=$(python3 - "$SESSION_KEY" "$MESSAGE" << 'PY'
import json, sys
key, msg = sys.argv[1], sys.argv[2]
print(json.dumps({"key": key, "message": msg}))
PY
)

RPC_PARAMS=$(python3 - "$SESSION_KEY" "$MESSAGE" << 'PY'
import json, sys
key, msg = sys.argv[1], sys.argv[2]
print(json.dumps({"key": key, "message": msg}))
PY
)

log_msg "INFO" "relay ok, calling sessions.send session=$SESSION_KEY chars=${#MESSAGE}"

# Call gateway RPC — timeout 60s so the model run can complete.
# Tolerate nonzero exits (e.g. "session not found") so we can report a
# structured error to stdout instead of dying silently under set -e.
RPC_JSON=$(openclaw gateway call sessions.send \
  --params "$RPC_PARAMS" \
  --json \
  --timeout 60000 2>&1) || true

RPC_OK=$(printf '%s' "$RPC_JSON" | jq -r '.status // empty' 2>/dev/null || true)
RPC_RUNID=$(printf '%s' "$RPC_JSON" | jq -r '.runId // empty' 2>/dev/null || true)
RPC_ERR=$(printf '%s' "$RPC_JSON" | jq -r '.error // empty' 2>/dev/null || true)

if [[ "$RPC_OK" != "started" ]]; then
  # Fallback: if the response was not JSON (e.g. raw "Gateway call failed: ..."
  # error text from the CLI), use the whole captured output as the error message,
  # trimmed to one line for the relay agent's reply.
  if [[ -z "$RPC_ERR" ]]; then
    RPC_ERR=$(printf '%s' "$RPC_JSON" | tr '\n' ' ' | sed 's/  */ /g' | head -c 300)
  fi
  echo "Error: sessions.send failed — $RPC_ERR"
  log_msg "ERROR" "sessions.send failed: $RPC_ERR"
  exit 0
fi

log_msg "INFO" "sessions.send started runId=$RPC_RUNID"
echo "Relayed"
