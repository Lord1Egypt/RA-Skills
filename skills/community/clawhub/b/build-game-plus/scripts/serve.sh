#!/usr/bin/env bash
# serve.sh <dir> — serve a game directory locally on the next free port.
DIR="${1:?usage: serve.sh <dir>}"
PORT="${2:-$((8000 + RANDOM % 1000))}"
cd "$DIR" || exit 1
if command -v python3 >/dev/null; then
  echo "http://localhost:$PORT"
  exec python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1
else
  echo "no python3 found" >&2; exit 1
fi
