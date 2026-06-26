#!/bin/bash
set -euo pipefail

TARGET_DIR="${1:-$(pwd)/book-image-redesign-static}"
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$TARGET_DIR"
cp "$SRC_DIR/assets/index.html" "$TARGET_DIR/index.html"
cp "$SRC_DIR/assets/vercel.json" "$TARGET_DIR/vercel.json"

echo "Static site exported to: $TARGET_DIR"
echo "Files:"
echo "  - $TARGET_DIR/index.html"
echo "  - $TARGET_DIR/vercel.json"
echo
echo "Deploy options:"
echo "1) Vercel: import this folder or run 'vercel' inside it"
echo "2) Any static host: upload index.html"
