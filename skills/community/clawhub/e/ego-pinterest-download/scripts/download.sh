#!/usr/bin/env bash
# CLI for pinterest-download. ego-browser nodejs does not accept extra argv,
# so this wrapper parses query/count/out and the .mjs file inlines them.
#
#   ./skills/pinterest-download/scripts/download.sh --query wallpaper --count 2 --out /tmp/ego-pinterest-wallpaper
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$DIR/download.mjs" "$@"
