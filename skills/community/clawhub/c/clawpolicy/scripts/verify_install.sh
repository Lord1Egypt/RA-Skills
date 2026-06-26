#!/usr/bin/env bash
set -euo pipefail

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

python3 -m venv "$TMPDIR/venv"
source "$TMPDIR/venv/bin/activate"
python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install clawpolicy >/dev/null

clawpolicy --help >/dev/null
cd "$TMPDIR"
clawpolicy init >/dev/null
clawpolicy policy status >/dev/null
python -m clawpolicy policy status >/dev/null

echo "VERIFY_OK"
