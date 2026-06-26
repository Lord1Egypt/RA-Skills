#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WRAPPER="$SCRIPT_DIR/render-custom-gotchi-svg.sh"
HAS_SLUG=0
HAS_BACKGROUND=0
ARGS=()

for arg in "$@"; do
  if [[ "$arg" == "--slug" ]]; then
    HAS_SLUG=1
  elif [[ "$arg" == "--background" || "$arg" == "--background-mode" ]]; then
    HAS_BACKGROUND=1
  fi
  ARGS+=("$arg")
done

if [[ "$HAS_SLUG" -eq 0 ]]; then
  ARGS+=("--slug" "tg-$(date +%s)-$RANDOM")
fi

if [[ "$HAS_BACKGROUND" -eq 0 ]]; then
  ARGS+=("--background" "common")
fi

manifest_json="$("$WRAPPER" "${ARGS[@]}")"

node -e '
const manifest = JSON.parse(process.argv[1]);
function relForOpenClaw(file) {
  if (!file) return "";
  const marker = "/.openclaw/workspace/";
  const idx = file.indexOf(marker);
  if (idx >= 0) return `./${file.slice(idx + marker.length)}`;
  return file;
}
const front = relForOpenClaw(manifest.output?.front_png || manifest.output?.front);
const left = relForOpenClaw(manifest.output?.left_png || manifest.output?.left);
const right = relForOpenClaw(manifest.output?.right_png || manifest.output?.right);
const back = relForOpenClaw(manifest.output?.back_png || manifest.output?.back);
const rarity = manifest.rarity?.tier || "unknown";
const color = manifest.rarity?.color_name || manifest.rarity?.color_hex || "";
const background = manifest.background || {};
const backgroundLabel = background.label || background.tier || manifest.request?.background_mode || "rarity";
const backgroundColor = background.color_name || background.color_hex || background.colorName || background.colorHex || "";
const outfit = (manifest.request?.wearableNames || [])
  .map((entry) => entry?.name || "")
  .filter(Boolean)
  .join(", ") || "custom loadout";
const summary = `OG SVG gotchi rendered. Rarity: ${rarity}${color ? ` (${color})` : ""}. Background: ${backgroundLabel}${backgroundColor ? ` (${backgroundColor})` : ""}. Outfit: ${outfit}.`;
console.log(`FRONT_MEDIA=${front}`);
console.log(`LEFT_MEDIA=${left}`);
console.log(`RIGHT_MEDIA=${right}`);
console.log(`BACK_MEDIA=${back}`);
console.log(`CAPTION_FRONT=OG SVG gotchi - front view`);
console.log(`CAPTION_LEFT=OG SVG gotchi - left view`);
console.log(`CAPTION_RIGHT=OG SVG gotchi - right view`);
console.log(`CAPTION_BACK=OG SVG gotchi - back view`);
console.log(`SUMMARY=${summary}`);
' "$manifest_json"
