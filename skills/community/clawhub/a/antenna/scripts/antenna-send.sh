#!/usr/bin/env bash
# Native transport only; no general-hooks fallback.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec node "$SCRIPT_DIR/../plugin/send.mjs" "$(dirname "$SCRIPT_DIR")" "$@"
