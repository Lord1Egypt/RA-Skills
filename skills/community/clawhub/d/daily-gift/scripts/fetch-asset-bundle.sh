#!/bin/bash
set -euo pipefail

# Usage: fetch-asset-bundle.sh <bundle-key> [base-dir] [manifest-path]
# Example: fetch-asset-bundle.sh "image-examples/meme-sticker" "/path/to/repo"
# Prints the extracted target directory on success.

BUNDLE_KEY="${1:-}"
BASE_DIR="${2:-}"
MANIFEST_PATH="${3:-}"

if [ -z "$BUNDLE_KEY" ]; then
  echo "Usage: fetch-asset-bundle.sh <bundle-key> [base-dir] [manifest-path]" >&2
  exit 1
fi

if [ -z "$BASE_DIR" ]; then
  BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
fi

if [ -z "$MANIFEST_PATH" ]; then
  MANIFEST_PATH="$BASE_DIR/references/asset-manifest.json"
fi

if [ ! -f "$MANIFEST_PATH" ]; then
  echo "asset manifest not found: $MANIFEST_PATH" >&2
  exit 1
fi

bundle_url="$(python3 - "$MANIFEST_PATH" "$BUNDLE_KEY" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(manifest.get(sys.argv[2], ""))
PY
)"

if [ -z "$bundle_url" ]; then
  echo "bundle key not found in manifest: $BUNDLE_KEY" >&2
  exit 1
fi

target_dir=""
case "$BUNDLE_KEY" in
  audio)
    target_dir="$BASE_DIR/assets/audio"
    ;;
  image-examples/*|video-examples/*)
    target_dir="$BASE_DIR/assets/examples/$BUNDLE_KEY"
    ;;
  examples/*)
    target_dir="$BASE_DIR/assets/$BUNDLE_KEY"
    ;;
  *)
    echo "unsupported bundle key: $BUNDLE_KEY" >&2
    exit 1
    ;;
esac

if [ -d "$target_dir" ] && [ -n "$(ls -A "$target_dir" 2>/dev/null || true)" ]; then
  printf '%s\n' "$target_dir"
  exit 0
fi

mkdir -p "$target_dir"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
zip_path="$tmpdir/bundle.zip"

case "$bundle_url" in
  http://*|https://*)
    curl -fsSL "$bundle_url" -o "$zip_path"
    ;;
  *)
    cp "$bundle_url" "$zip_path"
    ;;
esac

unzip -oq "$zip_path" -d "$target_dir"
printf '%s\n' "$target_dir"
