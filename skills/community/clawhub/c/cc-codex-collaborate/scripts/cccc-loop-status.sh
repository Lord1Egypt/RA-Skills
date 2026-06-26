#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"
ROOT="$(cccc_repo_root)"
cd "$ROOT"
SETTINGS=".claude/settings.json"
CONFIG="docs/cccc/config.json"
STATE="docs/cccc/state.json"
HOOK_DIR=".claude/hooks"

# Helper: read value from JSON file using python3
json_value() {
  local file="$1" key="$2" default="$3"
  python3 - "$file" "$key" "$default" <<'PY'
import json, sys
try:
    data = json.loads(open(sys.argv[1]).read())
    parts = sys.argv[2].lstrip('.').split('.')
    v = data
    for p in parts:
        if isinstance(v, dict) and p in v:
            v = v[p]
        else:
            v = None
            break
    print(v if v is not None else sys.argv[3])
except Exception:
    print(sys.argv[3])
PY
}

# Helper: check if a hook command is registered in settings
has_hook_cmd() {
  local cmd="$1"
  python3 - "$SETTINGS" "$cmd" <<'PY'
import json, sys
try:
    settings = json.loads(open(sys.argv[1]).read())
    target = sys.argv[2]
    for event, groups in settings.get('hooks', {}).items():
        for group in groups:
            for hook in group.get('hooks', []):
                if hook.get('command') == target:
                    print('yes')
                    sys.exit(0)
    print('no')
except Exception:
    print('no')
PY
}

echo "cc-codex-collaborate status"
echo "============================"
echo ""

# ── Version information ──

SKILL_DIR="$(cccc_skill_dir)"
SKILL_VERSION="$(cat "$SKILL_DIR/VERSION" 2>/dev/null || echo 'unknown')"
PROJECT_VERSION="$(json_value "$CONFIG" '.skill.installed_version' 'unknown')"
# Fallback to old version field if skill.installed_version missing
if [[ "$PROJECT_VERSION" == "unknown" ]]; then
  PROJECT_VERSION="$(json_value "$CONFIG" '.version' 'unknown')"
fi

echo "Version:"
echo "  Skill version: $SKILL_VERSION"
echo "  Project installed version: $PROJECT_VERSION"

# Schema versions
CONFIG_SCHEMA="$(json_value "$CONFIG" '.skill.workspace_schema_version' 'unknown')"
STATE_SCHEMA="$(json_value "$STATE" '.workspace_schema_version' 'unknown')"

echo "  Config schema version: $CONFIG_SCHEMA"
echo "  State schema version: $STATE_SCHEMA"

# ── Migration history ──

if [[ -f "$STATE" ]]; then
  LAST_MIGRATION="$(json_value "$STATE" '.last_migration_at' '')"
  FROM_VERSION="$(json_value "$STATE" '.last_migration_from_version' '')"
  TO_VERSION="$(json_value "$STATE" '.last_migration_to_version' '')"
  if [[ -n "$LAST_MIGRATION" && "$LAST_MIGRATION" != "null" ]]; then
    echo "  Last migration: $LAST_MIGRATION"
    echo "  Migration: $FROM_VERSION -> $TO_VERSION"
  fi
fi

echo ""

# ── Update recommendation ──

if [[ "$SKILL_VERSION" != "$PROJECT_VERSION" ]]; then
  echo "Update recommended: YES"
  echo "  Run: /cc-codex-collaborate update"
else
  echo "Update recommended: NO (versions match)"
fi

echo ""

# ── Config status ──

if [[ -f "$CONFIG" ]]; then
  echo "Config file: present ($CONFIG)"
  echo "  mode: $(json_value "$CONFIG" '.mode' 'unknown')"
  echo "  stop_hook_loop_enabled: $(json_value "$CONFIG" '.automation.stop_hook_loop_enabled' 'false')"
  echo "  user_language: $(json_value "$CONFIG" '.language.user_language' 'auto')"
else
  echo "Config file: MISSING ($CONFIG)"
  echo "  Run /cc-codex-collaborate setup first."
fi

echo ""

# ── State status ──

if [[ -f "$STATE" ]]; then
  echo "State file: present ($STATE)"
  echo "  status: $(json_value "$STATE" '.status' 'unknown')"
  echo "  current_milestone: $(json_value "$STATE" '.current_milestone_id' 'none')"
  echo "  pause_reason: $(json_value "$STATE" '.pause_reason' '')"
  echo "  stop_hook_continuations: $(json_value "$STATE" '.stop_hook_continuations' '0')"
else
  echo "State file: MISSING ($STATE)"
fi

echo ""

# Hooks directory and files
echo "Hooks directory: $([[ -d "$HOOK_DIR" ]] && echo present || echo missing)"
for script in cccc-sensitive-op-guard.sh cccc-stop.sh cccc-stop-failure.sh; do
  if [[ -x "$HOOK_DIR/$script" ]]; then
    file_status="installed"
  elif [[ -f "$HOOK_DIR/$script" ]]; then
    file_status="present (not executable)"
  else
    file_status="missing"
  fi
  echo "  $script: $file_status"
done

echo ""

# Settings.json hook registrations
echo "Settings file: $([[ -f "$SETTINGS" ]] && echo present || echo missing)"
hook_commands=(
  "PreToolUse:\${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-sensitive-op-guard.sh"
  "Stop:\${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop.sh"
  "StopFailure:\${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop-failure.sh"
)
for entry in "${hook_commands[@]}"; do
  event="${entry%%:*}"
  cmd="${entry#*:}"
  configured="$(has_hook_cmd "$cmd")"
  echo "  $event: $configured"
done

echo ""

# Overall loop status
loop_enabled_in_config="false"
if [[ -f "$CONFIG" ]]; then
  loop_enabled_in_config="$(json_value "$CONFIG" '.automation.stop_hook_loop_enabled' 'false')"
fi
stop_hook_registered="$(has_hook_cmd '${CLAUDE_PROJECT_DIR}/.claude/hooks/cccc-stop.sh')"

if [[ "$loop_enabled_in_config" == "True" ]] && [[ "$stop_hook_registered" == "yes" ]]; then
  echo "Auto loop: ENABLED"
else
  echo "Auto loop: DISABLED"
fi

# ── Resume guidance ──

echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_MILESTONE_ID="$(json_value "$STATE" '.current_milestone_id' '')"
HAS_PLANNING_DOCS="false"
if [[ -f docs/cccc/roadmap.md || -f docs/cccc/milestone-backlog.md || -f docs/cccc/current-state.md ]]; then
  HAS_PLANNING_DOCS="$(python3 "$SCRIPT_DIR/cccc-detect-workflow.py" has-planning-docs 2>/dev/null || echo "false")"
fi

# State mismatch detection
if [[ -f "$STATE" ]] && [[ "$HAS_PLANNING_DOCS" == "true" ]]; then
  if [[ -z "$CURRENT_MILESTONE_ID" || "$CURRENT_MILESTONE_ID" == "null" || "$CURRENT_MILESTONE_ID" == "none" ]]; then
    echo "State mismatch:"
    echo "  Planning docs exist (roadmap/backlog/current-state)"
    echo "  state.current_milestone_id is missing"
    CANDIDATE="$(python3 "$SCRIPT_DIR/cccc-detect-workflow.py" find-milestone 2>/dev/null || echo "null")"
    if [[ "$CANDIDATE" != "null" && "$CANDIDATE" != "" ]]; then
      CANDIDATE_ID="$(echo "$CANDIDATE" | jq -r '.id // empty')"
      CANDIDATE_TITLE="$(echo "$CANDIDATE" | jq -r '.title // empty')"
      if [[ -n "$CANDIDATE_ID" ]]; then
        echo "  Candidate milestone: $CANDIDATE_ID ${CANDIDATE_TITLE:+— $CANDIDATE_TITLE}"
      fi
    fi
    echo ""
    echo "Next: /cc-codex-collaborate resume"
  else
    # Normal resume guidance with milestone
    RESUME_STATUS="$(json_value "$STATE" '.status' 'unknown')"
    case "$RESUME_STATUS" in
      PAUSED_FOR_HUMAN|NEEDS_HUMAN)
        echo "Next: /cc-codex-collaborate resume"
        ;;
      PAUSED_FOR_CODEX)
        echo "Next: configure Codex locally, then /cc-codex-collaborate resume"
        ;;
      PAUSED_FOR_SYSTEM)
        echo "Next: inspect docs/cccc/logs/stop-failure-*.json, then /cc-codex-collaborate resume"
        ;;
      NEEDS_SECRET|SENSITIVE_OPERATION|UNSAFE|FAIL_UNCLEAR|REVIEW_THRESHOLD_EXCEEDED)
        echo "Next: /cc-codex-collaborate resume"
        ;;
      DONE|COMPLETED|FAILED)
        echo "Next: /cc-codex-collaborate \"your task\""
        ;;
      *)
        if [[ "$loop_enabled_in_config" == "True" ]]; then
          echo "Next: /cc-codex-collaborate resume or wait for Stop hook continuation"
        else
          echo "Next: /cc-codex-collaborate \"your task\""
        fi
        ;;
    esac
  fi
elif [[ -f "$STATE" ]]; then
  RESUME_STATUS="$(json_value "$STATE" '.status' 'unknown')"
  case "$RESUME_STATUS" in
    PAUSED_FOR_HUMAN|NEEDS_HUMAN|PAUSED_FOR_CODEX|PAUSED_FOR_SYSTEM|NEEDS_SECRET|SENSITIVE_OPERATION|UNSAFE|FAIL_UNCLEAR|REVIEW_THRESHOLD_EXCEEDED)
      echo "Next: /cc-codex-collaborate resume"
      ;;
    DONE|COMPLETED|FAILED)
      echo "Next: /cc-codex-collaborate \"your task\""
      ;;
    *)
      if [[ "$loop_enabled_in_config" == "True" ]]; then
        echo "Next: /cc-codex-collaborate resume or wait for Stop hook continuation"
      else
        echo "Next: /cc-codex-collaborate \"your task\""
      fi
      ;;
  esac
else
  echo "Next: /cc-codex-collaborate \"your task\""
fi
