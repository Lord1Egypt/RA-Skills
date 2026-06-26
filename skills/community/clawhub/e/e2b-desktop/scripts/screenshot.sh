#!/usr/bin/env bash
# screenshot.sh - Take a screenshot of the E2B Desktop sandbox
# Usage: screenshot.sh [OUTPUT_FILE]
# Default output: /tmp/e2b_screenshot.png

set -e

OUTPUT="${1:-/tmp/e2b_screenshot.png}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<EOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

data = desktop.screenshot()
with open("$OUTPUT", "wb") as f:
    f.write(data)
print(f"Screenshot saved to: $OUTPUT")
EOF
