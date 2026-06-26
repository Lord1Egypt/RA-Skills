#!/bin/bash
# force_sync.sh — Trigger heartbeat sync detection immediately (v1.4)
# Usage: bash force_sync.sh [memory_dir] [old_version] [new_version] [--dry-run] [--lang en|zh]
# Example: bash force_sync.sh ~/.openclaw/workspace-amaster/memory v3.1 v3.2
#          bash force_sync.sh --dry-run ~/.openclaw/workspace-amaster/memory v3.1 v3.2
#
# v1.4: atomic writes for all sentinel files (prevents partial writes)

set -e

# ── Atomic write (prevents partial/corrupt sentinel files) ─────
_atomic_write() {
  local file="$1" content="$2"
  local tmp_file="${file}.tmp.$$"
  echo "$content" > "$tmp_file" && sync "$tmp_file" && mv "$tmp_file" "$file"
}

MEMORY_DIR=""
OLD_VER=""
NEW_VER=""
DRY_RUN=false
LANG="zh"
CONFIRMED=false

# Version format regex: v<MAJOR>.<MINOR>[.<PATCH>]
VERSION_RE='^v[0-9]+\.[0-9]+(\.[0-9]+)?$'

# ── Bilingual messages ─────────────────────────────────────────
msg() {
  local key="$1"; shift
  case "$LANG" in
    en)
      case "$key" in
        title)          echo "=== Force Sync Trigger v1.4 ===" ;;
        dry_warn)       echo "🔍 DRY-RUN MODE — no changes will be made" ;;
        mem_dir)        echo "Memory dir: $1" ;;
        usage)          echo "Usage: $0 <memory_dir> <old_version> <new_version> [--dry-run] [--lang en|zh]" ;;
        current_vers)   echo "Current versions:" ;;
        current_val)    echo "  current:    $1" ;;
        last_val)       echo "  last_sync:  $1" ;;
        force_hint)     echo "To force sync, run:" ;;
        force_example)  echo "  $0 $MEMORY_DIR v3.0 v3.1" ;;
        invalid_old)    echo "❌ Invalid old_version format: '$1'" ;;
        invalid_new)    echo "❌ Invalid new_version format: '$1'" ;;
        version_fmt)    echo "   Must match: vX.Y or vX.Y.Z (e.g., v3.0, v3.2.1)" ;;
        backup1)        echo "📦 Backed up: $1" ;;
        backup2)        echo "📦 Backed up: $1" ;;
        mismatch)       echo "✅ Version mismatch created:" ;;
        override)       echo "   .current_system_version = $1 (override)" ;;
        set_last)       echo "   .last_sync_version      = $1" ;;
        next)           echo "Next heartbeat will detect the mismatch and trigger sync." ;;
        dry_would1)     echo "[DRY-RUN] Would set .current_system_version = $1" ;;
        dry_would2)     echo "[DRY-RUN] Would set .last_sync_version = $1" ;;
        dry_backup1)    echo "[DRY-RUN] Would backup: $1" ;;
        dry_backup2)    echo "[DRY-RUN] Would backup: $1" ;;
        help1)          echo "Usage: bash force_sync.sh <memory_dir> <old_version> <new_version> [options]" ;;
        help2)          echo "  memory_dir    Path to memory directory (e.g. ~/.openclaw/workspace-amaster/memory)" ;;
        help3)          echo "  old_version   Current synced version (e.g. v3.0)" ;;
        help4)          echo "  new_version   Version to sync to (e.g. v3.1)" ;;
        help5)          echo "  --dry-run     Preview without making changes" ;;
        help5b)         echo "  --confirm     Required for real execution (skip with --dry-run)" ;;
        help6)          echo "  --lang en|zh  Output language (default: zh)" ;;
        help7)          echo "  -h, --help    Show this help" ;;
      esac
      ;;
    zh|*)
      case "$key" in
        title)          echo "=== 强制同步触发器 v1.4 ===" ;;
        dry_warn)       echo "🔍 预览模式 — 不会执行任何修改" ;;
        mem_dir)        echo "Memory 目录: $1" ;;
        usage)          echo "用法: $0 <memory_dir> <old_version> <new_version> [--dry-run] [--lang en|zh]" ;;
        current_vers)   echo "当前版本:" ;;
        current_val)    echo "  current:    $1" ;;
        last_val)       echo "  last_sync:  $1" ;;
        force_hint)     echo "强制同步请执行:" ;;
        force_example)  echo "  $0 $MEMORY_DIR v3.0 v3.1" ;;
        invalid_old)    echo "❌ old_version 格式无效: '$1'" ;;
        invalid_new)    echo "❌ new_version 格式无效: '$1'" ;;
        version_fmt)    echo "   格式要求: vX.Y 或 vX.Y.Z (例如 v3.0, v3.2.1)" ;;
        backup1)        echo "📦 已备份: $1" ;;
        backup2)        echo "📦 已备份: $1" ;;
        mismatch)       echo "✅ 版本差异已创建:" ;;
        override)       echo "   .current_system_version = $1 (覆盖)" ;;
        set_last)       echo "   .last_sync_version      = $1" ;;
        next)           echo "下次 heartbeat 将检测到差异并触发同步。" ;;
        dry_would1)     echo "[预览] 将设置 .current_system_version = $1" ;;
        dry_would2)     echo "[预览] 将设置 .last_sync_version = $1" ;;
        dry_backup1)    echo "[预览] 将备份: $1" ;;
        dry_backup2)    echo "[预览] 将备份: $1" ;;
        help1)          echo "用法: bash force_sync.sh <memory_dir> <old_version> <new_version> [选项]" ;;
        help2)          echo "  memory_dir    Memory 目录路径 (如 ~/.openclaw/workspace-amaster/memory)" ;;
        help3)          echo "  old_version   当前已同步版本 (如 v3.0)" ;;
        help4)          echo "  new_version   要同步到的目标版本 (如 v3.1)" ;;
        help5)          echo "  --dry-run     预览模式，不执行修改" ;;
        help5b)         echo "  --confirm     正式执行时必需 (--dry-run 模式下不需要)" ;;
        help6)          echo "  --lang en|zh  输出语言 (默认: zh)" ;;
        help7)          echo "  -h, --help    显示帮助" ;;
      esac
      ;;
  esac
}

# ── Help ───────────────────────────────────────────────────────
show_help() {
  msg help1
  echo ""
  msg help2
  msg help3
  msg help4
  msg help5
  msg help6
  msg help7
  exit 0
}

# ── Parse arguments (positional + flags interleaved) ───────────
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
MEMORY_DIR="${POS_ARGS[0]:-$HOME/.openclaw/workspace-amaster/memory}"
OLD_VER="${POS_ARGS[1]}"
NEW_VER="${POS_ARGS[2]}"

# Expand ~ in path
MEMORY_DIR="${MEMORY_DIR/#\~/$HOME}"

msg title
[ "$DRY_RUN" = true ] && { msg dry_warn; echo ""; }
msg mem_dir "$MEMORY_DIR"

# ── Missing args: show current state ─────────────────────────
if [ -z "$NEW_VER" ] || [ -z "$OLD_VER" ]; then
  msg usage
  echo ""
  msg current_vers
  msg current_val "$(cat "$MEMORY_DIR/.current_system_version" 2>/dev/null || echo 'N/A')"
  msg last_val "$(cat "$MEMORY_DIR/.last_sync_version" 2>/dev/null || echo 'N/A')"
  echo ""
  msg force_hint
  msg force_example
  exit 1
fi

# ── Version format validation ─────────────────────────────────
if ! echo "$OLD_VER" | grep -qE "$VERSION_RE"; then
  msg invalid_old "$OLD_VER"
  msg version_fmt
  exit 1
fi

if ! echo "$NEW_VER" | grep -qE "$VERSION_RE"; then
  msg invalid_new "$NEW_VER"
  msg version_fmt
  exit 1
fi

# ── Confirm check (required for non-dry-run execution) ─────────
if [ "$DRY_RUN" = false ] && [ "$CONFIRMED" = false ]; then
  echo ""
  echo "⚠️  安全确认未通过"
  echo "   首次运行请先使用 --dry-run 预览变更"
  echo "   确认无误后添加 --confirm 执行:"
  echo "     $0 $MEMORY_DIR $OLD_VER $NEW_VER --confirm ${LANG:+"--lang $LANG"}"
  echo ""
  exit 0
fi

# Path safety check — only allow ~/.openclaw/workspace-*/memory paths
case "$MEMORY_DIR" in
  $HOME/.openclaw/workspace-*/memory)  # allowed
    ;;
  *)
    echo "❌ 拒绝: $MEMORY_DIR (不在 ~/.openclaw/workspace-*/memory 范围内)"
    exit 1
    ;;
esac

# ── Execute ───────────────────────────────────────────────────
CURRENT_FILE="$MEMORY_DIR/.current_system_version"
LAST_SYNC_FILE="$MEMORY_DIR/.last_sync_version"
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ "$DRY_RUN" = true ]; then
  # Dry-run: show what would happen
  if [ -f "$CURRENT_FILE" ]; then
    msg dry_backup1 "${CURRENT_FILE}.bak.${BACKUP_TIMESTAMP}"
  fi
  if [ -f "$LAST_SYNC_FILE" ]; then
    msg dry_backup2 "${LAST_SYNC_FILE}.bak.${BACKUP_TIMESTAMP}"
  fi
  msg dry_would1 "$NEW_VER"
  msg dry_would2 "$OLD_VER"
  echo ""
  msg next
  exit 0
fi

# Backup existing files
if [ -f "$CURRENT_FILE" ]; then
  cp "$CURRENT_FILE" "${CURRENT_FILE}.bak.${BACKUP_TIMESTAMP}"
  msg backup1 "${CURRENT_FILE}.bak.${BACKUP_TIMESTAMP}"
fi

if [ -f "$LAST_SYNC_FILE" ]; then
  cp "$LAST_SYNC_FILE" "${LAST_SYNC_FILE}.bak.${BACKUP_TIMESTAMP}"
  msg backup2 "${LAST_SYNC_FILE}.bak.${BACKUP_TIMESTAMP}"
fi

# Override versions (atomic write)
_atomic_write "$MEMORY_DIR/.current_system_version" "$NEW_VER"
_atomic_write "$MEMORY_DIR/.last_sync_version" "$OLD_VER"

echo ""
msg mismatch
msg override "$NEW_VER"
msg set_last "$OLD_VER"
echo ""
msg next
