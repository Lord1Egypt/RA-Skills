#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"
ROOT="$(cccc_repo_root)"
cd "$ROOT"
SKILL_DIR="$(cccc_skill_dir)"
SETTINGS=".claude/settings.json"
CONFIG="docs/cccc/config.json"
STATE="docs/cccc/state.json"
BACKUP=".claude/settings.json.cccc-backup-$(date -u +%Y%m%dT%H%M%SZ)"

# ── Step 1: Enable stop-hook automation ──

mkdir -p .claude/hooks docs/cccc/runtime
cp "$SKILL_DIR/hooks/cccc-sensitive-op-guard.sh" .claude/hooks/cccc-sensitive-op-guard.sh
cp "$SKILL_DIR/hooks/cccc-stop.sh" .claude/hooks/cccc-stop.sh
cp "$SKILL_DIR/hooks/cccc-stop-failure.sh" .claude/hooks/cccc-stop-failure.sh
chmod +x .claude/hooks/cccc-*.sh

# Ensure workspace exists
if [[ ! -f docs/cccc/state.json ]]; then
  "$SCRIPT_DIR/cccc-init.sh"
fi

# Backup and update settings.json
if [[ -f "$SETTINGS" ]]; then
  cp "$SETTINGS" "$BACKUP"
else
  mkdir -p .claude
  echo '{}' > "$SETTINGS"
fi

python3 - <<'PY'
import json
from pathlib import Path
settings_path = Path('.claude/settings.json')
try:
    settings = json.loads(settings_path.read_text())
except Exception:
    settings = {}
settings.setdefault('hooks', {})

def add_hook(event, matcher, command):
    hooks = settings['hooks'].setdefault(event, [])
    for group in hooks:
        if group.get('matcher', '') == matcher:
            entries = group.setdefault('hooks', [])
            if not any(h.get('type') == 'command' and h.get('command') == command for h in entries):
                entries.append({'type': 'command', 'command': command})
            return
    hooks.append({'matcher': matcher, 'hooks': [{'type': 'command', 'command': command}]})

add_hook('PreToolUse', 'Bash|Edit|Write|MultiEdit', '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-sensitive-op-guard.sh')
add_hook('Stop', '', '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop.sh')
add_hook('StopFailure', '', '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop-failure.sh')
settings_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n')
PY

# Update config.json: enable loop, set mode
if [[ -f "$CONFIG" ]]; then
  python3 - <<'PY'
import json
from pathlib import Path
p = Path('docs/cccc/config.json')
data = json.loads(p.read_text())
data.setdefault('automation', {})['stop_hook_loop_enabled'] = True
data.setdefault('automation', {}).setdefault('max_stop_hook_continuations', 10)
data['mode'] = 'full-auto-safe'
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
PY
fi

# Update state.json: runtime fields only, remove mode/enabled if present
python3 - <<'PY'
import json
from pathlib import Path
state_path = Path('docs/cccc/state.json')
try:
    state = json.loads(state_path.read_text())
except Exception:
    state = {}
state['stop_hook_continuations'] = 0
state.pop('mode', None)
state.pop('enabled', None)
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
PY

echo "Enabled cc-codex-collaborate loop automation."
echo "Installed hooks into .claude/hooks and registered them in .claude/settings.json."
echo "Updated docs/cccc/config.json: mode = full-auto-safe"
echo "Updated docs/cccc/config.json: automation.stop_hook_loop_enabled = true"
echo "Updated docs/cccc/state.json: stop_hook_continuations = 0"
if [[ -f "$BACKUP" ]]; then echo "Backup: $BACKUP"; fi

echo ""

# ── Step 2: Check if an active workflow can be continued ──

DETECT_RESULT="$(python3 "$SCRIPT_DIR/cccc-detect-workflow.py" detect 2>/dev/null || echo '{}')"

WORKFLOW_ACTION="$(echo "$DETECT_RESULT" | jq -r '.action // "needs_task"')"
WORKFLOW_REASON="$(echo "$DETECT_RESULT" | jq -r '.reason // "No task, roadmap, or milestone backlog found."')"
WORKFLOW_MILESTONE="$(echo "$DETECT_RESULT" | jq -r '.milestone_id // empty')"
WORKFLOW_REPAIRED="$(echo "$DETECT_RESULT" | jq -r '.state_repaired // false')"

# ── Step 3: Output machine-readable markers and human guidance ──

echo "CCCC_LOOP_START_RESULT=enabled"
echo "CCCC_WORKFLOW_ACTION=$WORKFLOW_ACTION"
echo "CCCC_WORKFLOW_REASON=\"$WORKFLOW_REASON\""
echo ""

case "$WORKFLOW_ACTION" in
  continue_now)
    echo "Loop automation is enabled and an active workflow was found."
    if [[ "$WORKFLOW_REPAIRED" == "true" && -n "$WORKFLOW_MILESTONE" ]]; then
      echo "State repaired: current_milestone_id set to $WORKFLOW_MILESTONE."
    fi
    echo "Continue the cc-codex-collaborate state machine now."
    echo "Do not stop after enabling hooks."
    echo "Read docs/cccc/config.json and docs/cccc/state.json, then execute the next safe step."
    ;;
  needs_resume)
    echo "Existing workflow found but requires resume."
    echo "Run: /cc-codex-collaborate resume"
    ;;
  needs_task)
    echo "No workflow found. Start a new task:"
    echo "  /cc-codex-collaborate \"your task description\""
    ;;
  done)
    echo "Current workflow has already completed."
    echo "Start a new task: /cc-codex-collaborate \"your task description\""
    ;;
esac
