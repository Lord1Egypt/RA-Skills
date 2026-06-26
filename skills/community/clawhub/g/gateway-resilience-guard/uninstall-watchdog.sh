#!/usr/bin/env bash
# Uninstall OpenClaw Gateway Resilience Guard for the current user.

set -euo pipefail

SERVICE_NAME="gateway-watchdog"
PLIST_LABEL="ai.clawhub.gateway-resilience-guard"
INSTALL_DIR="${INSTALL_DIR:-${HOME}/.local/share/openclaw-gateway-watchdog}"
CONFIG_DIR="${XDG_CONFIG_HOME:-${HOME}/.config}/openclaw-gateway-watchdog"
STATE_DIR="${XDG_STATE_HOME:-${HOME}/.local/state}/openclaw-gateway-watchdog"
SERVICE_FILE="${HOME}/.config/systemd/user/${SERVICE_NAME}.service"
PLIST_FILE="${HOME}/Library/LaunchAgents/${PLIST_LABEL}.plist"
PURGE=0

if [ "${1:-}" = "--purge" ]; then
  PURGE=1
fi

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

if [ "$(uname -s 2>/dev/null || echo unknown)" = "Darwin" ] && have_cmd launchctl; then
  uid=$(id -u)
  launchctl bootout "gui/${uid}" "$PLIST_FILE" >/dev/null 2>&1 || true
fi

if have_cmd systemctl && systemctl --user status >/dev/null 2>&1; then
  systemctl --user stop "$SERVICE_NAME" 2>/dev/null || true
  systemctl --user disable "$SERVICE_NAME" 2>/dev/null || true
fi

if [ -f "${STATE_DIR}/watchdog.pid" ]; then
  pid="$(cat "${STATE_DIR}/watchdog.pid" 2>/dev/null || true)"
  if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
  fi
  rm -f "${STATE_DIR}/watchdog.pid"
fi

if [ -f "${STATE_DIR}/dashboard.pid" ]; then
  pid="$(cat "${STATE_DIR}/dashboard.pid" 2>/dev/null || true)"
  if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
  fi
  rm -f "${STATE_DIR}/dashboard.pid"
fi

rm -f "$SERVICE_FILE" "$PLIST_FILE"
if have_cmd systemctl && systemctl --user status >/dev/null 2>&1; then
  systemctl --user daemon-reload
fi

rm -rf "$INSTALL_DIR"

if [ "$PURGE" -eq 1 ]; then
  rm -rf "$CONFIG_DIR" "$STATE_DIR"
  echo "OpenClaw Gateway Resilience Guard removed, including config and logs."
else
  echo "OpenClaw Gateway Resilience Guard removed. Config/logs kept:"
  echo "  ${CONFIG_DIR}"
  echo "  ${STATE_DIR}"
  echo "Use --purge to remove them too."
fi
