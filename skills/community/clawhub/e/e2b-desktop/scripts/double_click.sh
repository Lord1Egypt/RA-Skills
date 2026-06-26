#!/usr/bin/env bash
# double_click.sh - Double click at coordinates in the E2B Desktop sandbox
# Usage: double_click.sh X Y

set -e

X="${1:?Usage: double_click.sh X Y}"
Y="${2:?Usage: double_click.sh X Y}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

desktop.double_click(int("$X"), int("$Y"))
print(f"Double clicked at ($X, $Y)")
EOF
