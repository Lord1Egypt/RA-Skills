#!/usr/bin/env bash
# CLI for instagram-saved-download. ego-browser nodejs does not accept extra argv.
#   ./skills/instagram-saved-download/scripts/download.sh --count 5 --out /tmp/ig-saved
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$DIR/download.mjs" "$@"
