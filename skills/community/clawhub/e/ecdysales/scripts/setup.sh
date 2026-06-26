#!/bin/bash
# Ecdysales Lite — Setup
# Checks deps, makes scripts executable, verifies everything works.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LITE_DIR="${SCRIPT_DIR}/.."

echo "🏷️  Ecdysales Lite — Setup"
echo ""

# Make scripts executable
chmod +x "${SCRIPT_DIR}/run.sh" "${SCRIPT_DIR}/make-product.sh" "${SCRIPT_DIR}/setup.sh"
echo "✅ Scripts marked executable"

# Check dependencies
MISSING=()

check_cmd() {
  if command -v "$1" &>/dev/null; then
    echo "✅ $1 — $(command -v "$1")"
    return 0
  else
    echo "❌ $1 — not found ($2)"
    MISSING+=("$1")
    return 1
  fi
}

echo ""
echo "🔍 Checking dependencies..."

# ImageMagick — check for v6 (convert/identify) or v7 (magick)
if command -v convert &>/dev/null && command -v identify &>/dev/null; then
  echo "✅ ImageMagick (v6) — $(command -v convert)"
elif command -v magick &>/dev/null; then
  echo "✅ ImageMagick (v7) — $(command -v magick)"
  echo "   ⚠️  ImageMagick 7 detected — scripts use v6 commands (convert/identify)"
  echo "   You may need: alias convert='magick' alias identify='magick identify'"
else
  echo "❌ ImageMagick — not found"
  MISSING+=("imagemagick")
fi

check_cmd bc "float math"
check_cmd python3 "config validation"

# Check assets
echo ""
echo "📦 Checking assets..."
for asset in watermark-pattern.png logo.png; do
  if [ -f "${LITE_DIR}/assets/${asset}" ]; then
    echo "✅ ${asset}"
  else
    echo "❌ ${asset} — missing from assets/"
  fi
done

# Create output dir with .gitkeep
mkdir -p "${LITE_DIR}/output"
touch "${LITE_DIR}/output/.gitkeep"
echo "✅ output/ directory ready"

echo ""

if [ ${#MISSING[@]} -eq 0 ]; then
  echo "🎉 Ecdysales Lite is ready!"
  echo ""
  echo "Quick test:"
  echo "  ${SCRIPT_DIR}/run.sh <some_image.jpg> '\$999'"
  exit 0
fi

echo "Missing: ${MISSING[*]}"
echo ""

if [[ "${1:-}" == "--install" ]]; then
  echo "📦 Installing..."
  if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y imagemagick bc python3
  elif command -v dnf &>/dev/null; then
    sudo dnf install -y ImageMagick bc python3
  elif command -v pacman &>/dev/null; then
    sudo pacman -S --noconfirm imagemagick bc python3
  elif command -v brew &>/dev/null; then
    brew install imagemagick bc python3
  else
    echo "⚠️  Unknown package manager. Install manually:"
    echo "   imagemagick bc python3"
    exit 1
  fi
  echo "✅ Done! Run setup again to verify."
else
  echo "Run with --install to auto-install:"
  echo "  ${SCRIPT_DIR}/setup.sh --install"
fi
