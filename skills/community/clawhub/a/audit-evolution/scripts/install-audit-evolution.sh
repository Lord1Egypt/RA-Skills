#!/usr/bin/env bash
set -euo pipefail

TARGET_WORKSPACE="$(pwd)"
AGENT="generic"
NO_AGENTS_UPDATE="false"
FORCE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target|--workspace)
      TARGET_WORKSPACE="${2:-$(pwd)}"
      shift 2
      ;;
    --agent)
      AGENT="${2:-generic}"
      shift 2
      ;;
    --no-agents-update)
      NO_AGENTS_UPDATE="true"
      shift
      ;;
    --force)
      FORCE="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_WORKSPACE="$(mkdir -p "$TARGET_WORKSPACE" && cd "$TARGET_WORKSPACE" && pwd)"
SKILL_DIR="$TARGET_WORKSPACE/skills/audit-evolution"
HOOK_DIR="$TARGET_WORKSPACE/.audit-evolution/hooks"
AGENTS_PATH="$TARGET_WORKSPACE/AGENTS.md"

if [[ -e "$SKILL_DIR" && "$FORCE" != "true" ]]; then
  echo "Target skill already exists: $SKILL_DIR. Re-run with --force to overwrite." >&2
  exit 1
fi

mkdir -p "$SKILL_DIR"

for name in SKILL.md README.md ADAPTERS_ZH.md QUICKSTART_60S_ZH.md DEMO_PLAYBOOK_ZH.md INSTALL_TEST_ZH.md SKILLHUNT_COPY_ZH.md FIELD_NOTE_TEMPLATE.md dirty_log.md clean_snapshot.md DESIGN_REVIEW_ZH.md index.html agents assets examples scripts; do
  if [[ -e "$REPO_ROOT/$name" ]]; then
    rm -rf "$SKILL_DIR/$name"
    cp -R "$REPO_ROOT/$name" "$SKILL_DIR/$name"
  fi
done

mkdir -p "$HOOK_DIR"
cp "$REPO_ROOT/scripts/invoke-audit-evolution-hook.sh" "$HOOK_DIR/invoke-audit-evolution-hook.sh"
chmod +x "$HOOK_DIR/invoke-audit-evolution-hook.sh"
if [[ -e "$REPO_ROOT/scripts/invoke-audit-evolution-hook.ps1" ]]; then
  cp "$REPO_ROOT/scripts/invoke-audit-evolution-hook.ps1" "$HOOK_DIR/invoke-audit-evolution-hook.ps1"
fi

read -r -d '' AGENTS_BLOCK <<'EOF' || true

<!-- AUDIT_EVOLUTION_START -->
## Audit Evolution Auto-Use

Use `skills/audit-evolution/SKILL.md` when any of these happen:

- The user says: `开始调用 Audit Evolution`, `进化`, `保存`, `暂停`, `跑分`, `继续`, or `详情`.
- A benchmark, scan, profile, worklog, handoff, task, or local test completes.
- The user points out an error, corrects a fact, or questions your conclusion.
- A task fails, times out, retries, gets blocked, or reads more than 5 files.
- Context pressure is over 60%, or your output contains uncertainty language such as "大概", "可能", "我理解为", or "不确定".
- You add or modify a skill, config, gear, route, prompt pattern, or answer pattern.

Default behavior:

1. First create or read `.audit-evolution/run-records/latest.md` when available.
2. Output: Evidence Pack, Snapshot, Evolution Card, Memory Ledger Entry, Minimal Skill Patch Proposal, Field Note, Next-Run Bootstrap, Short Command Menu.
3. Do not publish, upload, install, vote, comment, message, spend, claim, or run official benchmark without explicit human approval.
4. If you do not know where to save memory, use `write_target: proposed_only`.

Hook examples:

Windows:
```powershell
powershell -ExecutionPolicy Bypass -File .\.audit-evolution\hooks\invoke-audit-evolution-hook.ps1 -EventType task_failed_or_timeout_or_retry -Summary "任务失败，需要审计"
```

macOS/Linux:
```bash
bash ./.audit-evolution/hooks/invoke-audit-evolution-hook.sh --event task_failed_or_timeout_or_retry --summary "任务失败，需要审计"
```
<!-- AUDIT_EVOLUTION_END -->
EOF

if [[ "$NO_AGENTS_UPDATE" != "true" ]]; then
  if [[ -e "$AGENTS_PATH" ]]; then
    if grep -q '<!-- AUDIT_EVOLUTION_START -->' "$AGENTS_PATH"; then
      TMP_AGENTS="${AGENTS_PATH}.tmp"
      awk -v block="$AGENTS_BLOCK" '
        /<!-- AUDIT_EVOLUTION_START -->/ {
          if (!done) {
            print block
            done = 1
          }
          in_block = 1
          next
        }
        /<!-- AUDIT_EVOLUTION_END -->/ {
          in_block = 0
          next
        }
        !in_block { print }
      ' "$AGENTS_PATH" > "$TMP_AGENTS"
      mv "$TMP_AGENTS" "$AGENTS_PATH"
    else
      {
        printf "\n%s\n" "$AGENTS_BLOCK"
      } >> "$AGENTS_PATH"
    fi
  else
    {
      printf "# AGENTS.md\n"
      printf "%s\n" "$AGENTS_BLOCK"
    } > "$AGENTS_PATH"
  fi
fi

mkdir -p "$TARGET_WORKSPACE/.audit-evolution"
QUICKSTART_PATH="$TARGET_WORKSPACE/.audit-evolution/QUICKSTART_ZH.md"
cat > "$QUICKSTART_PATH" <<EOF
# Audit Evolution Quickstart

已安装到：

\`\`\`text
$SKILL_DIR
\`\`\`

立刻复制给你的 Agent：

\`\`\`text
开始调用 Audit Evolution。

请先读取 skills/audit-evolution/SKILL.md；如果存在 .audit-evolution/run-records/latest.md，也优先读取它。
目标：检查最近一次任务后，是否应该继续自进化。
边界：先审计和提出建议，不要直接修改系统，不要执行外部动作。
\`\`\`

短指令：

\`\`\`text
进化 / 保存 / 暂停 / 跑分 / 继续 / 详情
\`\`\`
EOF

cat <<JSON
{
  "status": "installed",
  "agent": "$AGENT",
  "target_workspace": "$TARGET_WORKSPACE",
  "skill_dir": "$SKILL_DIR",
  "agents_md": "$([[ "$NO_AGENTS_UPDATE" == "true" ]] && echo "skipped" || echo "$AGENTS_PATH")",
  "hook_dir": "$HOOK_DIR",
  "quickstart": "$QUICKSTART_PATH"
}
JSON
