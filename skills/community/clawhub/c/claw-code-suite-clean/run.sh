#!/bin/bash
# OpenClaw skill wrapper for Claw Code master harness
# Uses enhanced harness with full command set support

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER_PY="$SCRIPT_DIR/scripts/claw_wrapper_enhanced.py"
FALLBACK_WRAPPER="$SCRIPT_DIR/scripts/claw_wrapper.py"

if [[ ! -f "$WRAPPER_PY" ]]; then
    if [[ ! -f "$FALLBACK_WRAPPER" ]]; then
        echo "❌ Python wrapper not found: $WRAPPER_PY" >&2
        exit 1
    fi
    echo "⚠️  Using fallback wrapper (limited commands)" >&2
    WRAPPER_PY="$FALLBACK_WRAPPER"
fi

exec python3 "$WRAPPER_PY" "$@"