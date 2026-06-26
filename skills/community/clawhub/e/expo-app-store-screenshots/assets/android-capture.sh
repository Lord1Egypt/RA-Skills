#!/usr/bin/env bash
# Deep-link into a screen on an Android device/emulator and screenshot it.
#
# Usage:
#   bash android-capture.sh <URL> <OUTPUT_PATH> [PACKAGE] [SETTLE_SECONDS] [-s SERIAL]
#
# PACKAGE is optional; passing it makes the deep-link target unambiguous when
# multiple apps register the same scheme. Pass `-` to skip.
#
# Uses `screencap -p` + `adb pull`, NOT `adb exec-out screencap -p > file` —
# the latter mangles bytes on some shells.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <URL> <OUTPUT_PATH> [PACKAGE|-] [SETTLE_SECONDS] [-s SERIAL]" >&2
  exit 1
fi

url="$1"; shift
output="$1"; shift
pkg="${1:-}"; [[ $# -gt 0 ]] && shift || true
settle="${1:-2}"; [[ $# -gt 0 ]] && shift || true
# remaining args (typically `-s SERIAL`) forwarded to adb

mkdir -p "$(dirname "$output")"

remote_path="/sdcard/.app-store-screenshot.png"

if [[ -n "$pkg" && "$pkg" != "-" ]]; then
  adb "$@" shell am start -W -a android.intent.action.VIEW -d "$url" "$pkg" >/dev/null
else
  adb "$@" shell am start -W -a android.intent.action.VIEW -d "$url" >/dev/null
fi

sleep "$settle"
adb "$@" shell screencap -p "$remote_path"
adb "$@" pull "$remote_path" "$output" >/dev/null
adb "$@" shell rm "$remote_path"
