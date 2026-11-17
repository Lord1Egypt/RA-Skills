#!/usr/bin/env bash
# install-env.sh - Ensure Python venv + requirements are installed for ai-literacy-expert-v7.3 (Unix)
#
# Reads info.json and:
#   1. Finds Python >= 3.10
#   2. Creates .venv using project's skill_runtime.py (idempotent)
#   3. Installs requirements.txt with SHA256 stamp (skips if unchanged)
#   4. Verifies venv python is runnable
#
# This script is idempotent: safe to rerun.
#
# EXIT CODES
#   0  Success (venv ready)
#   1  General error (python missing / venv creation failed / pip install failed)

set -euo pipefail

# Resolve script and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR"
SCRIPTS="$ROOT/scripts"
VENV_PY="$ROOT/.venv/bin/python"

echo ""
echo "=== Environment install ====================================="

# --- 1. Verify host Python >= 3.10 ------------------------------------------
HOST_PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        VER="$("$cmd" --version 2>&1)"
        MAJ="$(echo "$VER" | grep -oP 'Python \K\d+')"
        MIN="$(echo "$VER" | grep -oP 'Python \d+\.\K\d+')"
        if [ -n "$MAJ" ] && [ -n "$MIN" ]; then
            if [ "$MAJ" -gt 3 ] || { [ "$MAJ" -eq 3 ] && [ "$MIN" -ge 10 ]; }; then
                HOST_PYTHON="$cmd"
                break
            fi
        fi
    fi
done

if [ -z "$HOST_PYTHON" ]; then
    echo "[FAIL] Host Python >= 3.10 not found."
    echo "       Install Python 3.10+ first, then rerun."
    exit 1
fi
echo "[PASS] Host Python: $("$HOST_PYTHON" --version 2>&1)"

# --- 2. Create .venv if missing (via skill_runtime for single source) -------
if [ ! -f "$VENV_PY" ]; then
    echo "[venv] Creating .venv via skill_runtime.ensure_skill_venv()..."
    "$HOST_PYTHON" -c "import sys; sys.path.insert(0, '$SCRIPTS'); from skill_runtime import ensure_skill_venv; ensure_skill_venv()"
    if [ $? -ne 0 ]; then
        echo "[FAIL] venv creation failed."
        exit 1
    fi
else
    echo "[PASS] venv exists: $VENV_PY"
fi

# --- 3. Install / refresh requirements (SHA256 stamp) -----------------------
echo "[reqs] Checking requirements.txt freshness..."
"$VENV_PY" -c "import sys; sys.path.insert(0, '$SCRIPTS'); from skill_runtime import ensure_skill_requirements; ensure_skill_requirements()"
if [ $? -ne 0 ]; then
    echo "[FAIL] requirements.txt install failed."
    exit 1
fi

# --- 4. Final sanity check ---------------------------------------------------
if [ ! -f "$VENV_PY" ]; then
    echo "[FAIL] venv python missing after install: $VENV_PY"
    exit 1
fi

echo "============================================================="
echo "[PASS] Environment ready."
echo ""
exit 0
