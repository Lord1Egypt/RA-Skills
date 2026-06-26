#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER="${SCRIPT_DIR}/render-gotchi-sprite.sh"
HAS_SLUG=0
HAS_OUTPUT_DIR=0
HAS_BACKGROUND=0
ARGS=()

for arg in "$@"; do
  if [[ "$arg" == "--slug" ]]; then
    HAS_SLUG=1
  elif [[ "$arg" == "--output-dir" ]]; then
    HAS_OUTPUT_DIR=1
  elif [[ "$arg" == "--background" || "$arg" == "--background-mode" ]]; then
    HAS_BACKGROUND=1
  fi
  ARGS+=("$arg")
done

if [[ "$HAS_SLUG" -eq 0 ]]; then
  ARGS+=("--slug" "tg-$(date +%s)-$RANDOM")
fi

if [[ "$HAS_OUTPUT_DIR" -eq 0 ]]; then
  ARGS+=("--output-dir" "./output/chat-$(date +%s)-$RANDOM")
fi

if [[ "$HAS_BACKGROUND" -eq 0 ]]; then
  ARGS+=("--background" "common")
fi

result_json="$("${WRAPPER}" "${ARGS[@]}")"
manifest_json="$(node -e 'const result = JSON.parse(process.argv[1]); console.log(result.manifest_json);' "$result_json")"

node -e '
const fs = require("fs");
const manifest = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const sprite = manifest.output?.sprite_png || "";
const gif = manifest.output?.sprite_gif || "";
const gotchi = manifest.request || {};
const attrs = Array.isArray(gotchi.attributes) ? gotchi.attributes : [];
const body = attrs.find((a) => a.trait_type === "Wearable (Body)")?.value || "none";
const face = attrs.find((a) => a.trait_type === "Wearable (Face)")?.value || "none";
const eyes = attrs.find((a) => a.trait_type === "Wearable (Eyes)")?.value || "none";
const head = attrs.find((a) => a.trait_type === "Wearable (Head)")?.value || "none";
const hands = attrs.filter((a) => a.trait_type === "Wearable (Hands)").map((a) => a.value).join(", ") || "none";
const bg = manifest.background || {};
const rows = Array.isArray(gotchi.gif_rows) ? gotchi.gif_rows.join(",") : "0";
const zoom = gotchi.zoom || 100;
const frameSize = gotchi.frame_size || 100;
const canvasSize = gotchi.canvas_size || frameSize;
const shiftPx = gotchi.vertical_shift_px ?? 0;
const summary = `Sprite gotchi rendered. Background: ${bg.label || gotchi.background_mode || "Common"}${bg.color_hex ? ` (${bg.color_hex})` : ""}. Canvas: ${canvasSize}x${canvasSize}. Source frame: ${frameSize}x${frameSize}. Placement: body centered on the canvas vertical axis, anchored 3px upward by default. Zoom: ${zoom}%. GIF rows: ${rows}. Collateral: ${gotchi.collateral || attrs.find((a) => a.trait_type === "Base Body")?.value || "unknown"}. Eye shape: ${attrs.find((a) => a.trait_type === "Eye Shape")?.value || "none"}. Eye color: ${attrs.find((a) => a.trait_type === "Eye Color")?.value || "none"}. Wearables: body=${body}, face=${face}, eyes=${eyes}, head=${head}, hands=${hands}.`;
console.log(`SPRITE_MEDIA=${sprite}`);
console.log(`GIF_MEDIA=${gif}`);
console.log(`SPRITE_FILEPATH=${sprite}`);
console.log(`GIF_FILEPATH=${gif}`);
console.log(`CAPTION_SPRITE=Aavegotchi game sprite sheet`);
console.log(`CAPTION_GIF=Aavegotchi animated sprite gif`);
console.log(`SUMMARY=${summary}`);
' "$manifest_json"
