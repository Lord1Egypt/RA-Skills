#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: xdotool-move-window.sh <window_id> <x> <y>

Move an X11 window to screen coordinates and verify geometry.
X11 uses screen pixel coordinates directly; no output scale conversion.
EOF
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -lt 3 ]]; then
  usage
  exit 2
fi

wid=$1
x=$2
y=$3

echo "\$ xdotool getwindowgeometry $wid"
xdotool getwindowgeometry "$wid" 2>&1 || true

echo "\$ xdotool windowmove $wid $x $y"
xdotool windowmove "$wid" "$x" "$y" 2>&1
sleep 0.3

echo "\$ xdotool getwindowgeometry $wid"
xdotool getwindowgeometry "$wid" 2>&1
