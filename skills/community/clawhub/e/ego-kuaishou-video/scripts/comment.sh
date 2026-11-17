#!/usr/bin/env bash
# Write /tmp/kuaishou-video-comment.json, then run comment.js inside ego-browser.
# usage: comment.sh <comment> [title-hint] [spaceId] [keep=1]
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
node "$DIR/write-comment-config.mjs" "$@" >/dev/null
exec node "$DIR/run-ego-module.mjs" "$DIR/comment.js" comment
