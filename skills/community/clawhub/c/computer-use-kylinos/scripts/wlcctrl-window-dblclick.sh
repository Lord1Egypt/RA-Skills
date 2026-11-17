#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: wlcctrl-window-dblclick.sh <window_uuid> <relative_x> <relative_y> [button] [delay_ms]

Double-click a point relative to a wlcctrl window capture coordinate system.
Queries geometry/scale ONCE, moves mouse ONCE, then fires two clicks in rapid
succession to stay within the compositor's double-click threshold.

Arguments:
  window_uuid   Target window UUID
  relative_x    X coordinate relative to window screenshot
  relative_y    Y coordinate relative to window screenshot
  button        Mouse button (default: 1)
  delay_ms      Delay between the two clicks in ms (default: 80)

Example:
  wlcctrl-window-dblclick.sh <uuid> 376 593 1 80
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

uuid=$1
rx=$2
ry=$3
button=${4:-1}
delay_ms=${5:-80}

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 127; }; }
need wlcctrl
need awk
need sed

# --- Query geometry ONCE ---
geom_out=$(wlcctrl --getwindowgeometry "$uuid" 2>&1)
geom=$(printf '%s\n' "$geom_out" | sed -n 's/.*geometry: (\([0-9]\+\), *\([0-9]\+\)) *\([0-9]\+\) x *\([0-9]\+\).*/\1 \2 \3 \4/p' | tail -1)
if [[ -z $geom ]]; then
  echo "failed to parse window geometry" >&2
  echo "$geom_out" >&2
  exit 1
fi
read -r wx wy ww wh <<<"$geom"

# --- Query scale ONCE ---
outputs_out=$(wlcctrl --outputs 2>&1)
output_uuid=$(printf '%s\n' "$outputs_out" | sed -n 's/^output "\([^"]*\)"/\1/p' | head -1)
if [[ -z $output_uuid ]]; then
  echo "failed to find output uuid" >&2
  exit 1
fi
disp_out=$(wlcctrl --getdisplaygeometry "$output_uuid" 2>&1)
scale=$(printf '%s\n' "$disp_out" | sed -n 's/.*scale: *\([0-9.]*\).*/\1/p' | tail -1)
if [[ -z $scale ]]; then
  echo "failed to parse output scale" >&2
  exit 1
fi

# --- Compute coordinates ---
logical_x=$(awk -v a="$wx" -v b="$rx" 'BEGIN{printf "%d", a+b}')
logical_y=$(awk -v a="$wy" -v b="$ry" 'BEGIN{printf "%d", a+b}')
move_x=$(awk -v v="$logical_x" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')
move_y=$(awk -v v="$logical_y" -v s="$scale" 'BEGIN{printf "%d", v*s + 0.5}')

echo "# window=($wx,$wy) ${ww}x${wh}, relative=($rx,$ry), logical=($logical_x,$logical_y), scale=$scale, mousemove=($move_x,$move_y)"

# --- Move ONCE, no verification (trust the math) ---
wlcctrl --mousemove "${move_x},${move_y}" 2>&1

# --- Double-click: two presses with minimal delay, NO re-query between ---
echo "# double-click: button=$button, delay=${delay_ms}ms"
wlcctrl --mousepress "$button" --mouserelease "$button" 2>&1
sleep "$(awk -v ms="$delay_ms" 'BEGIN{printf "%.3f", ms/1000}')"
wlcctrl --mousepress "$button" --mouserelease "$button" 2>&1

echo "# double-click done"
