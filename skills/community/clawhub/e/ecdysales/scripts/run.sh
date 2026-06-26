#!/bin/bash
# Ecdysales Lite — run.sh
# Single entry point: give it an image + price, get back a watermarked product image.
# For standalone CLI and AI agent integration.
#
# Usage:
#   ./run.sh <image> '<price>'                  # Standard — all layers (USE SINGLE QUOTES!)
#   ./run.sh <image> '<price>' --sticker-only   # Just the price tag
#   ./run.sh <image> '<price>' --no-logo        # Skip brand logo
#   ./run.sh <image> '<price>' --no-watermark   # Skip watermark
#
# ⚠️  ALWAYS use single quotes for prices starting with $:
#     ✅ ./run.sh img.jpg '$1300'
#     ❌ ./run.sh img.jpg "$1300"   ← $1 becomes shell variable!
#   ./run.sh --latest <price>                   # Auto-find latest image (set ECDYSALES_MEDIA_DIR or defaults to ~/Pictures/incoming)
#   ./run.sh --batch <dir> <prices.txt>         # Batch process
#   ./run.sh --json <image> <price>             # JSON output for piping
#
# Output: always goes to output/<timestamp>.jpg (or stdout with --json)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MAKE_PRODUCT="${SCRIPT_DIR}/make-product.sh"
OUTPUT_DIR="${SCRIPT_DIR}/../output"
CONFIG_DIR="${SCRIPT_DIR}/../config"
MEDIA_DIR="${ECDYSALES_MEDIA_DIR:-$HOME/Pictures/incoming}"

# Ensure output dir exists
mkdir -p "$OUTPUT_DIR"

# ─── JSON mode ──────────────────────────────────────────
JSON_MODE=false
if [[ "${1:-}" == "--json" ]]; then
  JSON_MODE=true
  shift
fi

# ─── Latest image finder ────────────────────────────────
find_latest_image() {
  local search_dir="${1:-$MEDIA_DIR}"
  if [ ! -d "$search_dir" ]; then
    echo "❌ Media directory not found: $search_dir" >&2
    exit 1
  fi
  # Find newest image file (jpg, png, webp)
  find "$search_dir" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) -printf '%T@ %p\n' 2>/dev/null \
    | sort -rn | head -1 | cut -d' ' -f2-
}

# ─── Batch mode ─────────────────────────────────────────
if [[ "${1:-}" == "--batch" ]]; then
  BATCH_DIR="${2:?Usage: run.sh --batch <image_dir> <prices_file>}"
  PRICES_FILE="${3:?Usage: run.sh --batch <image_dir> <prices_file>}"
  
  if [ ! -d "$BATCH_DIR" ]; then echo "❌ Directory not found: $BATCH_DIR"; exit 1; fi
  if [ ! -f "$PRICES_FILE" ]; then echo "❌ Prices file not found: $PRICES_FILE"; exit 1; fi
  
  echo "📦 Batch processing..."
  INDEX=0
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    # Format: filename price [options...]
    read -ra PARTS <<< "$line"
    IMG="${BATCH_DIR}/${PARTS[0]}"
    PRICE="${PARTS[1]}"
    EXTRA_ARGS=("${PARTS[@]:2}")
    
    if [ ! -f "$IMG" ]; then
      echo "⚠️  Skipping ${PARTS[0]} — not found"
      continue
    fi
    
    OUT="${OUTPUT_DIR}/batch-${INDEX}-$(basename "${PARTS[0]}")"
    "$MAKE_PRODUCT" "$IMG" "$PRICE" -o "$OUT" "${EXTRA_ARGS[@]}"
    INDEX=$((INDEX + 1))
  done < "$PRICES_FILE"
  
  echo "✅ Batch done: $INDEX images processed"
  exit 0
fi

# ─── Latest mode ────────────────────────────────────────
if [[ "${1:-}" == "--latest" ]]; then
  shift
  LATEST=$(find_latest_image)
  if [ -z "$LATEST" ]; then
    echo "❌ No images found in media folder"
    exit 1
  fi
  echo "📸 Found: $(basename "$LATEST")"
  set -- "$LATEST" "$@"
fi

# ─── Standard mode ──────────────────────────────────────
IMAGE="${1:?Usage: run.sh <image> <price> [options]}"
PRICE="${2:-}"
EXTRA_ARGS=()

# Collect remaining args
if [ -n "$PRICE" ] && [[ "$PRICE" != -* ]]; then
  shift 2
else
  PRICE=""
  shift 1
fi

# Translate user-friendly flags to make-product.sh flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --sticker-only) EXTRA_ARGS+=("--no-watermark" "--no-logo"); shift ;;
    *)              EXTRA_ARGS+=("$1"); shift ;;
  esac
done

# ─── Load config files ──────────────────────────────────
CONFIG_FLAGS=()

# Validate configs (temporarily disable set -e for validation)
set +e

# Validate sticker config
if [ -f "${CONFIG_DIR}/sticker-config.json" ]; then
  python3 -c "
import json, sys
with open('${CONFIG_DIR}/sticker-config.json') as f:
    c = json.load(f)
errors = []
reactive = c.get('reactive', False)
if reactive:
    wr = c.get('widthRatio', 0)
    hr = c.get('heightRatio', 0)
    if wr <= 0 or hr <= 0:
        errors.append(f'  reactive: true but widthRatio={wr} and heightRatio={hr}. Set both > 0 (e.g. 0.2 and 0.125).')
    if wr > 1 or hr > 1:
        errors.append(f'  widthRatio={wr} or heightRatio={hr} > 1. Sticker would be bigger than image.')
else:
    fs = c.get('fontSize', 0)
    if fs == 'auto':
        errors.append(f'  reactive: false but fontSize=\"auto\". Set a number (e.g. 48).')
    elif not isinstance(fs, (int, float)) or fs <= 0:
        errors.append(f'  reactive: false but fontSize={fs}. Set > 0 (e.g. 48).')
fill = c.get('fill', '')
if fill and not fill.startswith('#'):
    errors.append(f'  fill=\"{fill}\" must be hex color like #FFD700.')
if errors:
    print('❌ Sticker config error:')
    for e in errors: print(e)
    print('Fix: edit config/sticker-config.json')
    sys.exit(1)
" 2>&1
  if [ $? -ne 0 ]; then set -e; exit 1; fi
fi

# Validate watermark config
if [ -f "${CONFIG_DIR}/watermark-config.json" ]; then
  python3 -c "
import json, sys
with open('${CONFIG_DIR}/watermark-config.json') as f:
    c = json.load(f)
errors = []
op = c.get('opacity', 25)
if op < 0 or op > 100:
    errors.append(f'  opacity={op} must be 0-100.')
if errors:
    print('❌ Watermark config error:')
    for e in errors: print(e)
    print('Fix: edit config/watermark-config.json')
    sys.exit(1)
" 2>&1
  if [ $? -ne 0 ]; then set -e; exit 1; fi
fi

# Validate logo config
if [ -f "${CONFIG_DIR}/logo-config.json" ]; then
  python3 -c "
import json, sys
with open('${CONFIG_DIR}/logo-config.json') as f:
    c = json.load(f)
errors = []
sz = c.get('size', 15)
op = c.get('opacity', 80)
if sz <= 0 or sz > 100:
    errors.append(f'  size={sz} must be 1-100 (percent of image width).')
if op < 0 or op > 100:
    errors.append(f'  opacity={op} must be 0-100.')
if errors:
    print('❌ Logo config error:')
    for e in errors: print(e)
    print('Fix: edit config/logo-config.json')
    sys.exit(1)
" 2>&1
  if [ $? -ne 0 ]; then set -e; exit 1; fi
fi

set -e

load_config() {
  local config_file="$1"
  [ ! -f "$config_file" ] && return
  
  python3 -c "
import json, sys
with open('$config_file') as f:
    c = json.load(f)
for k, v in c.items():
    if isinstance(v, bool):
        if v: print(f'--{k.replace(\"_\",\"-\")}')
    else:
        print(f'--{k.replace(\"_\",\"-\")}')
        print(str(v))
" 2>/dev/null | while IFS= read -r line; do
    CONFIG_FLAGS+=("$line")
  done
}

# Load each config (CLI flags override config defaults)
STICKER_FLAGS=()
WATERMARK_FLAGS=()
LOGO_FLAGS=()

if [ -f "${CONFIG_DIR}/sticker-config.json" ]; then
  while IFS= read -r line; do STICKER_FLAGS+=("$line"); done < <(
    python3 -c "
import json
with open('${CONFIG_DIR}/sticker-config.json') as f: c = json.load(f)
reactive = c.get('reactive', False)
m = {'fill':'sticker-fill','stroke':'sticker-stroke','strokeWidth':'sticker-stroke-width','textColor':'text-color','font':'font','fontSize':'font-size','cornerRadius':'corner-radius','padding':'padding','position':'position','widthRatio':'width-ratio','heightRatio':'height-ratio'}
for k,v in c.items():
    if k == 'reactive': continue
    if not reactive and k in ('widthRatio','heightRatio'): continue
    if reactive and k == 'fontSize': continue
    flag = m.get(k, k)
    if isinstance(v, bool):
        if not v: print(f'--no-{flag}')
    elif isinstance(v, (int, float)) and v == 0 and k in ('widthRatio','heightRatio'):
        continue
    else:
        print(f'--{flag}'); print(str(v))
" 2>/dev/null
  )
fi

if [ -f "${CONFIG_DIR}/watermark-config.json" ]; then
  while IFS= read -r line; do WATERMARK_FLAGS+=("$line"); done < <(
    python3 -c "
import json
with open('${CONFIG_DIR}/watermark-config.json') as f: c = json.load(f)
if not c.get('enabled', True): print('--no-watermark')
elif 'opacity' in c: print('--pattern-opacity'); print(str(c['opacity']))
" 2>/dev/null
  )
fi

if [ -f "${CONFIG_DIR}/logo-config.json" ]; then
  while IFS= read -r line; do LOGO_FLAGS+=("$line"); done < <(
    python3 -c "
import json
with open('${CONFIG_DIR}/logo-config.json') as f: c = json.load(f)
if not c.get('enabled', True): print('--no-logo')
else:
    m = {'size':'logo-size','opacity':'logo-opacity','position':'logo-position'}
    for k,v in c.items():
        if k == 'enabled': continue
        flag = m.get(k, k)
        print(f'--{flag}'); print(str(v))
" 2>/dev/null
  )
fi

# Generate output filename
TIMESTAMP=$(date +%s)
OUT_FILE="${OUTPUT_DIR}/${TIMESTAMP}-$(basename "$IMAGE")"

# Run make-product (config flags first, CLI flags override)
if $JSON_MODE; then
  OUTPUT=$("$MAKE_PRODUCT" "$IMAGE" ${PRICE:+\"$PRICE\"} "${WATERMARK_FLAGS[@]}" "${LOGO_FLAGS[@]}" "${STICKER_FLAGS[@]}" -o "$OUT_FILE" "${EXTRA_ARGS[@]}" 2>&1)
  EXIT_CODE=$?
  echo "{\"exit\":$EXIT_CODE,\"output\":\"$(echo "$OUTPUT" | tr '\n' ' ')\"$( [ $EXIT_CODE -eq 0 ] && echo ",\"file\":\"$OUT_FILE\"" || echo "")}"
else
  "$MAKE_PRODUCT" "$IMAGE" ${PRICE:+\"$PRICE\"} "${WATERMARK_FLAGS[@]}" "${LOGO_FLAGS[@]}" "${STICKER_FLAGS[@]}" -o "$OUT_FILE" "${EXTRA_ARGS[@]}"
  echo "📁 Output: $OUT_FILE"
fi
