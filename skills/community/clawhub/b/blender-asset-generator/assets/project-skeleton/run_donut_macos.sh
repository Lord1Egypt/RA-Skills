#!/usr/bin/env bash
set -euo pipefail

# Builds a simple donut scene (donut + icing + sprinkles) and renders previews.
#
# Usage:
#   chmod +x run_donut_macos.sh
#   ./run_donut_macos.sh
#
# Override Blender binary:
#   export BLENDER_BIN="/Applications/Blender.app/Contents/MacOS/Blender"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

LOG="$ROOT/run-log.txt"
BLEND="$ROOT/donut.blend"
RENDERS="$ROOT/renders"
mkdir -p "$RENDERS"
mkdir -p "$ROOT/exports"

OUT_GLB="$ROOT/exports/donut.glb"
OUT_USDC="$ROOT/exports/donut.usdc"

BLENDER_BIN="${BLENDER_BIN:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [[ ! -x "$BLENDER_BIN" ]]; then
  echo "Blender binary not found/executable: $BLENDER_BIN" >&2
  exit 1
fi

"$BLENDER_BIN" -b --python scripts/donut_build.py -- --out_blend "$BLEND" --log "$LOG"
# Verify donut.blend exists (Blender may exit 0 even if the script errors).
if [[ ! -f "$BLEND" ]]; then
  echo "Donut build failed: missing $BLEND. Check $LOG for details." >&2
  exit 1
fi
"$BLENDER_BIN" -b --python scripts/render.py -- --blend "$BLEND" --out_dir "$RENDERS" --log "$LOG"
"$BLENDER_BIN" -b --python scripts/export.py -- --blend "$BLEND" --out_glb "$OUT_GLB" --out_usdc "$OUT_USDC" --log "$LOG"

echo "OK. Outputs:"
echo " - $BLEND"
echo " - $OUT_GLB"
echo " - $OUT_USDC"
echo " - renders/front.png"
echo " - renders/three_quarter.png"
echo " - run-log.txt"
