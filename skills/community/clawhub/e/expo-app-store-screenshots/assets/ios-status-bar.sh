#!/usr/bin/env bash
# Lock the iOS Simulator status bar to a clean marketing state (9:41 / charged / full bars).
#
# Usage:
#   bash ios-status-bar.sh [UDID|booted]   # default: booted
#
# Use `bash ios-status-bar.sh clear [UDID|booted]` to revert.

set -euo pipefail

if [[ "${1:-}" == "clear" ]]; then
  target="${2:-booted}"
  xcrun simctl status_bar "$target" clear
  exit 0
fi

target="${1:-booted}"

xcrun simctl status_bar "$target" override \
  --time "9:41" \
  --batteryState charged \
  --batteryLevel 100 \
  --wifiBars 3 \
  --cellularBars 4 \
  --dataNetwork wifi
