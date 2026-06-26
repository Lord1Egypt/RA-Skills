#!/usr/bin/env bash
# scroll.sh - Scroll in the E2B Desktop sandbox
# Usage: scroll.sh AMOUNT
# AMOUNT: positive = scroll up, negative = scroll down (e.g. 3 or -3)

set -e

AMOUNT="${1:?Usage: scroll.sh AMOUNT  (positive=up, negative=down)}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

amount = int("$AMOUNT")
desktop.scroll(amount)
direction = "up" if amount > 0 else "down"
print(f"Scrolled {direction} by {abs(amount)}")
EOF
