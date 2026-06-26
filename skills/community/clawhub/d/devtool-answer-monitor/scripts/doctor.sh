#!/usr/bin/env bash
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok() { echo -e "${GREEN}OK${NC}  $1"; }
warn() { echo -e "${YELLOW}WARN${NC} $1"; }
err() { echo -e "${RED}ERR${NC}  $1"; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON:-python3}"
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT/.venv/bin/python"
fi

echo "== DevTool Answer Monitor Doctor =="
echo "repo: $ROOT"
echo

for cmd in git python3; do
  if command -v "$cmd" >/dev/null 2>&1; then
    ok "found $cmd"
  else
    err "missing $cmd. Please install it first, then rerun 'make doctor'."
    exit 1
  fi
done

PY_VER="$($PYTHON_BIN - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)"
ok "python version ${PY_VER}"

required=(
  "README.md"
  "requirements.txt"
  "install.sh"
  "quickstart.sh"
  "docs/for-beginners.md"
  "docs/metric-definition.md"
  "data/query-pools/mineru-example.json"
  "data/models.sample.json"
  "data/models.multi.sample.json"
  "data/manual.sample.json"
  "data/manual.multi.sample.json"
  "data/runs/sample-run/summary.json"
  "scripts/run_monitor.py"
  "scripts/validate_data.py"
  "scripts/generate_weekly_report.py"
)

for file in "${required[@]}"; do
  if [[ -f "$file" ]]; then
    ok "found $file"
  else
    err "missing $file. Please pull the latest repository version and rerun."
    exit 1
  fi
done

missing_mods="$($PYTHON_BIN - <<'PY'
import importlib.util
mods = ["jsonschema", "matplotlib", "openai"]
missing = [m for m in mods if importlib.util.find_spec(m) is None]
print(",".join(missing))
PY
)"
if [[ -n "$missing_mods" ]]; then
  err "missing Python packages: $missing_mods"
  echo "fix: bash install.sh"
  exit 1
else
  ok "core Python packages look ready"
fi

if "$PYTHON_BIN" scripts/validate_data.py --repo-root . >/dev/null 2>&1; then
  ok "sample files and summaries passed validation"
else
  err "validation failed. Run: $PYTHON_BIN scripts/validate_data.py --repo-root ."
  exit 1
fi

if mkdir -p data/runs/_doctor assets >/dev/null 2>&1; then
  ok "output directories are writable"
else
  err "cannot write to data/runs or assets"
  exit 1
fi

echo
ok "doctor completed"
echo "next:"
echo "  1) bash quickstart.sh"
echo "  2) open docs/for-beginners.md"
