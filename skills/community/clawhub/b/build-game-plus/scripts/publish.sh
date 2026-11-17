#!/usr/bin/env bash
# publish.sh <dir> — make a built game reachable from the public web via the
# existing Cloudflare tunnel on this host (https://jerithai.com).
#
# Copies the game into /var/www/jerithai/games/<slug>/ and prints the public
# URL + the local path for iteration. Permanent, no external service needed.
set -euo pipefail

DIR="${1:?usage: publish.sh <game-dir> [slug]}"
SLUG="${2:-}"
# derive slug from progress.md title or dir name
if [[ -z "$SLUG" ]]; then
  if [[ -f "$DIR/progress.md" ]]; then
    SLUG=$(head -1 "$DIR/progress.md" | sed 's/^# *//; s/[^a-zA-Z0-9]/-/g; s/-\+$//; s/^-//' | tr 'A-Z' 'a-z' | cut -c1-40)
  fi
  [[ -z "$SLUG" ]] && SLUG=$(basename "$DIR")
fi
SLUG=$(echo "$SLUG" | tr -cd 'a-z0-9-')

WEBROOT=/var/www/jerithai/games
TARGET="$WEBROOT/$SLUG"
mkdir -p "$TARGET"
# copy game files (index.html + any assets), never progress.md/verify artifacts
rsync -a --exclude 'progress.md' --exclude 'report.json' --exclude '*.png' "$DIR"/ "$TARGET"/
echo "local : http://localhost/ (served by nginx if you put it in webroot directly)"
echo "public: https://jerithai.com/games/$SLUG/"
echo "path  : $TARGET"
