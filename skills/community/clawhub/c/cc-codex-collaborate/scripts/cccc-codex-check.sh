#!/usr/bin/env bash
# Check Codex CLI availability before running reviews.
# If unavailable, pause the skill and exit non-zero.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

ROOT="$(cccc_repo_root)"
cd "$ROOT"

CONFIG="docs/cccc/config.json"
STATE="docs/cccc/state.json"

# Read CLI command from config
CLI_CMD="codex"
if [[ -f "$CONFIG" ]]; then
  CLI_CMD="$(jq -r '.codex.cli_command // "codex"' "$CONFIG" 2>/dev/null || echo "codex")"
fi

# Check if command exists
if ! command -v "$CLI_CMD" >/dev/null 2>&1; then
  echo "ERROR: Codex CLI not found: $CLI_CMD" >&2
  echo "Install or configure Codex before continuing." >&2

  # Update state to paused
  if [[ -f "$STATE" ]]; then
    python3 - "$STATE" "$CLI_CMD" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
try:
    data = json.loads(p.read_text())
except Exception:
    data = {}
data['status'] = 'PAUSED_FOR_CODEX'
data['codex_unavailable_reason'] = f"Codex CLI not found: {sys.argv[2]}. Install or configure Codex before continuing."
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
PY
  fi

  exit 1
fi

# Try to get version info
VERSION_INFO=""
if "$CLI_CMD" --version >/dev/null 2>&1; then
  VERSION_INFO="$("$CLI_CMD" --version 2>/dev/null || echo 'unknown')"
fi

CLI_PATH="$(command -v "$CLI_CMD")"
echo "Codex CLI available: $CLI_PATH"
if [[ -n "$VERSION_INFO" ]]; then
  echo "Version: $VERSION_INFO"
fi

exit 0