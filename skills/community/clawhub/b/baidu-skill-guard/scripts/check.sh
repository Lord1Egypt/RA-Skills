#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v node >/dev/null 2>&1; then
    node "$SCRIPT_DIR/check.js" "$@"
    exit $?
fi

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT_DIR/check.py" "$@"
else
    echo '{"code":"error","msg":"Error: Neither node nor python3 runtime was found. Please install one of them.","ts":'"$(date +%s000)"',"data":[]}'
    exit 2
fi
