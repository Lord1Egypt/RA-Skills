#!/usr/bin/env bash
# Check all dependencies required by project-tunnel.sh
# Exit 0 = all OK, Exit 1 = something missing (prints what's missing)

MISSING=()

check_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    MISSING+=("$cmd")
  fi
}

# Required tools
check_cmd curl
check_cmd node
check_cmd npm
check_cmd lsof

# Python: accept python3 or python (Python 3 only)
if command -v python3 >/dev/null 2>&1; then
  PYTHON_OK=true
elif command -v python >/dev/null 2>&1 && python -c "import sys; assert sys.version_info[0]==3" 2>/dev/null; then
  PYTHON_OK=true
else
  PYTHON_OK=false
  MISSING+=("python3")
fi

if [[ ${#MISSING[@]} -eq 0 ]]; then
  echo "✅ environment OK"
  exit 0
else
  echo "❌ missing: ${MISSING[*]}"
  exit 1
fi
