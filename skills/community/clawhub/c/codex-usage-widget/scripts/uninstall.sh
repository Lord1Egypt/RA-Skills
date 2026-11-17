#!/usr/bin/env bash
set -euo pipefail

DEST="$HOME/Library/Application Support/Übersicht/widgets/codex-usage.widget"

if [ -d "$DEST" ]; then
  rm -rf "$DEST"
  echo "Removed: $DEST"
else
  echo "Widget is not installed at: $DEST"
fi
