#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install --user -r "$(dirname "$0")/requirements.txt"
echo "[ok] Dependencies installed"
