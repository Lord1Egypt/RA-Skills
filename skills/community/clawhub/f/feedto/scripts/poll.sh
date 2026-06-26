#!/bin/bash
set -euo pipefail
# FeedTo background inbox reader.
# Primary path: keep a persistent outbound realtime connection to FeedTo cloud
# and drain the local inbox written by scripts/realtime.mjs.
# Safe fallback: the daemon itself falls back to /api/feeds/pending when
# realtime is unavailable or disabled.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
API_KEY="${FEEDTO_API_KEY:-}"

if [ "${1:-}" = "--status" ]; then
  node "$SCRIPT_DIR/status.mjs"
  exit 0
fi

if [ -z "$API_KEY" ]; then
  echo "ERROR: FEEDTO_API_KEY not set."
  echo "Install the skill in OpenClaw, then paste your key when prompted."
  echo "You can also copy it from: https://feedto.ai/settings"
  exit 1
fi

node "$SCRIPT_DIR/bootstrap.mjs" >/dev/null 2>&1 || true
node "$SCRIPT_DIR/drain.mjs"
