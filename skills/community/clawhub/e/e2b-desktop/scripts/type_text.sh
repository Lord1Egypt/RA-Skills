#!/usr/bin/env bash
# type_text.sh - Type text at the current cursor position in the E2B Desktop sandbox
# Usage: type_text.sh "text to type"

set -e

TEXT="${1:?Usage: type_text.sh \"text to type\"}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<PYEOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

text = """$TEXT"""
desktop.write(text)
print(f"Typed: {repr(text)}")
PYEOF
