#!/usr/bin/env bash
# Install Epic AI Swarm Orchestration into an OpenClaw host.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
TARGET_DIR="${SWARM_TARGET_DIR:-$HOME/workspace/swarm}"
WORKSPACE_DIR="${OPENCLAW_WORKSPACE:-}"
FORCE=0
DRY_RUN=0
NO_ROLE=0
NO_ACTIVATE=0

usage() {
  cat <<'EOF'
Usage: bash install.sh [options]

Options:
  --target <dir>       Runtime install directory (default: ~/workspace/swarm)
  --workspace <dir>    OpenClaw workspace (default: infer, then ~/.openclaw/workspace)
  --force             Overwrite config/state templates after backing them up
  --no-role           Do not install roles/swarm-lead into the OpenClaw workspace
  --no-activate       Install role files but do not add swarm-lead to roles/active.json
  --dry-run           Print what would change
  -h, --help          Show this help

Environment overrides:
  SWARM_TARGET_DIR, OPENCLAW_WORKSPACE, SWARM_NOTIFY_TARGET,
  SWARM_NOTIFY_CHANNEL, SWARM_MAX_CONCURRENT
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET_DIR="${2:?--target requires a directory}"; shift 2 ;;
    --workspace) WORKSPACE_DIR="${2:?--workspace requires a directory}"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --no-role) NO_ROLE=1; shift ;;
    --no-activate) NO_ACTIVATE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

say() { printf '%s\n' "$*"; }
run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf '[dry-run]'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

abs_path() {
  python3 - "$1" <<'PY'
import os, sys
print(os.path.abspath(os.path.expanduser(sys.argv[1])))
PY
}

infer_workspace() {
  if [[ -n "$WORKSPACE_DIR" ]]; then
    abs_path "$WORKSPACE_DIR"
    return
  fi

  local d="$SCRIPT_DIR"
  while [[ "$d" != "/" ]]; do
    if [[ -f "$d/AGENTS.md" || -f "$d/roles/active.json" ]]; then
      printf '%s\n' "$d"
      return
    fi
    d="$(dirname "$d")"
  done

  if [[ -d "$HOME/.openclaw/workspace" ]]; then
    printf '%s\n' "$HOME/.openclaw/workspace"
  else
    printf '%s\n' "$HOME/.openclaw/workspace"
  fi
}

TARGET_DIR="$(abs_path "$TARGET_DIR")"
WORKSPACE_DIR="$(infer_workspace)"

backup_if_exists() {
  local path="$1"
  if [[ -e "$path" || -L "$path" ]]; then
    local backup="${path}.bak-${STAMP}"
    say "Backing up $path -> $backup"
    run cp -a "$path" "$backup"
  fi
}

copy_runtime_script() {
  local src="$1" dest="$2"
  if [[ ! -f "$src" ]]; then
    echo "Missing bundled script: $src" >&2
    exit 1
  fi
  run install -m 0755 "$src" "$dest"
}

install_template_once() {
  local src="$1" dest="$2" mode="${3:-0644}"
  if [[ -e "$dest" && "$FORCE" != "1" ]]; then
    say "Keeping existing $(basename "$dest")"
    return
  fi
  [[ -e "$dest" ]] && backup_if_exists "$dest"
  run install -m "$mode" "$src" "$dest"
}

say "🐝 Installing Epic AI Swarm Orchestration"
say "  Package:   $SCRIPT_DIR"
say "  Runtime:   $TARGET_DIR"
say "  Workspace: $WORKSPACE_DIR"

run mkdir -p "$TARGET_DIR" "$TARGET_DIR/logs" "$TARGET_DIR/endorsements"

say ""
say "Copying runtime scripts..."
find "$SCRIPT_DIR/scripts" -maxdepth 1 -type f -name '*.sh' -print0 | sort -z | while IFS= read -r -d '' src; do
  copy_runtime_script "$src" "$TARGET_DIR/$(basename "$src")"
done
if [[ -f "$SCRIPT_DIR/scripts/swarm.conf.example" ]]; then
  run install -m 0644 "$SCRIPT_DIR/scripts/swarm.conf.example" "$TARGET_DIR/swarm.conf.example"
fi

say ""
say "Installing config/state templates..."
install_template_once "$SCRIPT_DIR/templates/swarm.conf.sh" "$TARGET_DIR/swarm.conf" 0600
install_template_once "$SCRIPT_DIR/templates/duty-table.json" "$TARGET_DIR/duty-table.json" 0644
install_template_once "$SCRIPT_DIR/templates/active-tasks.json" "$TARGET_DIR/active-tasks.json" 0644
install_template_once "$SCRIPT_DIR/templates/archived-tasks.json" "$TARGET_DIR/archived-tasks.json" 0644
install_template_once "$SCRIPT_DIR/templates/inbox.json" "$TARGET_DIR/inbox.json" 0644
install_template_once "$SCRIPT_DIR/templates/pulse-state.json" "$TARGET_DIR/pulse-state.json" 0644
install_template_once "$SCRIPT_DIR/templates/usage-log.json" "$TARGET_DIR/usage-log.json" 0644
[[ -e "$TARGET_DIR/pending-notifications.txt" && "$FORCE" != "1" ]] || run touch "$TARGET_DIR/pending-notifications.txt"

# Apply non-secret environment overrides to swarm.conf when it was just installed or --force was used.
if [[ "$DRY_RUN" != "1" && -f "$TARGET_DIR/swarm.conf" ]]; then
  python3 - "$TARGET_DIR/swarm.conf" <<'PY'
import os, re, sys
path = sys.argv[1]
text = open(path).read()
updates = {
    'SWARM_NOTIFY_TARGET': os.environ.get('SWARM_NOTIFY_TARGET'),
    'SWARM_NOTIFY_CHANNEL': os.environ.get('SWARM_NOTIFY_CHANNEL'),
    'SWARM_MAX_CONCURRENT': os.environ.get('SWARM_MAX_CONCURRENT'),
}
for key, value in updates.items():
    if value is None or value == '':
        continue
    quoted = value if key == 'SWARM_MAX_CONCURRENT' and value.isdigit() else repr(value).replace("'", '"')
    text = re.sub(rf'^{key}=.*$', f'{key}={quoted}', text, flags=re.M)
open(path, 'w').write(text)
PY
fi

# Stamp template duty table with host-local install time and next Saturday noon PT if zoneinfo is available.
if [[ "$DRY_RUN" != "1" && -f "$TARGET_DIR/duty-table.json" ]]; then
  python3 - "$TARGET_DIR/duty-table.json" <<'PY' || true
import datetime, json, sys
try:
    from zoneinfo import ZoneInfo
    tz = ZoneInfo('America/Los_Angeles')
except Exception:
    tz = datetime.datetime.now().astimezone().tzinfo
path = sys.argv[1]
with open(path) as f:
    data = json.load(f)
if not data.get('assessedAt'):
    now = datetime.datetime.now(tz)
    nxt = now.replace(hour=12, minute=0, second=0, microsecond=0)
    nxt += datetime.timedelta(days=(5 - nxt.weekday()) % 7)
    if nxt <= now:
        nxt += datetime.timedelta(days=7)
    data['assessedAt'] = now.isoformat()
    data['nextAssessment'] = nxt.isoformat()
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
PY
fi

if [[ "$NO_ROLE" != "1" ]]; then
  say ""
say "Installing swarm-lead role..."
  ROLE_DEST="$WORKSPACE_DIR/roles/swarm-lead"
  run mkdir -p "$ROLE_DEST"
  for f in ROLE.md TOOLS.md HEARTBEAT.md; do
    src="$SCRIPT_DIR/roles/swarm-lead/$f"
    dest="$ROLE_DEST/$f"
    if [[ -f "$dest" ]] && ! cmp -s "$src" "$dest"; then
      backup_if_exists "$dest"
    fi
    run install -m 0644 "$src" "$dest"
  done

  if [[ "$NO_ACTIVATE" != "1" ]]; then
    say "Activating swarm-lead role..."
    run mkdir -p "$WORKSPACE_DIR/roles"
    if [[ "$DRY_RUN" != "1" ]]; then
      [[ -f "$WORKSPACE_DIR/roles/active.json" ]] && cp -a "$WORKSPACE_DIR/roles/active.json" "$WORKSPACE_DIR/roles/active.json.bak-${STAMP}"
      python3 - "$WORKSPACE_DIR/roles/active.json" <<'PY'
import datetime, json, os, sys
path = sys.argv[1]
if os.path.exists(path):
    try:
        data = json.load(open(path))
    except Exception:
        data = {}
else:
    data = {}
roles = data.get('activeRoles')
if not isinstance(roles, list):
    roles = []
if 'swarm-lead' not in roles:
    roles.append('swarm-lead')
data['activeRoles'] = roles
data['updatedAt'] = datetime.date.today().isoformat()
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
PY
    fi
  fi
fi

# Optional workspace symlink for agents that discover swarm inside the OpenClaw workspace.
if [[ -d "$WORKSPACE_DIR" && "$WORKSPACE_DIR/swarm" != "$TARGET_DIR" && ! -e "$WORKSPACE_DIR/swarm" && ! -L "$WORKSPACE_DIR/swarm" ]]; then
  say ""
say "Creating workspace symlink: $WORKSPACE_DIR/swarm -> $TARGET_DIR"
  run ln -s "$TARGET_DIR" "$WORKSPACE_DIR/swarm"
fi

say ""
say "✅ Install complete."
say "Next: bash $SCRIPT_DIR/doctor.sh --target $TARGET_DIR"
say "Then authenticate model CLIs and run: $TARGET_DIR/assess-models.sh --dry-run"
