#!/usr/bin/env bash
# Apply the Control UI per-message token-usage badge.
# Idempotent and re-runnable after edits / `openclaw update`.
# The script tag gets a content-hash query (?v=<hash>) so the Service Worker's
# cache-first rule for /assets/ never serves a stale copy.
set -euo pipefail

UI_DIR="${OPENCLAW_CONTROL_UI_DIR:-/usr/local/lib/node_modules/openclaw/dist/control-ui}"
SRC="$(cd "$(dirname "$0")" && pwd)/../assets/oc-usage-badge.js"
ASSET="oc-usage-badge.js"

if [ ! -f "$UI_DIR/index.html" ]; then
  echo "ERROR: Control UI index.html not found at $UI_DIR" >&2
  echo "Set OPENCLAW_CONTROL_UI_DIR to your openclaw dist/control-ui path." >&2
  exit 1
fi
if [ ! -f "$SRC" ]; then
  echo "ERROR: $SRC missing" >&2
  exit 1
fi

SUDO=""
if [ ! -w "$UI_DIR" ]; then SUDO="sudo -n"; fi

HASH="$(sha256sum "$SRC" | cut -c1-12)"

if [ ! -f "$UI_DIR/index.html.oc-usage-bak" ]; then
  $SUDO cp "$UI_DIR/index.html" "$UI_DIR/index.html.oc-usage-bak"
  echo "backup: $UI_DIR/index.html.oc-usage-bak"
fi

$SUDO cp "$SRC" "$UI_DIR/assets/$ASSET"
$SUDO chmod 644 "$UI_DIR/assets/$ASSET"
echo "asset:  $UI_DIR/assets/$ASSET"

$SUDO python3 - "$UI_DIR/index.html" "$HASH" <<'PY'
import re, sys
p, h = sys.argv[1], sys.argv[2]
new_tag = '<script src="./assets/oc-usage-badge.js?v=%s"></script>' % h
s = open(p, encoding='utf-8').read()
s2 = re.sub(r'[ \t]*<script src="\./assets/oc-usage-badge\.js[^"]*"></script>\n?', '', s)
if new_tag in s2:
    print("index:  already patched")
else:
    s2 = s2.replace('</head>', '    ' + new_tag + '\n  </head>', 1)
    open(p, 'w', encoding='utf-8').write(s2)
    print("index:  patched (v=%s)" % h)
PY

echo "done. hard-refresh the Control UI tab (Ctrl+Shift+R)."
