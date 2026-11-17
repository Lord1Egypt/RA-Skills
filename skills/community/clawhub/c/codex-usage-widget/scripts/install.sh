#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/assets/codex-usage.widget"
DEST="$HOME/Library/Application Support/Übersicht/widgets/codex-usage.widget"

if [ ! -d "$SRC" ]; then
  echo "Missing widget assets: $SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
chmod +x "$DEST/codex-usage.py"

python3 -m py_compile "$DEST/codex-usage.py"
echo "Installed Codex usage widget to: $DEST"
echo "Refresh Übersicht if the widget does not appear automatically."
