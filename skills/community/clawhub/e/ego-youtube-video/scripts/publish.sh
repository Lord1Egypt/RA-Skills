#!/usr/bin/env bash
# Write /tmp/youtube-video-publish.json, then run publish.js inside ego-browser.
# ego's embedded Node does not inherit shell environment variables.
# usage: publish.sh <video> <title> [description] [--visibility private] [--tags a,b] [--keep]
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
node "$DIR/write-publish-config.mjs" "$@" >/dev/null
exec node "$DIR/run-ego-module.mjs" "$DIR/publish.js" publish
