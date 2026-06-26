#!/usr/bin/env bash
set -euo pipefail

# --- Configuration (override via environment) ---
PROFILE_DIR="${CHROMIUM_PROFILE_DIR:-${HOME}/.openclaw/workspace/chromium-profile}"
DEBUG_PORT="${CHROMIUM_DEBUG_PORT:-18801}"
LOG_FILE="${CHROMIUM_LOG_FILE:-${HOME}/.openclaw/workspace/logs/chromium.log}"

# Auto-detect browser binary
if [ -n "${CHROMIUM_BIN:-}" ]; then
  BROWSER="$CHROMIUM_BIN"
elif command -v chromium >/dev/null 2>&1; then
  BROWSER="chromium"
elif command -v chromium-browser >/dev/null 2>&1; then
  BROWSER="chromium-browser"
elif command -v google-chrome >/dev/null 2>&1; then
  BROWSER="google-chrome"
else
  echo "ERROR: No Chromium/Chrome binary found. Set CHROMIUM_BIN." >&2
  exit 1
fi

mkdir -p "$PROFILE_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# Stop previous Chromium launched with same profile
pkill -f "${BROWSER}.*--user-data-dir=.*${PROFILE_DIR##*/}" >/dev/null 2>&1 || true
sleep 0.5

# Remove stale SingletonLock if Chromium is not running
if ! pgrep -f "${BROWSER}.*--user-data-dir=.*${PROFILE_DIR##*/}" >/dev/null 2>&1; then
  rm -f "$PROFILE_DIR/SingletonLock"
fi

nohup "$BROWSER" \
  --remote-debugging-port="$DEBUG_PORT" \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  --no-default-browser-check \
  --disable-sync \
  --disable-background-networking \
  --disable-component-update \
  --disable-features=Translate,MediaRouter \
  --disable-session-crashed-bubble \
  --hide-crash-restore-bubble \
  --password-store=basic \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --disable-setuid-sandbox \
  --disable-dev-shm-usage \
  --disable-blink-features=AutomationControlled \
  --noerrdialogs \
  --ozone-platform=headless \
  --ozone-override-screen-size=800,600 \
  --use-angle=swiftshader-webgl \
  about:blank \
  >"$LOG_FILE" 2>&1 &

echo "Chromium started ($BROWSER)"
echo "Profile: $PROFILE_DIR"
echo "Debug URL: http://127.0.0.1:${DEBUG_PORT}/json/version"
