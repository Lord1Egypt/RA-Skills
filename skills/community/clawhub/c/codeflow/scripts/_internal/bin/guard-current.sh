#!/bin/bash

set -euo pipefail
umask 077

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$BIN_DIR/../.." && pwd)"
PY_DIR="$(cd "$BIN_DIR/../py" && pwd)"
source "$BIN_DIR/lib.sh"
codeflow_init_default_paths "$ROOT_DIR"
CODEFLOW_SCRIPT_DIR="$PY_DIR"
codeflow_require_python310

STATE_FILE="${CODEFLOW_GUARD_FILE:-$CODEFLOW_GUARD_FILE_DEFAULT}"
AUDIT_FILE="${CODEFLOW_AUDIT_FILE:-$CODEFLOW_AUDIT_FILE_DEFAULT}"
PLATFORM="auto"
SESSION_KEY="${OPENCLAW_SESSION_KEY:-${OPENCLAW_SESSION:-}}"
CHAT_ID=""
THREAD_ID=""

infer_platform_from_session_key() {
  local session_key="${1:-}"
  codeflow_platform_from_session_key "$session_key"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    -P|--platform)
      [ "$#" -lt 2 ] && { echo "Error: $1 requires a value" >&2; exit 2; }
      PLATFORM="$2"
      shift 2
      ;;
    --session-key)
      [ "$#" -lt 2 ] && { echo "Error: $1 requires a value" >&2; exit 2; }
      SESSION_KEY="$2"
      shift 2
      ;;
    --chat-id)
      [ "$#" -lt 2 ] && { echo "Error: $1 requires a value" >&2; exit 2; }
      CHAT_ID="$2"
      shift 2
      ;;
    --thread-id)
      [ "$#" -lt 2 ] && { echo "Error: $1 requires a value" >&2; exit 2; }
      THREAD_ID="$2"
      shift 2
      ;;
    --state)
      [ "$#" -lt 2 ] && { echo "Error: $1 requires a value" >&2; exit 2; }
      STATE_FILE="$2"
      shift 2
      ;;
    --audit)
      [ "$#" -lt 2 ] && { echo "Error: $1 requires a value" >&2; exit 2; }
      AUDIT_FILE="$2"
      shift 2
      ;;
    -h|--help|help)
      cat <<'EOF'
Usage:
  guard-current.sh [-P <platform|auto>] [--session-key <key>] [--chat-id <id>] [--thread-id <id>]

Outputs the resolved Codeflow guard binding for the current context as JSON.
EOF
      exit 0
      ;;
    *)
      echo "Error: unknown argument '$1'" >&2
      exit 2
      ;;
  esac
done

if [ -n "$SESSION_KEY" ]; then
  export OPENCLAW_SESSION_KEY="$SESSION_KEY"
  export OPENCLAW_SESSION="$SESSION_KEY"
fi

codeflow_resolve_openclaw_session_context
[ -z "$CHAT_ID" ] && CHAT_ID="${TELEGRAM_CHAT_ID:-}"
[ -z "$THREAD_ID" ] && THREAD_ID="${TELEGRAM_THREAD_ID:-}"

if [ -z "$PLATFORM" ] || [ "$PLATFORM" = "auto" ]; then
  PLATFORM="$(infer_platform_from_session_key "$SESSION_KEY")"
fi

python3 "$PY_DIR/codeflow-guard.py" current \
  --state "$STATE_FILE" \
  --audit "$AUDIT_FILE" \
  --session-key "$SESSION_KEY" \
  --platform "${PLATFORM:-}" \
  --chat-id "${CHAT_ID:-}" \
  --thread-id "${THREAD_ID:-}" \
  --workdir "" \
  --agent "" \
  --command ""
