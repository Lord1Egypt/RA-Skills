#!/usr/bin/env bash
# Quick status check for the Control UI usage badge.
set -uo pipefail

UI_DIR="${OPENCLAW_CONTROL_UI_DIR:-/usr/local/lib/node_modules/openclaw/dist/control-ui}"
ASSET="oc-usage-badge.js"

echo "UI dir : $UI_DIR"
[ -d "$UI_DIR" ] || { echo "STATUS : MISSING (Control UI dir not found)"; exit 1; }

if grep -q 'assets/oc-usage-badge.js' "$UI_DIR/index.html" 2>/dev/null; then
  tag="$(grep -o 'assets/oc-usage-badge\.js[^"]*' "$UI_DIR/index.html" | head -1)"
  echo "index  : PATCHED ($tag)"
else
  echo "index  : NOT PATCHED"
fi

if [ -f "$UI_DIR/assets/$ASSET" ]; then
  echo "asset  : present ($(wc -c < "$UI_DIR/assets/$ASSET") bytes)"
else
  echo "asset  : MISSING"
fi

if command -v openclaw >/dev/null 2>&1; then
  echo "version: $(openclaw --version 2>/dev/null | head -1)"
fi

echo
echo "If NOT PATCHED (e.g. after 'openclaw update'), run:  bash \"$(dirname "$0")/apply.sh\""
