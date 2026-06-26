#!/usr/bin/env bash
# Prepare /tmp/oganim-test/ for headless verification probes.
# Idempotent — safe to re-run.
set -euo pipefail

DIR="/tmp/oganim-test"
mkdir -p "$DIR"
cd "$DIR"

# Initialize an npm scratch project if needed
if [ ! -f package.json ]; then
  npm init -y >/dev/null
fi

# Install playwright if not already present
if [ ! -d node_modules/playwright ]; then
  echo "Installing playwright (no-save) ..."
  npm i playwright --no-save 2>&1 | tail -3
fi

# Match the cached Chromium revision so we don't have to download again.
# Playwright pins via the package version; we keep an alias to whichever
# revision is currently on disk under ~/.cache/ms-playwright/.
PW_CACHE="$HOME/.cache/ms-playwright"
if [ -d "$PW_CACHE" ]; then
  for dir in "$PW_CACHE"/chromium_headless_shell-*; do
    [ -d "$dir" ] || continue
    LATEST="$dir"
  done
  if [ -n "${LATEST:-}" ]; then
    # Symlink any "expected" rev names to the one we actually have.
    for rev in 1217 1223 1224 1225 1230; do
      TARGET="$PW_CACHE/chromium_headless_shell-$rev"
      [ -e "$TARGET" ] && continue
      ln -sfn "$LATEST" "$TARGET"
    done
    echo "Symlinked Playwright Chromium aliases → $(basename "$LATEST")"
  fi
fi

echo "Ready. Probes can now require('playwright') from $DIR."
