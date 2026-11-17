#!/usr/bin/env bash
set -u

have() { command -v "$1" >/dev/null 2>&1; }

echo '== os =='
bash "$(dirname "$0")/detect-os.sh" 2>/dev/null || echo 'detect failed'

echo
echo '== xdotool =='
if ! have xdotool; then
  echo 'xdotool: not found — install with: sudo apt install xdotool' >&2
  exit 1
fi
command -v xdotool
xdotool version 2>&1 || true

echo
echo '== display =='
xdpyinfo 2>/dev/null | grep -Ei 'dimensions|resolution' || true

echo
echo '== screenshot tool =='
if have import; then
  echo "import (ImageMagick) available"
elif have maim; then
  echo "maim available"
elif have scrot; then
  echo "scrot available"
else
  echo 'no screenshot tool found — install: sudo apt install imagemagick' >&2
fi

echo
echo '== active window =='
xdotool getactivewindow 2>&1 || true
aw=$(xdotool getactivewindow 2>/dev/null) && xdotool getwindowgeometry "$aw" 2>&1 || true

echo
echo '== mouse location =='
xdotool getmouselocation 2>&1 || true

echo
echo '== visible windows (sample) =='
xdotool search --onlyvisible --name '' 2>/dev/null | head -20 | while read -r wid; do
  name=$(xdotool getwindowname "$wid" 2>/dev/null || echo '?')
  printf '%s\t%s\n' "$wid" "$name"
done
