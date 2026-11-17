#!/usr/bin/env bash
# Remove the Control UI per-message token-usage badge.
set -euo pipefail

UI_DIR="${OPENCLAW_CONTROL_UI_DIR:-/usr/local/lib/node_modules/openclaw/dist/control-ui}"
ASSET="oc-usage-badge.js"

if [ ! -f "$UI_DIR/index.html" ]; then
  echo "ERROR: Control UI index.html not found at $UI_DIR" >&2
  exit 1
fi

SUDO=""
if [ ! -w "$UI_DIR" ]; then SUDO="sudo -n"; fi

if [ -f "$UI_DIR/index.html.oc-usage-bak" ]; then
  $SUDO cp "$UI_DIR/index.html.oc-usage-bak" "$UI_DIR/index.html"
  echo "index:  restored from backup"
else
  $SUDO python3 - "$UI_DIR/index.html" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
s = re.sub(r'[ \t]*<script src="\./assets/oc-usage-badge\.js[^"]*"></script>\n?', '', s)
open(p, 'w', encoding='utf-8').write(s)
print("index:  tag removed")
PY
fi

$SUDO rm -f "$UI_DIR/assets/$ASSET"
echo "asset:  removed"
echo "done. hard-refresh the Control UI tab."
