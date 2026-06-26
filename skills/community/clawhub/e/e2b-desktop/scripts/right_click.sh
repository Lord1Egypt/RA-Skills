#!/usr/bin/env bash
# right_click.sh - Right click at coordinates in the E2B Desktop sandbox
# Usage: right_click.sh X Y

set -e

X="${1:?Usage: right_click.sh X Y}"
Y="${2:?Usage: right_click.sh X Y}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.right_click(int("$X"), int("$Y"))
print(f"Right clicked at ($X, $Y)")
EOF
