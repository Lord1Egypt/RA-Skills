#!/bin/bash
# Weekly internship report generator.

set -euo pipefail

export PATH="/usr/bin:/bin:/usr/local/bin:/home/linuxbrew/.linuxbrew/bin:${PATH:-}"
export HOME="${HOME:-/root}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$DAILY_DIR")"
export OPENCLAW_WORKSPACE="$WORKSPACE"

CONFIG_FILE="$DAILY_DIR/.env"
if [ -f "$CONFIG_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$CONFIG_FILE"
    set +a
fi

exec node "$SCRIPT_DIR/generate-weekly-report.js" "$@"
