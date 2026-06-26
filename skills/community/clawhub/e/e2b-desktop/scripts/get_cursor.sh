#!/usr/bin/env bash
# get_cursor.sh - Get the current mouse cursor position in the E2B Desktop sandbox
# Usage: get_cursor.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

x, y = desktop.get_cursor_position()
print(f"CURSOR_X={x}")
print(f"CURSOR_Y={y}")
EOF
