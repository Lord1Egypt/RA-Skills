#!/usr/bin/env bash
# Setup script for excalidraw-render skill.
# Run once before first use to build the local Excalidraw bundle.
# Usage: bash setup.sh

set -e
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Building local Excalidraw bundle..."

# Install esbuild and excalidraw in a temp dir, then bundle
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cd "$TMP"
npm init -y > /dev/null
npm install @excalidraw/excalidraw esbuild --save-dev > /dev/null 2>&1

npx esbuild node_modules/@excalidraw/excalidraw/dist/prod/index.js \
  --bundle \
  --format=iife \
  --global-name=ExcalidrawLib \
  --minify \
  --outfile="$SKILL_DIR/excalidraw.iife.js" 2>&1

echo "Done. Bundle written to: $SKILL_DIR/excalidraw.iife.js"

# Install excalidraw-cli locally so it doesn't need npx at runtime
echo "Installing @swiftlysingh/excalidraw-cli..."
npm install -g @swiftlysingh/excalidraw-cli > /dev/null 2>&1 || \
  npm install --prefix "$SKILL_DIR/.npm" @swiftlysingh/excalidraw-cli > /dev/null 2>&1
echo "Done."
echo "Now run: cd $SKILL_DIR && uv sync && uv run playwright install chromium"
