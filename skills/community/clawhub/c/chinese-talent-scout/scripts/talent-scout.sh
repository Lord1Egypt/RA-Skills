#!/usr/bin/env bash
set -euo pipefail
if ! command -v node >/dev/null 2>&1; then
  echo "Node.js 22+ is required to run this skill." >&2
  exit 1
fi
exec node "$(dirname "$0")/talent-scout.mjs" "$@"
