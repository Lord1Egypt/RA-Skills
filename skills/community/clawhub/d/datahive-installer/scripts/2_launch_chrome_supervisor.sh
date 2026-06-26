#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM="${PLATFORM:-$($SCRIPT_DIR/0_detect_platform.sh)}"

PROFILE_DIR="${PROFILE_DIR:-$HOME/.chrome-datahive}"
LOG_FILE="${LOG_FILE:-$PROFILE_DIR/chrome.log}"
PID_FILE="${PID_FILE:-$PROFILE_DIR/chrome.pid}"
CHROME_HEADLESS="${CHROME_HEADLESS:-1}"
CHROME_NO_SANDBOX="${CHROME_NO_SANDBOX:-0}"
LOG_MAX_BYTES="${LOG_MAX_BYTES:-10485760}" # 10MB

HEADLESS_FLAG=""
if [[ "$CHROME_HEADLESS" == "1" ]]; then
  HEADLESS_FLAG="--headless=new"
fi

NO_SANDBOX_FLAG=""
if [[ "$CHROME_NO_SANDBOX" == "1" ]]; then
  NO_SANDBOX_FLAG="--no-sandbox"
fi

mkdir -p "$PROFILE_DIR"

rotate_log_if_needed() {
  if [[ -f "$LOG_FILE" ]]; then
    local size
    size=$(wc -c < "$LOG_FILE" | tr -d '[:space:]')
    if [[ "$size" -ge "$LOG_MAX_BYTES" ]]; then
      [[ -f "$LOG_FILE.2" ]] && mv -f "$LOG_FILE.2" "$LOG_FILE.3"
      [[ -f "$LOG_FILE.1" ]] && mv -f "$LOG_FILE.1" "$LOG_FILE.2"
      mv -f "$LOG_FILE" "$LOG_FILE.1"
      : > "$LOG_FILE"
    fi
  fi
}

is_valid_supervisor_pid() {
  local pid="$1"
  [[ "$pid" =~ ^[0-9]+$ ]] || return 1
  kill -0 "$pid" 2>/dev/null || return 1

  local cmd child
  cmd=$(ps -p "$pid" -o command= 2>/dev/null || true)
  child=$(pgrep -P "$pid" -af 'Chrome|google-chrome' 2>/dev/null || true)

  # Valid if this is our while-loop supervisor, or if it currently owns a Chrome child
  # with the expected CDP port/profile.
  if echo "$cmd" | grep -q 'while true; do'; then
    return 0
  fi

  if [[ -n "$child" ]] \
    && echo "$child" | grep -q -- '--remote-debugging-port=9222' \
    && echo "$child" | grep -Fq -- "--user-data-dir=$PROFILE_DIR"; then
    return 0
  fi

  return 1
}

# Prevent duplicate launchers, with stale PID cleanup.
if [[ -f "$PID_FILE" ]]; then
  OLD_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
  if is_valid_supervisor_pid "$OLD_PID"; then
    echo "Chrome launcher already running (PID: $OLD_PID)"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

rotate_log_if_needed

if [[ "$PLATFORM" == "ubuntu" ]]; then
  CHROME_CMD="xvfb-run -a google-chrome --no-sandbox --disable-gpu --disable-dev-shm-usage --no-first-run --disable-default-apps $HEADLESS_FLAG --remote-debugging-port=9222 --user-data-dir=\"$PROFILE_DIR\" --profile-directory=datahive"
elif [[ "$PLATFORM" == "macos" ]]; then
  CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  if [[ ! -x "$CHROME_BIN" ]]; then
    echo "Error: Chrome binary not found at $CHROME_BIN" >&2
    exit 1
  fi

  CHROME_CMD="\"$CHROME_BIN\" --no-first-run --disable-default-apps --disable-gpu $NO_SANDBOX_FLAG $HEADLESS_FLAG --remote-debugging-port=9222 --user-data-dir=\"$PROFILE_DIR\" --profile-directory=datahive"
else
  echo "Unsupported platform: $PLATFORM. Supported platforms: ubuntu, macos" >&2
  exit 1
fi

SUPERVISOR_SCRIPT='set -u
while true; do
  eval "$CHROME_CMD"
  echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Chrome exited; restarting in 2s..." >&2
  sleep 2
done'

if command -v setsid >/dev/null 2>&1; then
  env CHROME_CMD="$CHROME_CMD" setsid bash -c "$SUPERVISOR_SCRIPT" >>"$LOG_FILE" 2>&1 < /dev/null &
  SUP_PID=$!
else
  # macOS often lacks `setsid`, and `nohup` may fail in non-interactive sessions
  # with: "can't detach from console: Inappropriate ioctl for device".
  # Run detached from stdin in background directly instead.
  env CHROME_CMD="$CHROME_CMD" bash -c "$SUPERVISOR_SCRIPT" >>"$LOG_FILE" 2>&1 < /dev/null &
  SUP_PID=$!
  disown "$SUP_PID" 2>/dev/null || true
fi

echo "$SUP_PID" > "$PID_FILE"
echo "Chrome supervisor running in background (PID: $SUP_PID, platform: $PLATFORM, headless: $CHROME_HEADLESS)"