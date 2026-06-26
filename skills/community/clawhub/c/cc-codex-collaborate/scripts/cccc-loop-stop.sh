#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"
ROOT="$(cccc_repo_root)"
cd "$ROOT"
SETTINGS=".claude/settings.json"
STATE="docs/cccc/state.json"
CONFIG="docs/cccc/config.json"
BACKUP=".claude/settings.json.cccc-backup-$(date -u +%Y%m%dT%H%M%SZ)"

if [[ -f "$SETTINGS" ]]; then
  cp "$SETTINGS" "$BACKUP"
  python3 - <<'PY'
import json
from pathlib import Path
settings_path = Path('.claude/settings.json')
try:
    settings = json.loads(settings_path.read_text())
except Exception:
    settings = {}
commands = {
    '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-sensitive-op-guard.sh',
    '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop.sh',
    '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop-failure.sh',
}
hooks = settings.get('hooks', {})
for event in list(hooks.keys()):
    groups = []
    for group in hooks.get(event, []):
        entries = [h for h in group.get('hooks', []) if not (h.get('type') == 'command' and h.get('command') in commands)]
        if entries:
            group['hooks'] = entries
            groups.append(group)
    if groups:
        hooks[event] = groups
    else:
        hooks.pop(event, None)
if hooks:
    settings['hooks'] = hooks
else:
    settings.pop('hooks', None)
settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n')
PY
fi

# Update config.json: disable loop
if [[ -f "$CONFIG" ]]; then
  python3 - <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/config.json')
data = json.loads(p.read_text())
data.setdefault('automation', {})['stop_hook_loop_enabled'] = False
# Revert mode to supervised-auto if it was full-auto-safe
if data.get('mode') == 'full-auto-safe':
    data['mode'] = 'supervised-auto'
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
PY
fi

# Update state.json: runtime fields only, remove mode if present
if [[ -f "$STATE" ]]; then
  python3 - <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/state.json')
try:
    state = json.loads(p.read_text())
except Exception:
    state = {}
state['pause_reason'] = 'Loop stopped by user.'
state['stop_hook_continuations'] = 0
state.pop('mode', None)
state.pop('enabled', None)
p.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
PY
fi

echo "Disabled cc-codex-collaborate loop automation."
echo "Removed cccc hook registrations from .claude/settings.json."
echo "Updated docs/cccc/config.json: mode = supervised-auto"
echo "Updated docs/cccc/config.json: automation.stop_hook_loop_enabled = false"
echo "Updated docs/cccc/state.json: stop_hook_continuations = 0"
if [[ -f "$BACKUP" ]]; then echo "Backup: $BACKUP"; fi
echo "Hook script files under .claude/hooks are left in place, but no longer registered."
