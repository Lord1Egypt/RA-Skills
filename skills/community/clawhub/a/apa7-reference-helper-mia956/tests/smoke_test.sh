#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
python3 scripts/apa7_quick_check.py examples/demo_references.txt >/tmp/apa7_reference_helper_smoke.txt
if ! grep -q "Checked 3 reference" /tmp/apa7_reference_helper_smoke.txt; then
  echo "Smoke test failed" >&2
  exit 1
fi
echo "apa7-reference-helper smoke test passed"
