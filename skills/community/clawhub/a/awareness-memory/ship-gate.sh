#!/usr/bin/env bash
# awareness-memory (ClawHub skill) ship-gate.
# No package.json — this is a SKILL.md + scripts bundle.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$HERE"

banner() { printf "\n\033[1;34m==== %s ====\033[0m\n" "$1"; }

banner "L1 · Syntax check scripts/"
for f in scripts/*.js; do node -c "$f"; done
echo "  OK — $(ls scripts/*.js 2>/dev/null | wc -l | tr -d ' ') js scripts parse"

banner "L1 · SSOT consistency (F-036)"
( cd "$HERE/../.." && bash scripts/sync-shared-scripts.sh --check )

banner "L1 · SKILL.md sanity"
grep -q "^name:" SKILL.md || { echo "SKILL.md missing name" >&2; exit 1; }
grep -q "^description:" SKILL.md || { echo "SKILL.md missing description" >&2; exit 1; }
echo "  OK"

banner "L2 · Integration test (from main repo if available)"
if [ -f "../../backend/tests/test_device_auth.py" ]; then
  echo "  [skip] backend tests run in main ship-gate"
fi

banner "✅ awareness-memory ship-gate PASS"
