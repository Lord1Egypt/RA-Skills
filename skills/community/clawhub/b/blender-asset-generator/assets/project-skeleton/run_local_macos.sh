#!/usr/bin/env bash
set -euo pipefail

# Local macOS runner (Blender 4.2)
#
# Usage:
#   chmod +x run_local_macos.sh
#   ./run_local_macos.sh
#
# Override Blender binary:
#   export BLENDER_BIN="/Applications/Blender.app/Contents/MacOS/Blender"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

SPEC="$ROOT/spec.json"
LOG="$ROOT/run-log.txt"
SCENE="$ROOT/scene.blend"
RENDERS="$ROOT/renders"

mkdir -p "$ROOT/exports" "$RENDERS"

BLENDER_BIN="${BLENDER_BIN:-/Applications/Blender.app/Contents/MacOS/Blender}"
if [[ ! -x "$BLENDER_BIN" ]]; then
  echo "Blender binary not found/executable: $BLENDER_BIN" >&2
  exit 1
fi

OUT_GLB="$(python3 -c 'import json; print(json.load(open("spec.json"))["outputs"]["export_glb"])')"
OUT_FBX="$(python3 -c 'import json; print(json.load(open("spec.json"))["outputs"].get("export_fbx_optional") or "")')"
OUT_USDC="$(python3 -c 'import json; print(json.load(open("spec.json"))["outputs"].get("export_usdc_optional") or "")')"

"$BLENDER_BIN" -b --python scripts/build.py -- --spec "$SPEC" --out_blend "$SCENE" --log "$LOG"
"$BLENDER_BIN" -b --python scripts/render.py -- --blend "$SCENE" --out_dir "$RENDERS" --log "$LOG"

if [[ -z "$OUT_FBX" ]]; then
  "$BLENDER_BIN" -b --python scripts/export.py -- --blend "$SCENE" --out_glb "$ROOT/$OUT_GLB" --log "$LOG"
else
  "$BLENDER_BIN" -b --python scripts/export.py -- --blend "$SCENE" --out_glb "$ROOT/$OUT_GLB" --out_fbx "$ROOT/$OUT_FBX" --log "$LOG"
fi

if [[ -n "$OUT_USDC" ]]; then
  "$BLENDER_BIN" -b --python scripts/export.py -- --blend "$SCENE" --out_glb "$ROOT/$OUT_GLB" --out_usdc "$ROOT/$OUT_USDC" --log "$LOG"
fi

echo "OK. Outputs:"
echo " - $ROOT/$OUT_GLB"
if [[ -n "$OUT_FBX" ]]; then echo " - $ROOT/$OUT_FBX"; fi
if [[ -n "$OUT_USDC" ]]; then echo " - $ROOT/$OUT_USDC"; fi
echo " - renders/front.png"
echo " - renders/three_quarter.png"
echo " - run-log.txt"
