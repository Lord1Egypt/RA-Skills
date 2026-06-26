#!/bin/bash
# batch_generate.sh — Batch generate game UI assets with consistent style
# Usage: batch_generate.sh <style_prompt> <count> <output_dir> [-i <ref_image>]
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
STYLE_PROMPT="${1:-}"
COUNT="${2:-6}"
OUTDIR="${3:-.}"

if [[ -z "$STYLE_PROMPT" ]]; then
  echo "Usage: batch_generate.sh <style_prompt> <count> [output_dir] [-i <ref_image>]"
  echo "  style_prompt  - Description of the visual style (shared across all items)"
  echo "  count          - Number of items to generate (default: 6)"
  echo "  output_dir     - Output directory (default: .)"
  exit 1
fi

WORKDIR=$(mktemp -d)
cd "$WORKDIR" && git init -q
mkdir -p "$OUTDIR"

PROMPT="Generate a set of ${COUNT} game UI elements, all sharing the exact same visual style: ${STYLE_PROMPT}. Each element should be on a white background (#ffffff), with consistent lighting, consistent border thickness, and consistent padding. Generate ONE single combined image containing all ${COUNT} items arranged in a clean grid (e.g., 3x2 or 2x3 layout). Make each individual element approximately 512x512 pixels in the final combined image."

echo "Generating batch: $COUNT items, style: $STYLE_PROMPT"

export http_proxy="$PROXY" https_proxy="$PROXY"

if [[ -n "$REF_IMAGE" ]]; then
  codex exec -i "$REF_IMAGE" --skip-git-repo-check -- "$PROMPT" 2>&1
else
  codex exec --skip-git-repo-check -- "$PROMPT" 2>&1
fi

latest=$(ls -t ~/.codex/generated_images/ 2>/dev/null | head -1)
if [[ -n "$latest" ]]; then
  cp ~/.codex/generated_images/$latest/*.png "$OUTDIR/batch.png" 2>/dev/null
  echo "Batch saved to $OUTDIR/batch.png"
fi