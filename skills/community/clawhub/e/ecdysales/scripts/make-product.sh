#!/bin/bash
# Ecdysales v2 — Product Image Generator
# Adds watermark pattern + brand logo + price sticker to product images
# Assets auto-resolve relative to this script's location.
#
# Usage: ./make-product.sh <image> <price> [options]
#
# By default: watermark + logo + sticker are ALL applied.
# Use --no-watermark, --no-logo, --no-sticker to skip any layer.
#
# Options:
#   -o, --output <path>          Output file (default: output.jpg)
#   -P, --position <pos>         Sticker position (default: top-right)
#   --logo-position <pos>        Logo position (default: bottom-right)
#   --logo-size <pct>            Logo width as % of image width (default: 15)
#   --logo-opacity <pct>         Logo opacity 0-100 (default: 80)
#   --sticker-fill <color>       Sticker fill (default: #FFD700)
#   --sticker-stroke <color>     Sticker stroke (default: #000000)
#   --sticker-stroke-width <px>  Sticker stroke width (default: 4)
#   --text-color <color>         Price text color (default: #000000)
#   --font <name>                Font (default: Helvetica-Bold)
#   --font-size <px>             Font size (default: 48)
#   --corner-radius <px>         Sticker corner radius (default: 20)
#   --padding <px>               Sticker padding (default: 30)
#   --pattern-opacity <pct>      Watermark opacity 0-100 (default: 25)
#   --no-watermark               Skip watermark pattern
#   --no-logo                    Skip brand logo
#   --no-sticker                 Skip price sticker

set -euo pipefail

# ─── Resolve assets relative to script ──────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="${SCRIPT_DIR}/../assets"
PATTERN="${ASSETS_DIR}/watermark-pattern.png"
LOGO="${ASSETS_DIR}/logo.png"

# ─── Defaults ───────────────────────────────────────────
OUTPUT="output.jpg"
POSITION="top-right"
LOGO_POSITION="bottom-right"
LOGO_SIZE=15
LOGO_OPACITY=80
STICKER_FILL="#FFD700"
STICKER_STROKE="#000000"
STICKER_STROKE_WIDTH=4
TEXT_COLOR="#000000"
FONT="Helvetica-Bold"
FONT_SIZE=48
CORNER_RADIUS=20
PADDING=30
PATTERN_OPACITY=25
NO_WATERMARK=false
NO_LOGO=false
NO_STICKER=false
WIDTH_RATIO=0
HEIGHT_RATIO=0

# ─── Parse args ─────────────────────────────────────────
ORIGINAL="${1:?Usage: ./make-product.sh <image> <price> [options]}"
PRICE="${2:-}"
if [ -z "$PRICE" ] || [[ "$PRICE" == -* ]]; then
  shift 1
else
  shift 2
fi

# Strip surrounding quotes from price if present
PRICE="${PRICE#\"}"
PRICE="${PRICE%\"}"
PRICE="${PRICE#\'}"
PRICE="${PRICE%\'}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)              OUTPUT="$2"; shift 2 ;;
    -P|--position)            POSITION="$2"; shift 2 ;;
    --logo-position)          LOGO_POSITION="$2"; shift 2 ;;
    --logo-size)              LOGO_SIZE="$2"; shift 2 ;;
    --logo-opacity)           LOGO_OPACITY="$2"; shift 2 ;;
    --sticker-fill)           STICKER_FILL="$2"; shift 2 ;;
    --sticker-stroke)         STICKER_STROKE="$2"; shift 2 ;;
    --sticker-stroke-width)   STICKER_STROKE_WIDTH="$2"; shift 2 ;;
    --text-color)             TEXT_COLOR="$2"; shift 2 ;;
    --font)                   FONT="$2"; shift 2 ;;
    --font-size)              FONT_SIZE="$2"; shift 2 ;;
    --corner-radius)          CORNER_RADIUS="$2"; shift 2 ;;
    --padding)                PADDING="$2"; shift 2 ;;
    --pattern-opacity)        PATTERN_OPACITY="$2"; shift 2 ;;
    --no-watermark)           NO_WATERMARK=true; shift ;;
    --no-logo)                NO_LOGO=true; shift ;;
    --no-sticker)             NO_STICKER=true; shift ;;
    --width-ratio)            WIDTH_RATIO="$2"; shift 2 ;;
    --height-ratio)           HEIGHT_RATIO="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ─── Temp files ─────────────────────────────────────────
TMPDIR_WORK=$(mktemp -d)
trap 'rm -rf "$TMPDIR_WORK"' EXIT

# ─── Validate ───────────────────────────────────────────
if [ "$NO_STICKER" = false ] && [ -z "$PRICE" ]; then
  echo "❌ Price required (pass --no-sticker to skip)"
  exit 1
fi

if [ ! -f "$ORIGINAL" ]; then
  echo "❌ Image not found: $ORIGINAL"
  exit 1
fi

# ─── Image dimensions ──────────────────────────────────
IMG_W=$(identify -format "%w" "$ORIGINAL")
IMG_H=$(identify -format "%h" "$ORIGINAL")

# ─── Position helper ────────────────────────────────────
calc_position() {
  local obj_w="$1" obj_h="$2" pos="$3"
  local offset=30
  case "$pos" in
    top-left)     echo "$offset $offset" ;;
    top-right)    echo "$((IMG_W - obj_w - offset)) $offset" ;;
    bottom-left)  echo "$offset $((IMG_H - obj_h - offset))" ;;
    bottom-right) echo "$((IMG_W - obj_w - offset)) $((IMG_H - obj_h - offset))" ;;
    random)       local arr=("top-left" "top-right" "bottom-left" "bottom-right")
                  calc_position "$obj_w" "$obj_h" "${arr[$((RANDOM % 4))]}" ;;
    *)            echo "$((IMG_W - obj_w - offset)) $offset" ;;
  esac
}

CURRENT="$ORIGINAL"

# ─── Step 1: Watermark ─────────────────────────────────
if [ "$NO_WATERMARK" = false ] && [ -f "$PATTERN" ]; then
  PAT_W=$((IMG_W / 6))
  PAT_H=$((IMG_H / 6))

  convert "$PATTERN" -resize ${PAT_W}x${PAT_H} "$TMPDIR_WORK/pattern_scaled.png"
  convert -size ${IMG_W}x${IMG_H} tile:"$TMPDIR_WORK/pattern_scaled.png" "$TMPDIR_WORK/pattern_tiled.png"
  convert "$CURRENT" "$TMPDIR_WORK/pattern_tiled.png" \
    -compose blend -define compose:args=${PATTERN_OPACITY} -composite \
    "$TMPDIR_WORK/watermarked.jpg"
  CURRENT="$TMPDIR_WORK/watermarked.jpg"
  echo "🔲 Watermark applied (${PATTERN_OPACITY}%)"
elif [ "$NO_WATERMARK" = false ]; then
  echo "⚠️  No watermark pattern at $PATTERN — skipping"
fi

# ─── Step 2: Logo ──────────────────────────────────────
if [ "$NO_LOGO" = false ] && [ -f "$LOGO" ]; then
  LOGO_W=$((IMG_W * LOGO_SIZE / 100))

  convert "$LOGO" -resize ${LOGO_W}x -alpha set \
    -channel A -evaluate multiply $(echo "$LOGO_OPACITY / 100" | bc -l) +channel \
    "$TMPDIR_WORK/logo_scaled.png"

  LW=$(identify -format "%w" "$TMPDIR_WORK/logo_scaled.png")
  LH=$(identify -format "%h" "$TMPDIR_WORK/logo_scaled.png")
  read LX LY <<< $(calc_position "$LW" "$LH" "$LOGO_POSITION")

  convert "$CURRENT" "$TMPDIR_WORK/logo_scaled.png" \
    -geometry +${LX}+${LY} -compose over -composite \
    "$TMPDIR_WORK/with_logo.jpg"
  CURRENT="$TMPDIR_WORK/with_logo.jpg"
  echo "🏷️  Logo applied (${LOGO_SIZE}% width, ${LOGO_POSITION})"
elif [ "$NO_LOGO" = false ]; then
  echo "⚠️  No logo at $LOGO — skipping"
fi

# ─── Step 3: Sticker ───────────────────────────────────
if [ "$NO_STICKER" = false ]; then
  # If ratios are set, calculate dimensions from image size
  if [ "$(echo "$WIDTH_RATIO > 0" | bc -l)" -eq 1 ] && [ "$(echo "$HEIGHT_RATIO > 0" | bc -l)" -eq 1 ]; then
    TARGET_W=$(echo "$IMG_W * $WIDTH_RATIO" | bc | cut -d. -f1)
    TARGET_H=$(echo "$IMG_H * $HEIGHT_RATIO" | bc | cut -d. -f1)
    
    # Auto-size font to fit within target box (start large, shrink until it fits)
    AUTO_FONT_SIZE=$FONT_SIZE
    for TEST_SIZE in 120 100 90 80 72 64 56 48 42 36 32 28 24 20 16; do
      TEXT_INFO=$(convert -font "$FONT" -pointsize $TEST_SIZE \
        caption:"$PRICE" -trim -format '%wx%h' info:)
      TW=$(echo "$TEXT_INFO" | cut -dx -f1)
      TH=$(echo "$TEXT_INFO" | cut -dx -f2)
      PAD_W=$((TARGET_W - TW))
      PAD_H=$((TARGET_H - TH))
      if [ "$PAD_W" -gt 10 ] && [ "$PAD_H" -gt 10 ]; then
        AUTO_FONT_SIZE=$TEST_SIZE
        PADDING=$((PAD_W / 2))
        break
      fi
    done
    FONT_SIZE=$AUTO_FONT_SIZE
    STICKER_W=$TARGET_W
    STICKER_H=$TARGET_H
    echo "📐 Reactive sticker: ${STICKER_W}x${STICKER_H} (${WIDTH_RATIO}x${HEIGHT_RATIO}), font ${FONT_SIZE}px"
  else
    TEXT_INFO=$(convert -font "$FONT" -pointsize $FONT_SIZE \
      caption:"$PRICE" -trim -format '%wx%h' info:)
    TEXT_WIDTH=$(echo "$TEXT_INFO" | cut -dx -f1)
    TEXT_HEIGHT=$(echo "$TEXT_INFO" | cut -dx -f2)

    STICKER_W=$((TEXT_WIDTH + PADDING * 2))
    STICKER_H=$((TEXT_HEIGHT + PADDING * 2))
  fi

  # Build sticker: rounded rectangle background + text as separate layers
  convert -size ${STICKER_W}x${STICKER_H} xc:none \
    -fill "$STICKER_FILL" -stroke "$STICKER_STROKE" -strokewidth $STICKER_STROKE_WIDTH \
    -draw "roundrectangle $((STICKER_STROKE_WIDTH/2)),$((STICKER_STROKE_WIDTH/2)) \
           $((STICKER_W - STICKER_STROKE_WIDTH/2)),$((STICKER_H - STICKER_STROKE_WIDTH/2)) \
           $CORNER_RADIUS,$CORNER_RADIUS" \
    "$TMPDIR_WORK/sticker_bg.png"

  # Generate text layer using caption (handles $ correctly unlike -draw)
  convert -font "$FONT" -pointsize $FONT_SIZE -fill "$TEXT_COLOR" -background none \
    caption:"$PRICE" -trim "$TMPDIR_WORK/sticker_text.png"

  # Composite text onto sticker background, centered
  convert "$TMPDIR_WORK/sticker_bg.png" "$TMPDIR_WORK/sticker_text.png" \
    -gravity center -composite \
    "$TMPDIR_WORK/sticker.png"

  read SX SY <<< $(calc_position "$STICKER_W" "$STICKER_H" "$POSITION")

  convert "$CURRENT" "$TMPDIR_WORK/sticker.png" \
    -geometry +${SX}+${SY} -compose over -composite \
    "$OUTPUT"
  echo "💰 Sticker applied ($PRICE, ${POSITION})"
else
  cp "$CURRENT" "$OUTPUT"
fi

echo "✅ Done: $OUTPUT (${IMG_W}x${IMG_H})"
