#!/usr/bin/env bash
set -euo pipefail

# Legacy compatibility wrapper.
# The real cache refresh implementation now lives in the Node CLI:
#   aqara devices cache refresh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: Required command 'node' was not found in PATH." >&2
  exit 1
fi

exec node "$SKILL_ROOT/bin/aqara-open-api.js" devices cache refresh "$@"
