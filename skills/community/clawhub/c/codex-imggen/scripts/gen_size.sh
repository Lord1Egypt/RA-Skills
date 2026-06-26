#!/bin/bash
# gen_size.sh — Generate image with specific size/aspect ratio
# Usage: gen_size.sh <size_key> <subject_prompt> [output_dir] [-i <ref_image>]
# Size keys: 1K | 2K | 4K | 720p | FHD | HD | 16:9 | 9:16 | 4:3 | 1:1 | <WxH>
set -euo pipefail

PROXY="${http_proxy:-http://127.0.0.1:1080}"
REF_IMAGE=""

# Parse -i before positional args
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--ref-image)
      REF_IMAGE="$2"
      shift 2
      ;;
    -*)
      echo "Unknown option: $1"
      exit 1
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

set -- "${ARGS[@]}"
SIZE_KEY="${1:-}"
SUBJECT="${2:-}"
OUTDIR="${3:-.}"

if [[ -z "$SIZE_KEY" ]] || [[ -z "$SUBJECT" ]]; then
  echo "Usage: gen_size.sh <size_key> <subject> [output_dir] [-i <ref_image>]"
  echo "  size_key: 1K|2K|4K|720p|FHD|HD|16:9|9:16|4:3|1:1 or WxH (e.g. 1920x1080)"
  echo "  subject: Description of what to generate"
  echo "  output_dir: Output directory (default: .)"
  exit 1
fi

WORKDIR=$(mktemp -d)
cd "$WORKDIR" && git init -q
mkdir -p "$OUTDIR"

# Map size key to semantic prompt fragment
case "$SIZE_KEY" in
  1K|1k)
    SIZE_DESC="1 megapixel square image (1:1 aspect ratio, approximately 1024x1024)"
    ;;
  2K|2k)
    SIZE_DESC="2 megapixel image (16:9 wide format, approximately 1920x1080)"
    ;;
  4K|4k)
    SIZE_DESC="4 megapixel 16:9 wide image (approximately 3840x2160)"
    ;;
  720p)
    SIZE_DESC="HD 720p image (1280x720, 16:9)"
    ;;
  FHD|1080p)
    SIZE_DESC="Full HD image (1920x1080, 16:9, 2 megapixels)"
    ;;
  HD)
    SIZE_DESC="HD resolution 16:9 image (approximately 1920x1080)"
    ;;
  16:9)
    SIZE_DESC="wide 16:9 image, approximately 2 megapixels (like 1920x1080)"
    ;;
  9:16)
    SIZE_DESC="vertical 9:16 image, approximately 1.5 megapixels (like 1080x1920)"
    ;;
  4:3)
    SIZE_DESC="4:3 image, approximately 2 megapixels (like 2048x1536)"
    ;;
  1:1)
    SIZE_DESC="square image, approximately 1 megapixel (1024x1024)"
    ;;
  *)
    # Treat as WxH
    SIZE_DESC="exactly $SIZE_KEY pixels"
    ;;
esac

PROMPT="Generate a $SIZE_DESC. Subject: $SUBJECT. Solid background with the subject centered and clearly visible. High quality, clean rendering."

echo "Generating: size=$SIZE_KEY, subject=$SUBJECT"

export http_proxy="$PROXY" https_proxy="$PROXY"

if [[ -n "$REF_IMAGE" ]]; then
  codex exec -i "$REF_IMAGE" --skip-git-repo-check -- "$PROMPT" 2>&1
else
  codex exec --skip-git-repo-check -- "$PROMPT" 2>&1
fi

latest=$(ls -t ~/.codex/generated_images/ 2>/dev/null | head -1)
if [[ -n "$latest" ]]; then
  cp ~/.codex/generated_images/$latest/*.png "$OUTDIR/output.png" 2>/dev/null
  echo "Saved to $OUTDIR/output.png"
fi