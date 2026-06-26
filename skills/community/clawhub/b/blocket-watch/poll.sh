#!/usr/bin/env bash
# Scheduled poll: blocket + dedupe + Telegram. No LLM.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
exec python3 "$DIR/poll.py" "$@"
