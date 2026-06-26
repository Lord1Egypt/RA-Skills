#!/usr/bin/env bash
# Batch resize PNGs to a target dimension using ImageMagick (fits + center-crops).
#
# Usage:
#   bash resize.sh <DIR_OR_GLOB> <WIDTHxHEIGHT>
#
# Examples:
#   bash resize.sh screenshots/en-US/iphone        1284x2778
#   bash resize.sh 'screenshots/*/android-phone'   1440x3120
#
# Idempotent — files already at the target size are skipped.

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: $0 <DIR_OR_GLOB> <WIDTHxHEIGHT>" >&2
  exit 1
fi

target="$1"
size="$2"

if ! command -v magick >/dev/null 2>&1; then
  echo "error: ImageMagick 'magick' not found in PATH" >&2
  exit 1
fi

if [[ ! "$size" =~ ^[0-9]+x[0-9]+$ ]]; then
  echo "error: size must be WIDTHxHEIGHT (e.g. 1284x2778)" >&2
  exit 1
fi

# Expand DIR → DIR/*.png; otherwise treat as glob
if [[ -d "$target" ]]; then
  shopt -s nullglob
  files=( "$target"/*.png )
else
  shopt -s nullglob
  files=( $target )
fi

if [[ ${#files[@]} -eq 0 ]]; then
  echo "error: no PNG files matched: $target" >&2
  exit 1
fi

for f in "${files[@]}"; do
  current=$(magick identify -format "%wx%h" "$f")
  if [[ "$current" == "$size" ]]; then
    echo "skip  $f (already $size)"
    continue
  fi
  magick "$f" -resize "${size}^" -gravity center -extent "$size" "$f"
  echo "resize $f  $current -> $size"
done
