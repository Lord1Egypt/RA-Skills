#!/bin/bash
# Inject OAuth token into a Colab script and run it.
# Usage: inject_and_run.sh <script.py> [--gpu T4] [extra colab_run args...]
set -euo pipefail

SCRIPT="$1"
shift

if [ ! -f "$SCRIPT" ]; then
    echo "Error: $SCRIPT not found" >&2
    exit 1
fi

TOKEN_B64=$(python3 -c "
import base64, os
with open(os.path.expanduser('~/.colab-mcp-auth-token.json')) as f:
    print(base64.b64encode(f.read().encode()).decode())
")

# Create temp script with token injected (restricted permissions)
TMPSCRIPT=$(mktemp /tmp/colab_XXXXX.py)
chmod 600 "$TMPSCRIPT"

# Always clean up the token-bearing temp file
cleanup() { rm -f "$TMPSCRIPT"; }
trap cleanup EXIT INT TERM

sed "s|__COLAB_TOKEN_PLACEHOLDER__|${TOKEN_B64}|" "$SCRIPT" > "$TMPSCRIPT"

# Run on Colab
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/colab_run.py" exec --file "$TMPSCRIPT" "$@"
