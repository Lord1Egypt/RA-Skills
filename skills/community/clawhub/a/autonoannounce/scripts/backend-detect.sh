#!/usr/bin/env bash
set -euo pipefail

os=$(uname -s 2>/dev/null || echo unknown)

check_bin() { command -v "$1" >/dev/null 2>&1; }

if [[ "$os" == "Linux" ]]; then
  for b in mpv ffplay paplay; do
    if check_bin "$b"; then echo "$b"; exit 0; fi
  done
elif [[ "$os" == "Darwin" ]]; then
  for b in afplay mpv ffplay; do
    if check_bin "$b"; then echo "$b"; exit 0; fi
  done
elif [[ "$os" =~ MINGW|MSYS|CYGWIN|Windows_NT ]]; then
  for b in mpv ffplay; do
    if check_bin "$b"; then echo "$b"; exit 0; fi
  done
  echo "powershell-soundplayer"; exit 0
fi

echo "none"
exit 1
