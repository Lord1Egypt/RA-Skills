#!/usr/bin/env bash
# get_screen_size.sh - Get the screen resolution of the E2B Desktop sandbox
# Usage: get_screen_size.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

w, h = desktop.get_screen_size()
print(f"SCREEN_WIDTH={w}")
print(f"SCREEN_HEIGHT={h}")
EOF
