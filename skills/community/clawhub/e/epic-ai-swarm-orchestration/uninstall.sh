#!/usr/bin/env bash
# Safely remove an Epic AI Swarm Orchestration runtime install.

set -euo pipefail

TARGET_DIR="${SWARM_TARGET_DIR:-$HOME/workspace/swarm}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
YES=0
KEEP_ROLE=0

usage() {
  cat <<'EOF'
Usage: bash uninstall.sh [options]

Options:
  --target <dir>       Runtime install directory (default: ~/workspace/swarm)
  --workspace <dir>    OpenClaw workspace (default: ~/.openclaw/workspace)
  --yes               Actually remove files (default is preview only)
  --keep-role          Do not remove/deactivate roles/swarm-lead
  -h, --help          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET_DIR="${2:?--target requires a directory}"; shift 2 ;;
    --workspace) WORKSPACE_DIR="${2:?--workspace requires a directory}"; shift 2 ;;
    --yes) YES=1; shift ;;
    --keep-role) KEEP_ROLE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

TARGET_DIR="$(python3 - "$TARGET_DIR" <<'PY'
import os, sys
print(os.path.abspath(os.path.expanduser(sys.argv[1])))
PY
)"
WORKSPACE_DIR="$(python3 - "$WORKSPACE_DIR" <<'PY'
import os, sys
print(os.path.abspath(os.path.expanduser(sys.argv[1])))
PY
)"

run() {
  if [[ "$YES" != "1" ]]; then
    printf '[preview]'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

printf '🐝 Epic AI Swarm uninstall\n'
printf '  Runtime:   %s\n' "$TARGET_DIR"
printf '  Workspace: %s\n' "$WORKSPACE_DIR"

if tmux ls >/tmp/swarm-uninstall-tmux.log 2>&1 && grep -qE '^(claude|codex|gemini|deepseek)-' /tmp/swarm-uninstall-tmux.log; then
  echo "Refusing to uninstall while swarm tmux sessions are running:" >&2
  grep -E '^(claude|codex|gemini|deepseek)-' /tmp/swarm-uninstall-tmux.log >&2
  exit 1
fi

if [[ -e "$TARGET_DIR" || -L "$TARGET_DIR" ]]; then
  run rm -rf "$TARGET_DIR"
else
  echo "Runtime directory not found; nothing to remove."
fi

if [[ "$KEEP_ROLE" != "1" ]]; then
  if [[ -d "$WORKSPACE_DIR/roles/swarm-lead" ]]; then
    run rm -rf "$WORKSPACE_DIR/roles/swarm-lead"
  fi
  if [[ -f "$WORKSPACE_DIR/roles/active.json" ]]; then
    if [[ "$YES" != "1" ]]; then
      echo "[preview] remove swarm-lead from $WORKSPACE_DIR/roles/active.json"
    else
      cp -a "$WORKSPACE_DIR/roles/active.json" "$WORKSPACE_DIR/roles/active.json.bak-$(date +%Y%m%d-%H%M%S)"
      python3 - "$WORKSPACE_DIR/roles/active.json" <<'PY'
import datetime, json, sys
path = sys.argv[1]
with open(path) as f: data = json.load(f)
roles = [r for r in data.get('activeRoles', []) if r != 'swarm-lead']
data['activeRoles'] = roles
data['updatedAt'] = datetime.date.today().isoformat()
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
PY
    fi
  fi
fi

if [[ "$YES" != "1" ]]; then
  echo ""
  echo "Preview only. Re-run with --yes to remove."
else
  echo ""
  echo "✅ Uninstall complete."
fi
