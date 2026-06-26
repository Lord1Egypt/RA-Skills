#!/usr/bin/env bash
# Write <DIR>/summary.md documenting the device + the screens captured into that
# folder. Auto-detects model, OS, and resolution from a sample PNG.
#
# Usage:
#   bash write-summary.sh ios     <UDID>           <DIR> <LOCALE> [SCREEN_ROW]...
#   bash write-summary.sh android [SERIAL|-]       <DIR> <LOCALE> [SCREEN_ROW]...
#
# SCREEN_ROW format: "NN slug deep-path"  (same as the SCREENS arrays in SKILL.md)
#
# Idempotent — safe to re-run after each capture. Pass `-` for the Android
# target to let adb pick the only attached device.

set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 <ios|android> <UDID|SERIAL|-> <DIR> <LOCALE> [SCREEN_ROW]..." >&2
  exit 1
fi

platform="$1"
target="$2"
dir="$3"
locale="$4"
shift 4
# Remaining positional args are SCREEN_ROWs.

[[ -d "$dir" ]] || { echo "error: not a directory: $dir" >&2; exit 1; }

device_label=$(basename "$dir")
captured=$(date '+%Y-%m-%d')

# Resolution = dimensions of any captured PNG in the folder (post-resize, so
# this reflects the final delivered size).
png=$(find "$dir" -maxdepth 1 -name '*.png' -print -quit 2>/dev/null || true)
if [[ -n "$png" ]] && command -v magick >/dev/null 2>&1; then
  resolution=$(magick identify -format "%wx%h" "$png")
else
  resolution="(no PNG found)"
fi

case "$platform" in
  ios)
    # `xcrun simctl list devices` format:
    #   == Devices ==
    #   -- iOS 18.3 --
    #       iPhone 16 Pro Max (427DD273-...) (Booted)
    line=$(xcrun simctl list devices 2>/dev/null \
      | awk -v u="$target" '
          /^-- / { rt=$0; sub(/^-- /, "", rt); sub(/ --$/, "", rt) }
          $0 ~ u  { print rt "|" $0; exit }
        ')
    runtime=${line%%|*}
    model_line=${line#*|}
    model=$(echo "$model_line" | sed -E 's/^[[:space:]]+//; s/ \([0-9A-Fa-f-]+\).*//')
    os_short=${runtime:-(unknown)}
    : "${model:=(unknown)}"
    ;;
  android)
    adb_cmd=(adb)
    if [[ "$target" != "-" && -n "$target" ]]; then
      adb_cmd+=(-s "$target")
    fi
    model=$("${adb_cmd[@]}" shell getprop ro.product.model 2>/dev/null | tr -d '\r' || true)
    avd=$("${adb_cmd[@]}" shell getprop ro.boot.qemu.avd_name 2>/dev/null | tr -d '\r' || true)
    rel=$("${adb_cmd[@]}" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r' || true)
    sdk=$("${adb_cmd[@]}" shell getprop ro.build.version.sdk 2>/dev/null | tr -d '\r' || true)
    [[ -n "$avd" ]] && model="$avd ($model)"
    : "${model:=(unknown)}"
    if [[ -n "$rel" ]]; then
      os_short="Android $rel (API $sdk)"
    else
      os_short="(unknown)"
    fi
    ;;
  *)
    echo "error: platform must be 'ios' or 'android'" >&2
    exit 1
    ;;
esac

out="$dir/summary.md"
{
  echo "# $device_label · $locale"
  echo
  echo "| Field | Value |"
  echo "| --- | --- |"
  echo "| Model | $model |"
  echo "| OS | $os_short |"
  echo "| Resolution | $resolution |"
  echo "| Locale | $locale |"
  echo "| Last captured | $captured |"
  if [[ $# -gt 0 ]]; then
    echo
    echo "## Screens"
    echo
    echo "| NN | Slug | Deep link |"
    echo "| --- | --- | --- |"
    for row in "$@"; do
      read -r nn slug path <<<"$row"
      echo "| $nn | $slug | \`$path\` |"
    done
  fi
} > "$out"

echo "wrote $out"
