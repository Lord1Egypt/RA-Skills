#!/usr/bin/env bash
# Start a virtual *headed* X display so a real (non-headless) browser can run on a box
# with no usable physical display. Uses TigerVNC's Xvnc.
#
#   ./start-display.sh [DISPLAY_NUM]      e.g. ./start-display.sh :1
#
# After this:  DISPLAY=:1 HEADED=1 node login-interactive.mjs
set -euo pipefail

DISP="${1:-:1}"
LOG="$HOME/.vnc/display-launch.log"
mkdir -p "$HOME/.vnc"

# No-auth VNC (localhost only) so we don't need a viewer/password; we only need the X display.
if vncserver -list 2>/dev/null | grep -qF "${DISP}"; then
  echo "display ${DISP} already running"
else
  printf 'espn2fa\n' | vncpasswd -f > "$HOME/.vnc/passwd" 2>/dev/null || true
  chmod 600 "$HOME/.vnc/passwd" 2>/dev/null || true
  vncserver "${DISP}" -geometry 1366x900 -depth 24 -SecurityTypes None -localhost yes >>"$LOG" 2>&1
  sleep 3
fi

# Verify
if DISPLAY="${DISP}" XAUTHORITY="$HOME/.Xauthority" xdpyinfo >/dev/null 2>&1; then
  echo "display ${DISP} ready (export DISPLAY=${DISP} XAUTHORITY=$HOME/.Xauthority)"
else
  echo "ERROR: display ${DISP} not reachable — check ${LOG}" >&2
  exit 1
fi
