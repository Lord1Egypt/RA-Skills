#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: xdotool-window-dblclick.sh <window_id> <relative_x> <relative_y> [button] [delay_ms]

Double-click a point relative to a window's coordinate system (X11 / KylinOS V10SP1).
Queries geometry ONCE, moves mouse ONCE, then uses xdotool's native --repeat to
fire two clicks within the double-click threshold in a SINGLE process invocation.

Arguments:
  window_id     Target window ID (decimal)
  relative_x    X coordinate relative to window screenshot
  relative_y    Y coordinate relative to window screenshot
  button        Mouse button (default: 1)
  delay_ms      Delay between the two clicks in ms (default: 80)

Example:
  xdotool-window-dblclick.sh 46137345 376 593 1 80
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
delay_ms=${5:-80}

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing command: $1" >&2; exit 127; }; }
need xdotool
need awk
need sed

# --- Query geometry ONCE ---
geom_out=$(xdotool getwindowgeometry --shell "$wid" 2>&1)
wx=$(printf '%s\n' "$geom_out" | sed -n 's/^X=\([0-9-]*\)$/\1/p')
wy=$(printf '%s\n' "$geom_out" | sed -n 's/^Y=\([0-9-]*\)$/\1/p')
if [[ -z $wx || -z $wy ]]; then
  echo "failed to parse window geometry" >&2
  echo "$geom_out" >&2
  exit 1
fi

# --- Compute screen coordinates (no scale on X11) ---
move_x=$(awk -v a="$wx" -v b="$rx" 'BEGIN{printf "%d", a+b}')
move_y=$(awk -v a="$wy" -v b="$ry" 'BEGIN{printf "%d", a+b}')

echo "# window=($wx,$wy), relative=($rx,$ry), screen=($move_x,$move_y)"

# --- Move ONCE ---
xdotool mousemove "$move_x" "$move_y" 2>&1

# --- Native double-click: single xdotool process, --repeat 2 with delay ---
echo "# double-click: button=$button, delay=${delay_ms}ms, repeat=2"
xdotool click --repeat 2 --delay "$delay_ms" "$button" 2>&1

echo "# double-click done"
