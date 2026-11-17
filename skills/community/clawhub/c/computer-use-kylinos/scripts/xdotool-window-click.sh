#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: xdotool-window-click.sh <window_id> <relative_x> <relative_y> [button]

Click a point relative to a window's coordinate system (X11 / KylinOS V10SP1).
- Reads window geometry from xdotool getwindowgeometry.
- X11 has no fractional scaling: screen coords = window origin + relative offset.
- Moves mouse, verifies with getmouselocation, then clicks.

Example:
  xdotool-window-click.sh 46137345 376 593 1
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
rx=$2
ry=$3
button=${4:-1}

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 127; }; }
need xdotool
need awk
need sed

geom_out=$(xdotool getwindowgeometry --shell "$wid" 2>&1)
echo "\$ geom: xdotool getwindowgeometry $wid"
echo "$geom_out"

wx=$(printf '%s\n' "$geom_out" | sed -n 's/^X=\([0-9-]*\)$/\1/p')
wy=$(printf '%s\n' "$geom_out" | sed -n 's/^Y=\([0-9-]*\)$/\1/p')
if [[ -z $wx || -z $wy ]]; then
  echo "failed to parse window geometry" >&2
  exit 1
fi

move_x=$(awk -v a="$wx" -v b="$rx" 'BEGIN{printf "%d", a+b}')
move_y=$(awk -v a="$wy" -v b="$ry" 'BEGIN{printf "%d", a+b}')

echo "# window=($wx,$wy), relative=($rx,$ry), screen=($move_x,$move_y)"
echo "\$ xdotool mousemove ${move_x} ${move_y}"
xdotool mousemove "$move_x" "$move_y" 2>&1

echo "\$ xdotool getmouselocation"
xdotool getmouselocation 2>&1

echo "\$ xdotool click $button"
xdotool click "$button" 2>&1
