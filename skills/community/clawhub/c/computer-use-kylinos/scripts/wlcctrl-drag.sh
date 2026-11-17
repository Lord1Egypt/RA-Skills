#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: wlcctrl-drag.sh <window_uuid> <start_x> <start_y> <end_x> <end_y> [button]

Drag from one point to another, both RELATIVE to the window's top-left corner.
- Reads window geometry from wlcctrl --getwindowgeometry.
- Reads output scale from wlcctrl --getdisplaygeometry of the first output.
- Converts logical screen coordinates to scaled wlcctrl --mousemove input
  (mousemove needs logical x scale -- see SKILL.md "Coordinate formula").
- Performs: move to start, press, move to end, release.
- Verifies final location with wlcctrl --getmouselocation.

Example (drag a slider/scrollbar inside a window):
  wlcctrl-drag.sh <uuid> 100 200 100 60 1
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

uuid=$1
sx=$2
sy=$3
ex=$4
ey=$5
button=${6:-1}

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 127; }; }
need wlcctrl
need awk
need sed

geom_out=$(wlcctrl --getwindowgeometry "$uuid" 2>&1)
echo "$ geom: wlcctrl --getwindowgeometry $uuid"
echo "$geom_out"

geom=$(printf '%s\n' "$geom_out" | sed -n 's/.*geometry: (\([0-9]\+\), *\([0-9]\+\)) *\([0-9]\+\) x *\([0-9]\+\).*/\1 \2 \3 \4/p' | tail -1)
if [[ -z $geom ]]; then
  echo "failed to parse window geometry" >&2
  exit 1
fi
read -r wx wy ww wh <<<"$geom"

outputs_out=$(wlcctrl --outputs 2>&1)
output_uuid=$(printf '%s\n' "$outputs_out" | sed -n 's/^output "\([^"]*\)"/\1/p' | head -1)
if [[ -z $output_uuid ]]; then
  echo "failed to find output uuid" >&2
  echo "$outputs_out" >&2
  exit 1
fi

disp_out=$(wlcctrl --getdisplaygeometry "$output_uuid" 2>&1)
echo "$ display: wlcctrl --getdisplaygeometry $output_uuid"
echo "$disp_out"
scale=$(printf '%s\n' "$disp_out" | sed -n 's/.*scale: *\([0-9.]*\).*/\1/p' | tail -1)
if [[ -z $scale ]]; then
  echo "failed to parse output scale" >&2
  exit 1
fi

# Start point
start_logical_x=$(awk -v a="$wx" -v b="$sx" 'BEGIN{printf "%d", a+b}')
start_logical_y=$(awk -v a="$wy" -v b="$sy" 'BEGIN{printf "%d", a+b}')
start_move_x=$(awk -v v="$start_logical_x" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')
start_move_y=$(awk -v v="$start_logical_y" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')

# End point
end_logical_x=$(awk -v a="$wx" -v b="$ex" 'BEGIN{printf "%d", a+b}')
end_logical_y=$(awk -v a="$wy" -v b="$ey" 'BEGIN{printf "%d", a+b}')
end_move_x=$(awk -v v="$end_logical_x" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')
end_move_y=$(awk -v v="$end_logical_y" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')

echo "# window=($wx,$wy) ${ww}x${wh}, scale=$scale"
echo "# start: relative=($sx,$sy) logical=($start_logical_x,$start_logical_y) mousemove=($start_move_x,$start_move_y)"
echo "# end:   relative=($ex,$ey) logical=($end_logical_x,$end_logical_y) mousemove=($end_move_x,$end_move_y)"

echo "$ wlcctrl --mousemove ${start_move_x},${start_move_y}"
wlcctrl --mousemove "${start_move_x},${start_move_y}" 2>&1
echo "$ wlcctrl --mousepress $button"
wlcctrl --mousepress "$button" 2>&1
echo "$ wlcctrl --mousemove ${end_move_x},${end_move_y}"
wlcctrl --mousemove "${end_move_x},${end_move_y}" 2>&1
echo "$ wlcctrl --mouserelease $button"
wlcctrl --mouserelease "$button" 2>&1

echo "$ wlcctrl --getmouselocation"
wlcctrl --getmouselocation 2>&1
