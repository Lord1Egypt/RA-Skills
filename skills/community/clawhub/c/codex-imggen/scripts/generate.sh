#!/bin/bash
# generate.sh — Codex image generation wrapper
# Usage: generate.sh <prompt> [output_dir] [-i <ref_image>]
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
PROMPT="${1:-}"
OUTDIR="${2:-.}"

if [[ -z "$PROMPT" ]]; then
  echo "Usage: generate.sh <prompt> [output_dir] [-i <ref_image>]"
  exit 1
fi

WORKDIR=$(mktemp -d)
cd "$WORKDIR" && git init -q
mkdir -p "$OUTDIR"

export http_proxy="$PROXY" https_proxy="$PROXY"

if [[ -n "$REF_IMAGE" ]]; then
  codex exec -i "$REF_IMAGE" --skip-git-repo-check -- "$PROMPT" 2>&1
else
  codex exec --skip-git-repo-check -- "$PROMPT" 2>&1
fi

latest=$(ls -t ~/.codex/generated_images/ 2>/dev/null | head -1)
if [[ -n "$latest" ]]; then
  cp ~/.codex/generated_images/$latest/*.png "$OUTDIR/" 2>/dev/null
  echo "Saved to $OUTDIR/"
fi