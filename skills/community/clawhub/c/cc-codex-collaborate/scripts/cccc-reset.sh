#!/usr/bin/env bash
# CCCC Reset — reset state machine runtime state and rehydrate from docs.
# Does NOT delete planning docs, reviews, or logs.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

ROOT="$(cccc_repo_root)"
cd "$ROOT"

CONFIG="docs/cccc/config.json"
STATE="docs/cccc/state.json"
SKILL_DIR="$(cccc_skill_dir)"
TEMPLATE_DIR="$SKILL_DIR/templates/cccc"

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: docs/cccc/config.json 不存在。" >&2
  echo "运行 /cc-codex-collaborate setup" >&2
  exit 1
fi

TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
BACKUP_DIR="docs/cccc/backups/reset-$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

# Backup files that will be modified
for f in "$STATE" docs/cccc/context-bundle.md docs/cccc/current-state.md docs/cccc/milestone-backlog.md; do
  if [[ -f "$f" ]]; then
    cp "$f" "$BACKUP_DIR/$(basename "$f")"
  fi
done

echo "备份目录: $BACKUP_DIR"
echo ""

# Run rehydration
TEMPLATE_PATH="$TEMPLATE_DIR/state.template.json"
NEW_STATE="$(python3 "$SCRIPT_DIR/cccc-rehydrate-state.py")"

# Write new state
echo "$NEW_STATE" > "$STATE"
echo "state.json 已重建。"

# Parse key fields for report
STATUS="$(echo "$NEW_STATE" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("status","UNKNOWN"))')"
MID="$(echo "$NEW_STATE" | python3 -c 'import json,sys; d=json.loads(sys.stdin.read()); print(d.get("current_milestone_id") or "(none)")')"
CONFIDENCE="$(echo "$NEW_STATE" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read()).get("rehydrate_confidence","low"))')"
SOURCES="$(echo "$NEW_STATE" | python3 -c 'import json,sys; print(", ".join(json.loads(sys.stdin.read()).get("last_state_rehydrate_sources",[])))')"
PAUSE="$(echo "$NEW_STATE" | python3 -c 'import json,sys; d=json.loads(sys.stdin.read()); print(d.get("pause_reason") or "无")')"

# Rebuild context bundle
if [[ -f "$SCRIPT_DIR/cccc-build-context.sh" ]]; then
  CONTEXT_OUT="$(bash "$SCRIPT_DIR/cccc-build-context.sh" 2>/dev/null || echo "")"
  if [[ -n "$CONTEXT_OUT" ]]; then
    echo "context-bundle.md 已重建。"
  fi
fi

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Reset State 完成"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "恢复结果："
echo "  当前状态: $STATUS"
echo "  当前 milestone: $MID"
echo "  推断来源: $SOURCES"
echo "  置信度: $CONFIDENCE"
echo "  pause_reason: $PAUSE"
echo ""
echo "备份：$BACKUP_DIR"
echo ""
echo "下一步："
if [[ "$STATUS" == "NEEDS_HUMAN" ]]; then
  echo "  - /cc-codex-collaborate resume"
else
  echo "  - /cc-codex-collaborate resume"
fi
