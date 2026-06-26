#!/bin/bash
# revert_sync.sh — 版本回滚触发器 (v1.4)
# Usage: bash revert_sync.sh --dry-run <memory_dir> <target_version> [--lang en|zh]
#        bash revert_sync.sh --confirm <memory_dir> <target_version> [--lang en|zh]
#
# 回滚流程:
#  1. 读取 CHANGELOG.md，确认 target_version 是已发布的有效版本
#  2. 检查 memory/.sync_snapshots/<target_version>_pre/ 快照是否存在
#  3. 从 CHANGELOG 读取版本链（current → target 之间的所有版本）
#  4. 创建 Revert Manifest，分发到各 agent 工作空间
#  5. 更新 .current_system_version = target_version
#  6. 记录 journal（type=revert, status=reverted）
#  7. 输出操作结果摘要

set -e

# ── Atomic write (prevents partial/corrupt files) ──────────────────
_atomic_write() {
  local file="$1" content="$2"
  local tmp_file="${file}.tmp.$$"
  echo "$content" > "$tmp_file" && sync "$tmp_file" && mv "$tmp_file" "$file"
}

# ── Resolve script directory and registry path ─────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REGISTRY_FILE="$SKILL_DIR/references/agent-registry.json"

# ── Defaults ───────────────────────────────────────────────────────
MEMORY_DIR=""
TARGET_VER=""
DRY_RUN=false
LANG="zh"
CONFIRMED=false

# Version format regex: v<MAJOR>.<MINOR>[.<PATCH>]
VERSION_RE='^v[0-9]+\.[0-9]+(\.[0-9]+)?$'

# ── Simple JSON value extraction (no jq dependency) ────────────────
json_val() {
  local path="$1" file="$2" key
  key=$(echo "$path" | awk -F. '{print $NF}')
  if echo "$path" | grep -q '\.'; then
    local section=$(echo "$path" | awk -F. '{print $1}')
    grep -A 50 "\"$section\"" "$file" | grep "\"$key\"" | head -1 | sed 's/.*: *"//;s/".*//'
  else
    grep "\"$key\"" "$file" | head -1 | sed 's/.*: *"//;s/".*//'
  fi
}

# Resolve variables in a value string
resolve_vars() {
  local val="$1"
  local workspace_root=$(json_val "vars.workspace_root" "$REGISTRY_FILE")
  local master_agent=$(json_val "vars.master_agent" "$REGISTRY_FILE")
  val="${val//\$\{vars.workspace_root\}/$workspace_root}"
  val="${val//\$\{vars.master_agent\}/$master_agent}"
  echo "$val"
}

# Expand ~ to $HOME
expand_path() {
  local p="$1"
  echo "${p/#\~/$HOME}"
}

# Read all agent IDs from registry
read_agent_ids() {
  grep -E '^    "[a-z][a-z0-9_-]*" *: *\{' "$REGISTRY_FILE" \
    | sed 's/.*"\([^"]*\)".*/\1/' \
    | grep -v '^_comment'
}

# Read agent workspace from registry
read_agent_ws() {
  local agent_id="$1"
  local raw=$(grep -A 10 "\"$agent_id\":" "$REGISTRY_FILE" | grep '"workspace"' | head -1 | sed 's/.*: *"//;s/".*//')
  resolve_vars "$raw"
}

# Read agent display name
read_agent_name() {
  local agent_id="$1" lang="${2:-en}"
  local key result
  [ "$lang" = "zh" ] && key="name_zh" || key="name_en"
  result=$(grep -A 10 "\"$agent_id\":" "$REGISTRY_FILE" | grep "\"$key\"" | head -1 | sed 's/.*: *"//;s/".*//')
  # Fallback: if name_zh/name_en not found, use "name" field
  [ -z "$result" ] && result=$(grep -A 10 "\"$agent_id\":" "$REGISTRY_FILE" | grep '"name"' | head -1 | sed 's/.*: *"//;s/".*//')
  [ -z "$result" ] && result="$agent_id"
  echo "$result"
}

# ── Version comparison ─────────────────────────────────────────────
version_le() {
  # Returns 0 if $1 < $2 (true), 1 otherwise
  local a="${1#v}" b="${2#v}"
  local a1 a2 a3 b1 b2 b3
  IFS='.' read -r a1 a2 a3 <<< "$a"
  IFS='.' read -r b1 b2 b3 <<< "$b"
  a3="${a3:-0}"; b3="${b3:-0}"
  [ "$a1" -lt "$b1" ] && return 0
  [ "$a1" -gt "$b1" ] && return 1
  [ "$a2" -lt "$b2" ] && return 0
  [ "$a2" -gt "$b2" ] && return 1
  [ "$a3" -lt "$b3" ] && return 0
  return 1
}

# ── Bilingual messages ─────────────────────────────────────────────
msg() {
  local key="$1"; shift
  case "$LANG" in
    en)
      case "$key" in
        # ── Header / Help ──
        title)          echo "=== revert_sync.sh v1.4 — Rollback Trigger ===" ;;
        dry_warn)       echo "🔍 DRY-RUN MODE — no changes will be made" ;;
        mem_dir)        echo "Memory dir: $1" ;;

        # ── Help ──
        help1)          echo "Usage: bash scripts/revert_sync.sh --dry-run <memory_dir> <target_version> [--lang en|zh]" ;;
        help2)          echo "       bash scripts/revert_sync.sh --confirm <memory_dir> <target_version> [--lang en|zh]" ;;
        help3)          echo "  memory_dir         Path to memory directory (e.g. ~/.openclaw/workspace-amaster/memory)" ;;
        help4)          echo "  target_version     Version to rollback TO (e.g. v1.0)" ;;
        help5)          echo "  --dry-run          Preview without making changes" ;;
        help5b)         echo "  --confirm          Required for real execution (skip with --dry-run)" ;;
        help6)          echo "  --lang en|zh       Output language (default: zh)" ;;
        help7)          echo "  -h, --help         Show this help" ;;

        # ── Validation ──
        miss_args)      echo "Usage: bash scripts/revert_sync.sh <memory_dir> <target_version> [--dry-run|--confirm] [--lang en|zh]" ;;
        registry_err)   echo "❌ Registry not found: $REGISTRY_FILE" ;;
        invalid_target) echo "❌ Invalid target_version format: '$1'" ;;
        version_fmt)    echo "   Must match: vX.Y or vX.Y.Z (e.g., v1.0, v1.1)" ;;
        not_found)      echo "❌ Version '$1' not found in CHANGELOG.md" ;;
        not_pub)        echo "   Only published versions (with '## vX.Y' entries) are valid rollback targets." ;;
        same_version)   echo "❌ Target version is same as current version ($1) — nothing to do." ;;
        not_backward)   echo "❌ Target version ($1) is newer than current version ($2)." ;;
        no_changelog)   echo "❌ CHANGELOG.md not found at: $1" ;;
        no_current)     echo "❌ .current_system_version not found at: $1" ;;

        # ── Dry-run preview ──
        pv_title)       echo "" ; echo "── Rollback Preview ──" ;;
        pv_current)     echo "  Current version: $1" ;;
        pv_target)      echo "  Target version:  $1" ;;
        pv_path)        echo "  Rollback path:   $1 → $2 (${3} step(s))" ;;
        pv_versions)    echo "  Versions affected:$1" ;;
        pv_impact)      echo "  Scope:           all agents ($1)" ;;
        pv_snap_ok)     echo "  Snapshots:       memory/.sync_snapshots/$1_pre/ → EXISTS" ;;
        pv_snap_warn)   echo "  Snapshots:       memory/.sync_snapshots/$1_pre/ → MISSING (warning: fallback to file-list restore)" ;;
        pv_manifest)    echo "  Revert manifest  → will be written to $1 agent workspace(s)" ;;
        pv_summary)     echo "  On completion, .current_system_version → $1" ;;

        # ── Real execution ──
        ex_title)       echo "" ; echo "── Rollback Execution ──" ;;
        ex_current)     echo "  Current version: $1" ;;
        ex_target)      echo "  Target version:  $1" ;;
        ex_path)        echo "  Rollback path:   $1 → $2 (${3} step(s))" ;;
        ex_snap_ok)     echo "  ✅ Snapshot: .sync_snapshots/$1_pre/ exists" ;;
        ex_snap_warn)   echo "  ⚠️  Snapshot: .sync_snapshots/$1_pre/ MISSING (will use CHANGELOG file list)" ;;
        ex_manifest)    echo "  📄 Manifest saved: $1/memory/revert_sync_$2_$3.md" ;;
        ex_writing)     echo "  📝 Writing to agent: $1" ;;
        ex_agent_done)  echo "  ✅ Agent '$1' received revert manifest" ;;
        ex_agent_skip)  echo "  ⚠️  Agent '$1' workspace not found, skipped" ;;
        ex_updated)     echo "  🔄 .current_system_version = $1" ;;
        ex_journal)     echo "  📋 Journal record written" ;;
        ex_complete)    echo "" ; echo "✅ Rollback dispatched. Agents will restore from snapshot on next heartbeat." ;;

        # ── Confirm prompt ──
        confirm_msg)    echo "" ; echo "⚠️  Security confirmation required" ;;
        confirm_hint)   echo "   First run with --dry-run to preview" ;;
        confirm_cmd)    echo "   Then run with --confirm to execute:" ;;
      esac
      ;;
    zh|*)
      case "$key" in
        # ── Header / Help ──
        title)          echo "=== revert_sync.sh v1.4 — 回滚触发器 ===" ;;
        dry_warn)       echo "🔍 预览模式 — 不会执行任何修改" ;;
        mem_dir)        echo "Memory 目录: $1" ;;

        # ── Help ──
        help1)          echo "用法: bash scripts/revert_sync.sh --dry-run <memory_dir> <target_version> [--lang en|zh]" ;;
        help2)          echo "      bash scripts/revert_sync.sh --confirm <memory_dir> <target_version> [--lang en|zh]" ;;
        help3)          echo "  memory_dir         Memory 目录路径 (如 ~/.openclaw/workspace-amaster/memory)" ;;
        help4)          echo "  target_version     要回滚到的目标版本 (如 v1.0)" ;;
        help5)          echo "  --dry-run          预览模式，不执行修改" ;;
        help5b)          echo "  --confirm          正式执行时必需 (--dry-run 模式下不需要)" ;;
        help6)          echo "  --lang en|zh       输出语言 (默认: zh)" ;;
        help7)          echo "  -h, --help         显示帮助" ;;

        # ── Validation ──
        miss_args)      echo "用法: bash scripts/revert_sync.sh <memory_dir> <target_version> [--dry-run|--confirm] [--lang en|zh]" ;;
        registry_err)   echo "❌ 未找到注册表: $REGISTRY_FILE" ;;
        invalid_target) echo "❌ 目标版本格式无效: '$1'" ;;
        version_fmt)    echo "   格式要求: vX.Y 或 vX.Y.Z (例如 v1.0, v1.1)" ;;
        not_found)      echo "❌ 目标版本 '$1' 在 CHANGELOG.md 中未找到" ;;
        not_pub)        echo "   仅有 '## vX.Y' 条目的已发布版本可作为回滚目标。" ;;
        same_version)   echo "❌ 目标版本与当前版本相同 ($1) — 无需操作。" ;;
        not_backward)   echo "❌ 目标版本 ($1) 比当前版本 ($2) 更新。" ;;
        no_changelog)   echo "❌ 未找到 CHANGELOG.md: $1" ;;
        no_current)     echo "❌ 未找到 .current_system_version: $1" ;;

        # ── Dry-run preview ──
        pv_title)       echo "" ; echo "── 回滚预览 ──" ;;
        pv_current)     echo "  [预览] 当前版本: $1" ;;
        pv_target)      echo "  [预览] 目标版本: $1" ;;
        pv_path)        echo "  [预览] 回滚路径: $1 → $2（步长: $3）" ;;
        pv_versions)    echo "  [预览] 影响版本: $1" ;;
        pv_impact)      echo "  [预览] 影响范围: all agents ($1)" ;;
        pv_snap_ok)     echo "  [预览] 快照检查: memory/.sync_snapshots/$1_pre/ → 存在" ;;
        pv_snap_warn)   echo "  [预览] 快照检查: memory/.sync_snapshots/$1_pre/ → 缺失（警告：将使用文件清单回退）" ;;
        pv_manifest)    echo "  [预览] Revert manifest → 将写入 $1 个 agent 工作空间" ;;
        pv_summary)     echo "  [预览] 完成将更新 .current_system_version = $1" ;;

        # ── Real execution ──
        ex_title)       echo "" ; echo "── 回滚执行 ──" ;;
        ex_current)     echo "  当前版本: $1" ;;
        ex_target)      echo "  目标版本: $1" ;;
        ex_path)        echo "  回滚路径: $1 → $2（步长: $3）" ;;
        ex_snap_ok)     echo "  ✅ 快照: .sync_snapshots/$1_pre/ 存在" ;;
        ex_snap_warn)   echo "  ⚠️  快照: .sync_snapshots/$1_pre/ 缺失（将使用 CHANGELOG 文件清单回退）" ;;
        ex_manifest)    echo "  📄 清单已保存: $1/revert_sync_$2_$3.md" ;;
        ex_writing)     echo "  📝 写入 Agent: $1" ;;
        ex_agent_done)  echo "  ✅ Agent '$1' 已收到回滚清单" ;;
        ex_agent_skip)  echo "  ⚠️  Agent '$1' 工作空间不存在，已跳过" ;;
        ex_updated)     echo "  🔄 .current_system_version = $1" ;;
        ex_journal)     echo "  📋 日志记录已写入" ;;
        ex_complete)    echo "" ; echo "✅ 回滚已分发。各 Agent 将在下次 heartbeat 时从快照恢复。" ;;

        # ── Confirm prompt ──
        confirm_msg)    echo "" ; echo "⚠️  安全确认未通过" ;;
        confirm_hint)   echo "   首次运行请先使用 --dry-run 预览变更" ;;
        confirm_cmd)    echo "   确认无误后添加 --confirm 执行:" ;;
      esac
      ;;
  esac
}

# ── Help ───────────────────────────────────────────────────────────
show_help() {
  msg help1
  msg help2
  echo ""
  msg help3
  msg help4
  msg help5
  msg help5b
  msg help6
  msg help7
  echo ""
  echo "Examples:"
  echo "  # Preview rollback from v1.1 → v1.0"
  echo "  bash scripts/revert_sync.sh --dry-run ~/.openclaw/workspace-amaster/memory v1.0"
  echo ""
  echo "  # Execute rollback"
  echo "  bash scripts/revert_sync.sh --confirm ~/.openclaw/workspace-amaster/memory v1.0"
  echo ""
  echo "  # English output"
  echo "  bash scripts/revert_sync.sh --dry-run ~/.openclaw/workspace-amaster/memory v1.0 --lang en"
  exit 0
}

# ── Parse arguments (flags interleaved with positionals) ───────────
POS_ARGS=()
for arg in "$@"; do
  case "$arg" in
    -h|--help)   show_help ;;
    --dry-run)   DRY_RUN=true ;;
    --confirm)   CONFIRMED=true ;;
    --lang)      ;;  # value consumed by prev tracking below
    --lang=*)
      LANG="${arg#--lang=}"
      ;;
    *)
      if [ "$prev" = "--lang" ]; then
        LANG="$arg"
      else
        POS_ARGS+=("$arg")
      fi
      ;;
  esac
  prev="$arg"
done

# Validate language
case "$LANG" in
  en|zh) ;;
  *) LANG="zh" ;;
esac

# Extract positional args
MEMORY_DIR="${POS_ARGS[0]}"
TARGET_VER="${POS_ARGS[1]}"

# Expand ~ in path
MEMORY_DIR="${MEMORY_DIR/#\~/$HOME}"

msg title
[ "$DRY_RUN" = true ] && { msg dry_warn; echo ""; }
echo ""

# ── Missing args check ────────────────────────────────────────────
if [ -z "$MEMORY_DIR" ] || [ -z "$TARGET_VER" ]; then
  msg miss_args
  echo ""
  echo "  当前可用版本 (来自 CHANGELOG.md):"
  grep '^## v[0-9]' "$MEMORY_DIR/CHANGELOG.md" 2>/dev/null | sed 's/^/    /' || echo "    (CHANGELOG.md 不可用)"
  echo ""
  exit 1
fi

msg mem_dir "$MEMORY_DIR"

# ── Registry check ─────────────────────────────────────────────────
if [ ! -f "$REGISTRY_FILE" ]; then
  msg registry_err
  echo "  Looked in: $REGISTRY_FILE"
  exit 1
fi

# ── 1. CHANGELOG exists and target_version is published ───────────
CHANGELOG_FILE="$MEMORY_DIR/CHANGELOG.md"
if [ ! -f "$CHANGELOG_FILE" ]; then
  msg no_changelog "$CHANGELOG_FILE"
  exit 1
fi

if ! grep -q "^## $TARGET_VER " "$CHANGELOG_FILE"; then
  msg not_found "$TARGET_VER"
  msg not_pub
  echo ""
  echo "  已发布版本:"
  grep '^## v[0-9]' "$CHANGELOG_FILE" | sed 's/^/    /'
  exit 1
fi

# ── 2. Read current version ───────────────────────────────────────
CURRENT_FILE="$MEMORY_DIR/.current_system_version"
if [ ! -f "$CURRENT_FILE" ]; then
  msg no_current "$CURRENT_FILE"
  exit 1
fi

CURRENT_VER=$(cat "$CURRENT_FILE" | tr -d '[:space:]')

# ── 3. Version format validation ──────────────────────────────────
if ! echo "$TARGET_VER" | grep -qE "$VERSION_RE"; then
  msg invalid_target "$TARGET_VER"
  msg version_fmt
  exit 1
fi

# ── 4. Safety: target must not equal current ──────────────────────
if [ "$TARGET_VER" = "$CURRENT_VER" ]; then
  msg same_version "$CURRENT_VER"
  exit 1
fi

# ── 5. Safety: target must be < current (rollback goes backward) ──
if ! version_le "$TARGET_VER" "$CURRENT_VER"; then
  msg not_backward "$TARGET_VER" "$CURRENT_VER"
  exit 1
fi

# ── 6. Determine version chain (all versions between target and current) ──
VERSIONS_BETWEEN=""
while IFS= read -r line; do
  ver=$(echo "$line" | sed 's/^## \(v[0-9.]*\).*/\1/')
  # Collect versions: target < ver <= current
  if [ "$ver" = "$TARGET_VER" ] || [ "$ver" = "$CURRENT_VER" ]; then
    VERSIONS_BETWEEN="$VERSIONS_BETWEEN $ver"
  elif version_le "$TARGET_VER" "$ver" && version_le "$ver" "$CURRENT_VER"; then
    VERSIONS_BETWEEN="$VERSIONS_BETWEEN $ver"
  fi
done <<< "$(grep '^## v[0-9]' "$CHANGELOG_FILE")"

# Ensure target and current are included
VERSIONS_BETWEEN=$(echo "$TARGET_VER $VERSIONS_BETWEEN $CURRENT_VER" | tr ' ' '\n' | sort -t. -k1,1n -k2,2n -k3,3n | uniq | tr '\n' ' ')
VERSIONS_BETWEEN=$(echo "$VERSIONS_BETWEEN" | xargs)

# Count steps
STEP_COUNT=$(echo "$VERSIONS_BETWEEN" | wc -w)
STEP_COUNT=$((STEP_COUNT - 1))

# Versions display (between target and current, exclusive of target)
VERSIONS_DISPLAY=""
for v in $VERSIONS_BETWEEN; do
  if [ "$v" != "$TARGET_VER" ]; then
    VERSIONS_DISPLAY="$VERSIONS_DISPLAY $v"
  fi
done
VERSIONS_DISPLAY=$(echo "$VERSIONS_DISPLAY" | xargs)

# ── 7. Check snapshot existence ────────────────────────────────────
SNAPSHOT_DIR="$MEMORY_DIR/.sync_snapshots/${TARGET_VER}_pre"
SNAPSHOT_EXISTS=false
if [ -d "$SNAPSHOT_DIR" ] && [ -f "$SNAPSHOT_DIR/snapshot_manifest.json" ]; then
  SNAPSHOT_EXISTS=true
fi

# ── 8. Get agent list ─────────────────────────────────────────────
MASTER_AGENT=$(json_val "vars.master_agent" "$REGISTRY_FILE")
AGENT_IDS=""
AGENT_NAMES=""
while IFS= read -r agent_id; do
  [ -z "$agent_id" ] && continue
  AGENT_IDS="$AGENT_IDS $agent_id"
  aname=$(read_agent_name "$agent_id" "$LANG")
  [ -z "$aname" ] && aname="$agent_id"
  if [ -z "$AGENT_NAMES" ]; then
    AGENT_NAMES="$aname"
  else
    AGENT_NAMES="$AGENT_NAMES, $aname"
  fi
done <<< "$(read_agent_ids)"
AGENT_IDS=$(echo "$AGENT_IDS" | xargs)

WORKSPACE_ROOT=$(expand_path "$(json_val "vars.workspace_root" "$REGISTRY_FILE")")

AGENT_COUNT=0
for _ in $AGENT_IDS; do
  AGENT_COUNT=$((AGENT_COUNT + 1))
done

# ── Dry-run output ─────────────────────────────────────────────────
if [ "$DRY_RUN" = true ]; then
  msg pv_title
  msg pv_current "$CURRENT_VER"
  msg pv_target "$TARGET_VER"
  msg pv_path "$CURRENT_VER" "$TARGET_VER" "$STEP_COUNT"
  [ -n "$VERSIONS_DISPLAY" ] && msg pv_versions "$VERSIONS_DISPLAY"
  msg pv_impact "$AGENT_NAMES"
  if [ "$SNAPSHOT_EXISTS" = true ]; then
    msg pv_snap_ok "$TARGET_VER"
  else
    msg pv_snap_warn "$TARGET_VER"
  fi
  msg pv_manifest "$AGENT_COUNT"
  msg pv_summary "$TARGET_VER"
  echo ""
  exit 0
fi

# ── Confirm check (required for non-dry-run execution) ──────────────
if [ "$CONFIRMED" = false ]; then
  msg confirm_msg
  msg confirm_hint
  msg confirm_cmd
  echo "     bash scripts/revert_sync.sh --confirm $MEMORY_DIR $TARGET_VER ${LANG:+"--lang $LANG"}"
  echo ""
  exit 0
fi

# ── Path safety check ──────────────────────────────────────────────
case "$MEMORY_DIR" in
  $HOME/.openclaw/workspace-*/memory)  # allowed
    ;;
  *)
    echo "❌ 拒绝: $MEMORY_DIR (不在 ~/.openclaw/workspace-*/memory 范围内)"
    exit 1
    ;;
esac

# ── Execute rollback ───────────────────────────────────────────────
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
NOW_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
REVERT_SHA=$(echo "revert_sync_${CURRENT_VER}_to_${TARGET_VER}_${NOW_ISO}" | sha256sum | cut -c1-12)

msg ex_title
msg ex_current "$CURRENT_VER"
msg ex_target "$TARGET_VER"
msg ex_path "$CURRENT_VER" "$TARGET_VER" "$STEP_COUNT"
[ -n "$VERSIONS_DISPLAY" ] && msg pv_versions "$VERSIONS_DISPLAY"

# Backup current version file
if [ -f "$CURRENT_FILE" ]; then
  cp "$CURRENT_FILE" "${CURRENT_FILE}.bak.${BACKUP_TIMESTAMP}"
  echo "  📦 已备份: ${CURRENT_FILE}.bak.${BACKUP_TIMESTAMP}"
fi

# Snapshot status
if [ "$SNAPSHOT_EXISTS" = true ]; then
  msg ex_snap_ok "$TARGET_VER"
else
  msg ex_snap_warn "$TARGET_VER"
fi

# ── Create Revert Manifest (master copy) ──────────────────────────
REVERT_MANIFEST_BASENAME="revert_sync_${CURRENT_VER}_${REVERT_SHA}"
REVERT_MANIFEST_FILE="$MEMORY_DIR/${REVERT_MANIFEST_BASENAME}.md"

# Build affected versions section
AFFECTED_VERSIONS_MD=""
for v in $VERSIONS_BETWEEN; do
  if [ "$v" = "$TARGET_VER" ]; then
    AFFECTED_VERSIONS_MD="$AFFECTED_VERSIONS_MD- ✅ $v（目标版本，回滚终点）"$'\n'
  elif [ "$v" = "$CURRENT_VER" ]; then
    AFFECTED_VERSIONS_MD="$AFFECTED_VERSIONS_MD- ❌ $v（当前版本，回滚起点）"$'\n'
  else
    AFFECTED_VERSIONS_MD="$AFFECTED_VERSIONS_MD- 🔄 $v（中间版本，将被跳过）"$'\n'
  fi
done

# Extract impact from CHANGELOG entries
IMPACT_SUMMARY=""
for v in $VERSIONS_BETWEEN; do
  section=$(sed -n "/^## $v /,/^## v[0-9]/p" "$CHANGELOG_FILE" | head -50)
  impact=$(echo "$section" | grep -E '^\*\*影响范围\*\*|^\*\*Affected' | head -1 | sed 's/.*:\s*//')
  [ -n "$impact" ] && IMPACT_SUMMARY="$IMPACT_SUMMARY$v: $impact"$'\n'
done

if [ "$SNAPSHOT_EXISTS" = true ]; then
  SNAPSHOT_STATUS="✅ Snapshot exists"
  RESTORE_INSTRUCTIONS="从快照恢复: memory/.sync_snapshots/${TARGET_VER}_pre/"
else
  SNAPSHOT_STATUS="⚠️ NO snapshot — fallback: restore files from CHANGELOG impact list"
  RESTORE_INSTRUCTIONS="快照缺失，使用文件清单回退（可能不完整）"
fi

ISOLATED_AGENTS=""
for agent_id in $AGENT_IDS; do
  ISOLATED_AGENTS="$ISOLATED_AGENTS- ~~${agent_id}~~"$'\n'
done

cat > "$REVERT_MANIFEST_FILE" << REVERTEOF
# Revert Manifest — ${CURRENT_VER} → ${TARGET_VER}

**类型**: revert_sync
**回滚目标**: ${TARGET_VER}
**回滚起点**: ${CURRENT_VER}
**生成时间**: ${NOW_ISO}
**签名**: ${REVERT_SHA}
**发起人**: ${MASTER_AGENT}
**回滚类型**: full

## 版本链
回滚路径: ${CURRENT_VER} → ${TARGET_VER} (步长: ${STEP_COUNT})
${AFFECTED_VERSIONS_MD}
## 影响范围
${IMPACT_SUMMARY}
## 快照状态
${SNAPSHOT_STATUS}

## 受影响 Agent
${ISOLATED_AGENTS}
## 操作指令（Agent 端）
1. 检查快照: memory/.sync_snapshots/${TARGET_VER}_pre/
2. ${RESTORE_INSTRUCTIONS}
3. 验证 SHA256 checksums (参考 snapshot_manifest.json，如果存在)
4. 更新 memory/.agent_sync_version = ${TARGET_VER}
5. 删除本文件

## 验证清单
- [ ] CHANGELOG 回滚已完成
- [x] .current_system_version 已设为 ${TARGET_VER}
- [ ] 所有 pending_sync_*.md 文件已清理
- [ ] 所有 revert_sync_*.md 文件已处理
REVERTEOF

msg ex_manifest "$MEMORY_DIR" "$CURRENT_VER" "$REVERT_SHA"

# ── Dispatch revert manifest to each agent workspace ───────────────
for agent_id in $AGENT_IDS; do
  agent_ws=$(expand_path "$(read_agent_ws "$agent_id")")
  agent_ws=$(echo "$agent_ws" | xargs)

  # Path safety check
  case "$agent_ws" in
    $HOME/.openclaw/workspace-*) ;;
    *) continue ;;
  esac

  if [ ! -d "$agent_ws" ]; then
    msg ex_agent_skip "$agent_id"
    continue
  fi

  msg ex_writing "$agent_id"
  agent_revert_file="$agent_ws/${REVERT_MANIFEST_BASENAME}.md"
  _atomic_write "$agent_revert_file" "$(cat "$REVERT_MANIFEST_FILE")"
  msg ex_agent_done "$agent_id"
done

# ── Update .current_system_version = target_version ─────────────────
_atomic_write "$MEMORY_DIR/.current_system_version" "$TARGET_VER"
msg ex_updated "$TARGET_VER"

# ── Record journal entry ───────────────────────────────────────────
JOURNAL_FILE="$MEMORY_DIR/.sync_journal.jsonl"

# Build agents status for journal
JOURNAL_AGENTS=""
first_agent=true
for agent_id in $AGENT_IDS; do
  if [ "$first_agent" = true ]; then
    JOURNAL_AGENTS="\"$agent_id\": {\"status\": \"pending\", \"ts\": null}"
    first_agent=false
  else
    JOURNAL_AGENTS="$JOURNAL_AGENTS, \"$agent_id\": {\"status\": \"pending\", \"ts\": null}"
  fi
done

JOURNAL_ENTRY="{\"ts\":\"$NOW_ISO\",\"type\":\"revert\",\"from\":\"$CURRENT_VER\",\"to\":\"$TARGET_VER\",\"status\":\"reverted\",\"snapshot\":$SNAPSHOT_EXISTS,\"agents\":{$JOURNAL_AGENTS}}"
echo "$JOURNAL_ENTRY" >> "$JOURNAL_FILE"
msg ex_journal

# ── Complete ───────────────────────────────────────────────────────
msg ex_complete
echo ""
