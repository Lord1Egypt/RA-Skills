#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

if [ -f "$SKILL_DIR/.env.local" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$SKILL_DIR/.env.local"
  set +a
fi

exec python3 "$SCRIPT_DIR/gemini_smart_search.py" "$@"
