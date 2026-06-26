#!/bin/bash
set -euo pipefail

TARGET_DIR="${1:-$(pwd)/book-image-redesign-app}"
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$TARGET_DIR"
cp "$SRC_DIR/assets/index.html" "$TARGET_DIR/index.html"

echo "Created: $TARGET_DIR/index.html"
echo "Next: replace __APIMART_API_KEY__ with a secure backend or env-injected value."
