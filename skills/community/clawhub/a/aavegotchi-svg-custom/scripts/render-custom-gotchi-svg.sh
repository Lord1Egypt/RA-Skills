#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PNG_SIZE="${AAVEGOTCHI_SVG_PNG_SIZE:-512}"
EXPORT_PNG=1
NODE_ARGS=()

for arg in "$@"; do
  if [[ "$arg" == "--no-png" ]]; then
    EXPORT_PNG=0
    continue
  fi
  NODE_ARGS+=("$arg")
done

pick_raster_tool() {
  if [[ -d "$ROOT_DIR/node_modules/@resvg/resvg-js" ]]; then
    printf 'resvg-js'
    return 0
  fi
  if command -v qlmanage >/dev/null 2>&1; then
    printf 'qlmanage'
    return 0
  fi
  if command -v rsvg-convert >/dev/null 2>&1; then
    printf 'rsvg-convert'
    return 0
  fi
  if command -v magick >/dev/null 2>&1; then
    printf 'magick'
    return 0
  fi
  if command -v convert >/dev/null 2>&1; then
    printf 'convert'
    return 0
  fi
  if command -v inkscape >/dev/null 2>&1; then
    printf 'inkscape'
    return 0
  fi
  return 1
}

rasterize_svg() {
  local tool="$1"
  local svg_path="$2"
  local png_path="$3"
  local size="$4"

  case "$tool" in
    resvg-js)
      node "$ROOT_DIR/scripts/rasterize-svg.mjs" "$svg_path" "$png_path" "$size"
      ;;
    qlmanage)
      local tmpdir base generated
      tmpdir="$(mktemp -d)"
      base="$(basename "$svg_path")"
      generated="$tmpdir/${base}.png"
      qlmanage -t -s "$size" -o "$tmpdir" "$svg_path" >/dev/null 2>&1
      if [[ ! -f "$generated" ]]; then
        rm -rf "$tmpdir"
        return 1
      fi
      mv "$generated" "$png_path"
      rm -rf "$tmpdir"
      ;;
    rsvg-convert)
      rsvg-convert -w "$size" -h "$size" "$svg_path" -o "$png_path"
      ;;
    magick)
      magick -background none -density 384 -filter point -resize "${size}x${size}" "$svg_path" "$png_path"
      ;;
    convert)
      convert -background none -density 384 -filter point -resize "${size}x${size}" "$svg_path" "$png_path"
      ;;
    inkscape)
      inkscape "$svg_path" --export-type=png --export-filename="$png_path" -w "$size" -h "$size" >/dev/null 2>&1
      ;;
    *)
      return 1
      ;;
  esac
}

warnings_json() {
  printf '%s\n' "$@" | node -e 'const fs = require("node:fs"); const values = fs.readFileSync(0, "utf8").split(/\n/).map((value) => value.trim()).filter(Boolean); process.stdout.write(JSON.stringify(values));'
}

write_manifest() {
  local manifest_path="$1"
  local raster_tool="$2"
  local enabled="$3"
  local size="$4"
  local front_png="$5"
  local left_png="$6"
  local right_png="$7"
  local back_png="$8"
  local warnings="$9"

  node -e 'const fs = require("node:fs"); const [manifestPath, rasterTool, enabledRaw, sizeRaw, frontPng, leftPng, rightPng, backPng, warningsJson] = process.argv.slice(1); const data = JSON.parse(fs.readFileSync(manifestPath, "utf8")); const warnings = JSON.parse(warningsJson); data.output = data.output || {}; data.output.front_png = frontPng || null; data.output.left_png = leftPng || null; data.output.right_png = rightPng || null; data.output.back_png = backPng || null; data.png_export = { enabled: enabledRaw === "true", tool: rasterTool || null, size: Number(sizeRaw) }; data.warnings = [...new Set([...(data.warnings || []), ...warnings])]; fs.writeFileSync(manifestPath, `${JSON.stringify(data, null, 2)}\n`); process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);' "$manifest_path" "$raster_tool" "$enabled" "$size" "$front_png" "$left_png" "$right_png" "$back_png" "$warnings"
}

TMP_JSON="$(mktemp)"
trap 'rm -f "$TMP_JSON"' EXIT

node "$ROOT_DIR/scripts/render-svg-custom.mjs" "${NODE_ARGS[@]}" > "$TMP_JSON"

MANIFEST_PATH="$(node -e 'const fs = require("node:fs"); try { const data = JSON.parse(fs.readFileSync(process.argv[1], "utf8")); process.stdout.write(String(data.output?.manifest_json || "")); } catch { process.stdout.write(""); }' "$TMP_JSON")"

if [[ -z "$MANIFEST_PATH" || ! -f "$MANIFEST_PATH" ]]; then
  cat "$TMP_JSON"
  exit 0
fi

if [[ "$EXPORT_PNG" -eq 0 ]]; then
  cat "$TMP_JSON"
  exit 0
fi

SVG_PATHS=()
while IFS= read -r line; do
  SVG_PATHS+=("$line")
done < <(node -e 'const fs = require("node:fs"); const data = JSON.parse(fs.readFileSync(process.argv[1], "utf8")); for (const key of ["front_svg", "left_svg", "right_svg", "back_svg"]) { process.stdout.write(`${String(data.output?.[key] || "")}\n`); }' "$MANIFEST_PATH")

PNG_PATHS=("" "" "" "")
WARNINGS=()
RASTER_TOOL=""

if ! RASTER_TOOL="$(pick_raster_tool)"; then
  WARNINGS+=("No supported SVG rasterizer found; PNG export skipped.")
  WARNINGS_JSON='[]'
  if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    WARNINGS_JSON="$(warnings_json "${WARNINGS[@]}")"
  fi
  write_manifest "$MANIFEST_PATH" "" false "$PNG_SIZE" "" "" "" "" "$WARNINGS_JSON"
  exit 0
fi

for index in 0 1 2 3; do
  SVG_PATH="${SVG_PATHS[$index]}"
  if [[ -z "$SVG_PATH" || ! -f "$SVG_PATH" ]]; then
    continue
  fi
  PNG_PATH="${SVG_PATH%.svg}.png"
  if rasterize_svg "$RASTER_TOOL" "$SVG_PATH" "$PNG_PATH" "$PNG_SIZE"; then
    PNG_PATHS[$index]="$PNG_PATH"
  else
    WARNINGS+=("PNG export failed for $(basename "$SVG_PATH") using ${RASTER_TOOL}.")
    rm -f "$PNG_PATH"
  fi
done

WARNINGS_JSON='[]'
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  WARNINGS_JSON="$(warnings_json "${WARNINGS[@]}")"
fi

write_manifest \
  "$MANIFEST_PATH" \
  "$RASTER_TOOL" \
  true \
  "$PNG_SIZE" \
  "${PNG_PATHS[0]}" \
  "${PNG_PATHS[1]}" \
  "${PNG_PATHS[2]}" \
  "${PNG_PATHS[3]}" \
  "$WARNINGS_JSON"
