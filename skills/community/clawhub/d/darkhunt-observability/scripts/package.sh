#!/usr/bin/env bash
set -euo pipefail

# Build and package the plugin for ClawHub upload
# Usage: ./scripts/package.sh [--no-deps]
#
# By default bundles production node_modules so users need zero setup.
# Use --no-deps for a slim zip (requires npm install after extraction).

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

BUNDLE_DEPS=true
if [[ "${1:-}" == "--no-deps" ]]; then
  BUNDLE_DEPS=false
fi

# Read id and version from openclaw.plugin.json
PLUGIN_ID=$(node -e "console.log(require('./openclaw.plugin.json').id)")
VERSION=$(node -e "console.log(require('./openclaw.plugin.json').version)")
OUT="${PLUGIN_ID}-${VERSION}.zip"

echo "==> Building TypeScript..."
npm run build

echo "==> Running tests..."
npm test

# Install production-only deps in a temp dir to avoid polluting dev node_modules
if $BUNDLE_DEPS; then
  echo "==> Installing production dependencies..."
  STAGING=$(mktemp -d)
  cp package.json package-lock.json "$STAGING/"
  (cd "$STAGING" && npm ci --omit=dev --silent 2>&1)
fi

echo "==> Packaging ${OUT}..."
rm -f "$OUT"

zip -r "$OUT" \
  openclaw.plugin.json \
  package.json \
  package-lock.json \
  index.ts \
  README.md \
  SKILL.md \
  setup-plugin.sh \
  dist/ \
  src/ \
  -x "**/.DS_Store"

# Add production node_modules from staging
if $BUNDLE_DEPS; then
  (cd "$STAGING" && zip -r "$ROOT/$OUT" node_modules/ -x \
    "**/.DS_Store" \
    "**/LICENSE" "**/LICENSE.*" \
    "**/.npmignore" \
    "**/*.jsdoc" \
    "**/*.proto" \
    "**/*.map" \
    "**/*.min.js" \
    -q)
  rm -rf "$STAGING"
fi

echo ""
echo "==> Done: ${OUT} ($(du -h "$OUT" | cut -f1))"
echo "   Files: $(unzip -l "$OUT" | tail -1)"
if $BUNDLE_DEPS; then
  echo "   (includes node_modules — ready to install)"
else
  echo "   (no node_modules — user must run: npm install --omit=dev)"
fi
