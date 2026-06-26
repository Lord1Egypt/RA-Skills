#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SKILL_DIR"

if [ ! -f "dist/index.js" ]; then
  echo "dist/index.js was not found. Build the skill before packaging." >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js was not found. This skill requires Node.js >= 18 to run." >&2
  exit 1
fi

node dist/index.js "$@"
