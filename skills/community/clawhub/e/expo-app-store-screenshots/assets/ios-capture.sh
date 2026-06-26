#!/usr/bin/env bash
# Deep-link into a screen on an iOS Simulator and screenshot it.
#
# Usage:
#   bash ios-capture.sh <UDID> <URL> <OUTPUT_PATH> [SETTLE_SECONDS]
#
# Examples:
#   bash ios-capture.sh booted "myapp:///settings" out/06-iphone-settings.png
#   bash ios-capture.sh 427DD273-... "myapp:///agent" out/04-iphone-agent.png 3

set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: $0 <UDID|booted> <URL> <OUTPUT_PATH> [SETTLE_SECONDS]" >&2
  exit 1
fi

udid="$1"
url="$2"
output="$3"
settle="${4:-2}"

mkdir -p "$(dirname "$output")"
output_abs="$(cd "$(dirname "$output")" && pwd)/$(basename "$output")"
tmp="$(mktemp -t app-store-screenshot).png"

xcrun simctl openurl "$udid" "$url"
sleep "$settle"
xcrun simctl io "$udid" screenshot "$tmp"
mv -f "$tmp" "$output_abs"
