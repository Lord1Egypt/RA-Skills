#!/usr/bin/env bash
# CCCC Repair — auto-fix safe inconsistencies.
# Does NOT bypass Codex gates, safety pauses, or ambiguous states.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/cccc-common.sh"

ROOT="$(cccc_repo_root)"
cd "$ROOT"

CONFIG="docs/cccc/config.json"
STATE="docs/cccc/state.json"
SETTINGS="$ROOT/.claude/settings.json"
HOOKS_DIR="$ROOT/.claude/hooks"
COMMANDS_DIR="$ROOT/.claude/commands"
SKILL_DIR="$(cccc_skill_dir)"
TEMPLATE_DIR="$SKILL_DIR/templates"

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: docs/cccc/config.json 不存在。" >&2
  echo "运行 /cc-codex-collaborate setup" >&2
  exit 1
fi

TIMESTAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
BACKUP_DIR="docs/cccc/backups/repair-$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

FIXES=()
STATE_BACKED_UP=false

backup_state() {
  if ! $STATE_BACKED_UP && [[ -f "$STATE" ]]; then
    cp "$STATE" "$BACKUP_DIR/state.json"
    STATE_BACKED_UP=true
  fi
}

# ── Fix 1: state.mode deprecated field → config.mode ──
if python3 -c "
import json
st = json.loads(open('$STATE').read())
if 'mode' in st:
    print('true')
else:
    print('false')
" 2>/dev/null | grep -q true; then
  OLD_MODE="$(python3 -c "import json; print(json.loads(open('$STATE').read()).get('mode',''))" 2>/dev/null)"
  backup_state
  python3 -c "
import json
st = json.loads(open('$STATE').read())
del st['mode']
open('$STATE','w').write(json.dumps(st, indent=2, ensure_ascii=False) + '\n')
"
  FIXES+=("移除 state.mode (值为 $OLD_MODE)，mode 由 config.json 管理")
fi

# ── Fix 2: state.enabled deprecated field → remove ──
if python3 -c "
import json
st = json.loads(open('$STATE').read())
print('true' if 'enabled' in st else 'false')
" 2>/dev/null | grep -q true; then
  backup_state
  python3 -c "
import json
st = json.loads(open('$STATE').read())
del st['enabled']
open('$STATE','w').write(json.dumps(st, indent=2, ensure_ascii=False) + '\n')
"
  FIXES+=("移除 state.enabled deprecated 字段")
fi

# ── Fix 3: loop enabled but hooks not registered ──
LOOP_ENABLED="$(python3 -c "
import json
cfg = json.loads(open('$CONFIG').read())
print(cfg.get('automation',{}).get('stop_hook_loop_enabled',False))
" 2>/dev/null || echo 'false')"

HOOKS_REGISTERED=false
if [[ -f "$SETTINGS" ]]; then
  if python3 -c "
import json
data = json.loads(open('$SETTINGS').read())
hooks = data.get('hooks', {})
for event, groups in hooks.items():
    for group in groups:
        for h in group.get('hooks', []):
            if 'cccc' in h.get('command', '').lower():
                print('true')
                exit(0)
print('false')
" 2>/dev/null | grep -q true; then
    HOOKS_REGISTERED=true
  fi
fi

if [[ "$LOOP_ENABLED" == "True" ]] && ! $HOOKS_REGISTERED; then
  echo "LOOP 已启用但 hooks 未注册。运行 /cc-codex-collaborate loop-start 注册 hooks。"
  FIXES+=("检测到: loop enabled 但 hooks 未注册 (需手动运行 loop-start)")
fi

# ── Fix 4: hooks missing but loop enabled ──
if [[ "$LOOP_ENABLED" == "True" ]] && [[ ! -f "$HOOKS_DIR/cccc-stop.sh" ]]; then
  mkdir -p "$HOOKS_DIR"
  for hook in "$SKILL_DIR/hooks"/cccc-*.sh; do
    [[ -e "$hook" ]] || continue
    name="$(basename "$hook")"
    cp "$hook" "$HOOKS_DIR/$name"
    chmod +x "$HOOKS_DIR/$name"
  done
  FIXES+=("同步 hook 脚本到 .claude/hooks/")
fi

# ── Fix 5: current_milestone_id missing but can be uniquely identified ──
MID="$(python3 -c "import json; print(json.loads(open('$STATE').read()).get('current_milestone_id') or '')" 2>/dev/null)"
if [[ -z "$MID" ]]; then
  CANDIDATE="$(python3 "$SCRIPT_DIR/cccc-rehydrate-state.py" 2>/dev/null | python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
mid = d.get('current_milestone_id')
conf = d.get('rehydrate_confidence', 'low')
if mid and conf in ('high', 'medium'):
    print(mid)
else:
    print('')
" 2>/dev/null || echo '')"
  if [[ -n "$CANDIDATE" ]]; then
    cp "$STATE" "$BACKUP_DIR/state.json" 2>/dev/null || true
    python3 "$SCRIPT_DIR/cccc-update-state.py" --set "current_milestone_id=$CANDIDATE" --set "status=READY_TO_CONTINUE" 2>/dev/null
    FIXES+=("恢复 current_milestone_id = $CANDIDATE (从文档推断)")
  fi
fi

# ── Fix 6: missing generated commands ──
if [[ -d "$TEMPLATE_DIR/commands" ]]; then
  mkdir -p "$COMMANDS_DIR"
  MISSING=()
  for src in "$TEMPLATE_DIR/commands"/*.md; do
    [[ -e "$src" ]] || continue
    name="$(basename "$src")"
    if [[ ! -f "$COMMANDS_DIR/$name" ]]; then
      cp "$src" "$COMMANDS_DIR/$name"
      MISSING+=("$name")
    fi
  done
  if [[ ${#MISSING[@]} -gt 0 ]]; then
    FIXES+=("补齐缺失命令: ${MISSING[*]}")
  fi
fi

# ── Fix 7: context-bundle.md missing ──
if [[ ! -f "docs/cccc/context-bundle.md" ]] && [[ -f "$SCRIPT_DIR/cccc-build-context.sh" ]]; then
  bash "$SCRIPT_DIR/cccc-build-context.sh" >/dev/null 2>&1
  FIXES+=("重建 context-bundle.md")
fi

# ── Report ──
echo ""
echo "════════════════════════════════════════════════════════════"
echo "CCCC Repair 完成"
echo "════════════════════════════════════════════════════════════"

if [[ ${#FIXES[@]} -eq 0 ]]; then
  echo ""
  echo "没有发现可自动修复的不一致。"
  echo "运行 /cc-codex-collaborate doctor 查看完整诊断。"
else
  echo ""
  echo "已修复："
  for fix in "${FIXES[@]}"; do
    echo "  - $fix"
  done
  echo ""
  echo "备份: $BACKUP_DIR"
  echo ""
  echo "未修复（需手动处理）："
  echo "  - Codex gate 未通过"
  echo "  - NEEDS_SECRET / SENSITIVE_OPERATION / UNSAFE 状态"
  echo "  - 多候选 milestone（无法唯一确定）"
fi
