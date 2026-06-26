#!/usr/bin/env bash
set -euo pipefail

# Bootstrap script for clawfeedradar skill.
#
# This installs the upstream `clawfeedradar` Python package either into
# the default Python environment or into a workspace-local prefix when
# the default venv is not writable.

REQ="clawfeedradar>=0.1.0"
WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PREFIX="$WORKSPACE/skills/clawfeedradar/.venv"

echo "[clawfeedradar] installing/upgrading $REQ via pip..." >&2
if python -m pip install --upgrade "$REQ"; then
  echo "NEXT: clawfeedradar installed into the default Python environment." >&2
  echo "NEXT: the skill runtime will import 'clawfeedradar.cli' via python -m." >&2
  exit 0
fi

echo "[clawfeedradar] default env pip install failed, trying workspace prefix..." >&2
mkdir -p "$PREFIX"
if python -m pip install --upgrade "$REQ" --prefix "$PREFIX"; then
  PURELIB=$(python - << 'EOF'
import sysconfig, pathlib, os
p = pathlib.Path("'$PREFIX'")
vars_map = {"base": str(p), "platbase": str(p)}
print(sysconfig.get_path("purelib", vars=vars_map))
EOF
)
  echo "NEXT: clawfeedradar installed into workspace prefix: $PREFIX" >&2
  echo "NEXT: ensure PYTHONPATH includes: $PURELIB" >&2
  exit 0
fi

echo "ERROR: failed to install $REQ in both default env and workspace prefix." >&2
exit 1
