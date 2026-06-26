#!/usr/bin/env bash
# Toggle Android system UI demo mode for clean marketing screenshots
# (clock 9:41, full battery, full signal, no notifications).
#
# Usage:
#   bash android-status-bar.sh enter [-s SERIAL]
#   bash android-status-bar.sh exit  [-s SERIAL]
#
# Forwards `-s SERIAL` to adb to pin a specific device when multiple are attached.

set -euo pipefail

mode="${1:-}"
shift || true

case "$mode" in
  enter|exit) ;;
  *)
    echo "usage: $0 <enter|exit> [-s SERIAL]" >&2
    exit 1
    ;;
esac

if [[ "$mode" == "enter" ]]; then
  adb "$@" shell settings put global sysui_demo_allowed 1
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command enter
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0941
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command battery -e level 100 -e plugged false
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command network -e wifi show -e level 4
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command network -e mobile show -e datatype lte -e level 4
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command notifications -e visible false
else
  adb "$@" shell am broadcast -a com.android.systemui.demo -e command exit
fi
