#!/usr/bin/env bash
set -euo pipefail

has() { command -v "$1" >/dev/null 2>&1; }

if has codex; then
  echo "preferred_runner=codex"
  exit 0
fi

if has claude; then
  echo "preferred_runner=claude"
  exit 0
fi

echo "preferred_runner=api"
