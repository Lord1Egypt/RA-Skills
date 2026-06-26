#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

STATE="docs/cccc/state.json"
CONFIG="docs/cccc/config.json"

if [[ ! -f "$STATE" ]]; then
  echo "cc-codex-collaborate is not initialized. Run /cc-codex-collaborate setup first."
  exit 1
fi

python3 - "$STATE" "$CONFIG" <<'PY'
import json, sys

state = json.loads(open(sys.argv[1]).read())
config_path = sys.argv[2]
try:
    config = json.loads(open(config_path).read())
except Exception:
    config = {}

mode = config.get('mode', state.get('mode', 'unknown'))
lang = config.get('language', {}).get('user_language', state.get('user_language', 'auto'))
max_diff = config.get('milestones', {}).get('max_diff_lines_per_milestone', 1200)
max_files = config.get('milestones', {}).get('max_changed_files_per_milestone', 20)
max_review = config.get('review', {}).get('max_review_rounds_per_milestone', 3)
loop_enabled = config.get('automation', {}).get('stop_hook_loop_enabled', False)

print(f"Skill: {state.get('skill_name', 'cc-codex-collaborate')} v{state.get('skill_version', 'unknown')}")
print(f"Workspace: {state.get('workspace', 'docs/cccc')}")
print(f"Language: {lang}")
print(f"Mode: {mode}")
print(f"Status: {state.get('status', 'unknown')}")
print(f"Project context: {state.get('project_context_status', 'unknown')}")
print(f"Roadmap: {state.get('roadmap_status', 'unknown')}")
print(f"Current milestone: {state.get('current_milestone_id') or 'none'}")
print(f"Pause reason: {state.get('pause_reason') or 'none'}")
print(f"Completed milestones: {', '.join(state.get('completed_milestones', [])) or 'none'}")
print(f"Known risks: {len(state.get('known_risks', []))}")
print(f"--- Config (from config.json) ---")
print(f"Max diff per milestone: {max_diff}")
print(f"Max changed files per milestone: {max_files}")
print(f"Max review rounds per milestone: {max_review}")
print(f"Stop hook loop enabled: {loop_enabled}")
PY
