#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: xdotool-drag.sh <window_id> <start_x> <start_y> <end_x> <end_y> [button]

Drag from one point to another, both RELATIVE to the window's top-left corner
(X11 / KylinOS V10SP1).
- Reads window geometry from xdotool getwindowgeometry.
- X11 has no fractional scaling: screen coords = window origin + relative offset.
- Performs: move to start, mousedown, move to end, mouseup.

Example (drag a slider/scrollbar inside a window):
  xdotool-drag.sh 46137345 100 200 100 60 1
EOF
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi
if [[ $# -lt 5 ]]; then
  usage
  exit 2
fi

wid=$1
sx=$2
sy=$3
ex=$4
ey=$5
button=${6:-1}

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

# Start point (screen coordinates, no scale in X11)
start_x=$(awk -v a="$wx" -v b="$sx" 'BEGIN{printf "%d", a+b}')
start_y=$(awk -v a="$wy" -v b="$sy" 'BEGIN{printf "%d", a+b}')

# End point
end_x=$(awk -v a="$wx" -v b="$ex" 'BEGIN{printf "%d", a+b}')
end_y=$(awk -v a="$wy" -v b="$ey" 'BEGIN{printf "%d", a+b}')

echo "# window=($wx,$wy)"
echo "# start: relative=($sx,$sy) screen=($start_x,$start_y)"
echo "# end:   relative=($ex,$ey) screen=($end_x,$end_y)"

echo "\$ xdotool mousemove ${start_x} ${start_y}"
xdotool mousemove "$start_x" "$start_y" 2>&1
echo "\$ xdotool mousedown $button"
xdotool mousedown "$button" 2>&1
echo "\$ xdotool mousemove ${end_x} ${end_y}"
xdotool mousemove "$end_x" "$end_y" 2>&1
echo "\$ xdotool mouseup $button"
xdotool mouseup "$button" 2>&1

echo "\$ xdotool getmouselocation"
xdotool getmouselocation 2>&1
