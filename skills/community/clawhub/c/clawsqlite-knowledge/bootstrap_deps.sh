#!/usr/bin/env sh
set -eu

BASE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
LOCAL_TARGET="$BASE_DIR/.clawsqlite-python"
BIN_DIR="$BASE_DIR/bin"
LOCAL_CLI="$BIN_DIR/clawsqlite"
CLAWSQLITE_VERSION="1.0.12"
CLAWSQLITE_REQUIREMENT="clawsqlite==$CLAWSQLITE_VERSION"
if [ "${OPENCLAW_WORKSPACE:-}" ]; then
  DEFAULT_INSTANCE_HOME="$OPENCLAW_WORKSPACE/data/clawsqlite-knowledge/default"
elif [ "${XDG_DATA_HOME:-}" ]; then
  DEFAULT_INSTANCE_HOME="$XDG_DATA_HOME/clawsqlite-knowledge/default"
elif [ -d "$HOME/.openclaw/workspace" ]; then
  DEFAULT_INSTANCE_HOME="$HOME/.openclaw/workspace/data/clawsqlite-knowledge/default"
else
  DEFAULT_INSTANCE_HOME="$HOME/.local/share/clawsqlite-knowledge/default"
fi

if [ "${PYTHON:-}" ]; then
  PYTHON_BIN="$PYTHON"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  PYTHON_BIN=""
fi

if [ -z "$PYTHON_BIN" ] || ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "ERROR: python3 was not found." >&2
  echo "NEXT: install Python 3.10+ or set PYTHON=/path/to/python." >&2
  exit 2
fi

if ! "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
then
  echo "ERROR: Python 3.10+ is required." >&2
  echo "NEXT: install Python 3.10+ or set PYTHON=/path/to/python." >&2
  exit 2
fi

check_package_contract() {
  EXTRA_PATH="${1:-}"
  if [ -n "$EXTRA_PATH" ]; then
    PYTHONPATH="$EXTRA_PATH${PYTHONPATH:+:$PYTHONPATH}"
    export PYTHONPATH
  fi
  "$PYTHON_BIN" - <<PY >/dev/null 2>&1
from importlib import metadata
required = "$CLAWSQLITE_VERSION"
try:
    installed = metadata.version("clawsqlite")
except metadata.PackageNotFoundError:
    raise SystemExit(1)
if installed != required:
    raise SystemExit(1)
import clawsqlite_cli  # noqa: F401
raise SystemExit(0)
PY
}

INSTALL_MODE="already-satisfied"
if [ -d "$LOCAL_TARGET" ]; then
  if ! check_package_contract "$LOCAL_TARGET"; then
    INSTALL_MODE="local-target"
    rm -rf "$LOCAL_TARGET"
    "$PYTHON_BIN" -m pip install --upgrade --target "$LOCAL_TARGET" "$CLAWSQLITE_REQUIREMENT"
  fi
  PYTHONPATH="$LOCAL_TARGET${PYTHONPATH:+:$PYTHONPATH}"
  export PYTHONPATH
elif ! check_package_contract ""; then
  INSTALL_MODE="environment"
  if ! "$PYTHON_BIN" -m pip install "$CLAWSQLITE_REQUIREMENT"; then
    echo "WARN: environment install failed; falling back to local skill dependency target." >&2
    INSTALL_MODE="local-target"
    rm -rf "$LOCAL_TARGET"
    "$PYTHON_BIN" -m pip install --upgrade --target "$LOCAL_TARGET" "$CLAWSQLITE_REQUIREMENT"
    PYTHONPATH="$LOCAL_TARGET${PYTHONPATH:+:$PYTHONPATH}"
    export PYTHONPATH
  fi
fi

if ! check_package_contract ""; then
  echo "ERROR: installed clawsqlite package does not satisfy $CLAWSQLITE_REQUIREMENT." >&2
  echo "NEXT: check Python/pip output above, then rerun bootstrap_deps.sh." >&2
  exit 2
fi

if [ "$INSTALL_MODE" = "local-target" ] && [ ! -d "$LOCAL_TARGET" ]; then
  echo "ERROR: local dependency target was not created at $LOCAL_TARGET." >&2
  exit 2
fi

if [ "$INSTALL_MODE" = "local-target" ]; then
  :
elif [ "$INSTALL_MODE" = "environment" ]; then
  :
elif [ "$INSTALL_MODE" = "already-satisfied" ]; then
  :
else
  echo "ERROR: unexpected install mode: $INSTALL_MODE" >&2
  exit 2
fi

mkdir -p "$BIN_DIR"
if [ ! -f "$LOCAL_CLI" ]; then
  echo "ERROR: expected local CLI wrapper was not found at $LOCAL_CLI" >&2
  echo "NEXT: reinstall the clawsqlite-knowledge skill wrapper, then rerun bootstrap_deps.sh." >&2
  exit 2
fi
chmod +x "$LOCAL_CLI"

if ! "$LOCAL_CLI" --help >/dev/null 2>&1; then
  echo "ERROR: installed clawsqlite CLI could not execute --help." >&2
  echo "NEXT: check Python/pip output above, then rerun bootstrap_deps.sh." >&2
  exit 2
fi

"$LOCAL_CLI" knowledge --help >/dev/null
"$LOCAL_CLI" knowledge maintenance init-config --help >/dev/null

cat <<'EOF'
clawsqlite-knowledge dependencies ready.
EOF

CLAWSQLITE_CMD="$LOCAL_CLI"

cat <<EOF

Stable skill-local CLI:
  $CLAWSQLITE_CMD

NOTE: ClawHub installs only this thin skill wrapper. bootstrap_deps.sh installs
the published clawsqlite package required by this skill and prepares the stable local entry above.
The global 'clawsqlite' command may still be absent from PATH in managed Python
environments.
EOF

if [ "$INSTALL_MODE" = "local-target" ]; then
  cat <<EOF

Local dependency target:
  $LOCAL_TARGET
EOF
fi

cat <<'EOF'
Next steps:
1. Create the default knowledge instance:
EOF
cat <<EOF
   $CLAWSQLITE_CMD knowledge maintenance init-config --instance default
EOF
cat <<EOF
2. Enter the knowledge instance home:
   cd $DEFAULT_INSTANCE_HOME
   (The stable CLI also reads the default instance registry, so future commands
    can be run from any directory after initialization.)
EOF
cat <<EOF
3. Validate with:
   $CLAWSQLITE_CMD knowledge maintenance doctor --json
EOF
