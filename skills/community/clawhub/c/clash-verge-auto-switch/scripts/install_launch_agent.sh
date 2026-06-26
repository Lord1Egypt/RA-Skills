#!/bin/zsh
set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
  cat <<'EOF'
Usage:
  install_launch_agent.sh --interval-minutes N [arguments passed to switch_fastest.py]

Example:
  install_launch_agent.sh --interval-minutes 30 --group-scope current
EOF
  exit 0
fi

LABEL="com.codex.clash-verge-auto-switch"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOG_DIR="$HOME/Library/Logs"
OUT_LOG="$LOG_DIR/clash-verge-auto-switch.log"
ERR_LOG="$LOG_DIR/clash-verge-auto-switch.err.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3}"
INTERVAL_MINUTES=""
SCRIPT_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --interval-minutes)
      if [[ $# -lt 2 ]]; then
        echo "Missing value for --interval-minutes" >&2
        exit 1
      fi
      INTERVAL_MINUTES="$2"
      shift 2
      ;;
    *)
      SCRIPT_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ -z "$INTERVAL_MINUTES" ]]; then
  echo "Please choose an interval with --interval-minutes N" >&2
  exit 1
fi

if ! [[ "$INTERVAL_MINUTES" =~ ^[0-9]+$ ]] || [[ "$INTERVAL_MINUTES" -le 0 ]]; then
  echo "--interval-minutes must be a positive integer" >&2
  exit 1
fi

INTERVAL_SECONDS=$((INTERVAL_MINUTES * 60))

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

"$PYTHON_BIN" - "$PLIST_PATH" "$OUT_LOG" "$ERR_LOG" "$INTERVAL_SECONDS" "$PYTHON_BIN" "$SCRIPT_DIR/switch_fastest.py" "${SCRIPT_ARGS[@]}" <<'PY'
import plistlib
import sys

plist_path, out_log, err_log, interval_seconds, *program_arguments = sys.argv[1:]
payload = {
    "Label": "com.codex.clash-verge-auto-switch",
    "ProgramArguments": program_arguments,
    "RunAtLoad": True,
    "StartInterval": int(interval_seconds),
    "StandardOutPath": out_log,
    "StandardErrorPath": err_log,
    "WorkingDirectory": "/tmp",
}

with open(plist_path, "wb") as handle:
    plistlib.dump(payload, handle)
PY

launchctl bootout "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
launchctl enable "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
launchctl kickstart -k "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true

echo "Installed $LABEL"
echo "Interval: ${INTERVAL_MINUTES} minute(s)"
echo "Plist: $PLIST_PATH"
echo "Stdout: $OUT_LOG"
echo "Stderr: $ERR_LOG"
