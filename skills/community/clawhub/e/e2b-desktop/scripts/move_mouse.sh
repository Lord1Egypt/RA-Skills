#!/usr/bin/env bash
# move_mouse.sh - Move mouse to coordinates in the E2B Desktop sandbox
# Usage: move_mouse.sh X Y

set -e

X="${1:?Usage: move_mouse.sh X Y}"
Y="${2:?Usage: move_mouse.sh X Y}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.move_mouse(int("$X"), int("$Y"))
print(f"Mouse moved to ($X, $Y)")
EOF
