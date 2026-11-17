#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_SRC="$(cd -- "$SCRIPT_DIR/.." && pwd)"
SRC="${F_DESIGN_SRC:-$DEFAULT_SRC}"
SRC_REAL="$(realpath "$SRC")"
TARGET_HOME="${F_DESIGN_TARGET_HOME:-$HOME}"
LOCALE="${F_DESIGN_LOCALE:-${LC_ALL:-${LANG:-en}}}"
case "${LOCALE,,}" in
  zh|zh-cn|zh_cn|zh-cn.*) LOCALE="zh-CN" ;;
  *) LOCALE="en" ;;
esac
if [[ "${1:-}" == "--locale" && -n "${2:-}" ]]; then
  case "${2,,}" in
    zh|zh-cn|zh_cn) LOCALE="zh-CN" ;;
    en|en-us|en_us) LOCALE="en" ;;
    *) LOCALE="en" ;;
  esac
fi
msg() {
  local key="$1"
  if [[ "$LOCALE" == "zh-CN" ]]; then
    case "$key" in
      missing-source) echo "缺少源 skill：$SRC_REAL/SKILL.md" ;;
      missing-rsync) echo "缺少必需命令：rsync" ;;
      skipped) echo "已跳过源目录目标 $2" ;;
      refusing) echo "拒绝同步到源目录的子目录：$2" ;;
      synced) echo "已同步 $2" ;;
    esac
  else
    case "$key" in
      missing-source) echo "Missing source skill: $SRC_REAL/SKILL.md" ;;
      missing-rsync) echo "Missing required command: rsync" ;;
      skipped) echo "Skipped source target $2" ;;
      refusing) echo "Refusing to sync into a subdirectory of source: $2" ;;
      synced) echo "Synced $2" ;;
    esac
  fi
}
TARGETS=(
  "${TARGET_HOME}/.codex/skills/design-guide"
  "${TARGET_HOME}/.claude/skills/design-guide"
  "${TARGET_HOME}/.cursor/skills/design-guide"
  "${TARGET_HOME}/.qwen/skills/design-guide"
)
DOCTOR="$SRC_REAL/scripts/design-guide-doctor.py"

if [[ ! -f "$SRC_REAL/SKILL.md" ]]; then
  msg missing-source >&2
  exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
  msg missing-rsync >&2
  exit 1
fi

for target in "${TARGETS[@]}"; do
  target_real="$(realpath -m "$target")"

  if [[ "$target_real" == "$SRC_REAL" ]]; then
    msg skipped "$target_real"
    continue
  fi

  if [[ "$target_real/" == "$SRC_REAL/"* ]]; then
    msg refusing "$target_real" >&2
    exit 1
  fi

  mkdir -p "$(dirname "$target")"
  mkdir -p "$target"
  rsync -a --delete --delete-excluded \
    --exclude='.git/' \
    --exclude='.github/' \
    --exclude='.codex/' \
    --exclude='promo/' \
    --exclude='.design-guide/profile.md' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='*.tmp' \
    "$SRC_REAL/" "$target_real/"
  msg synced "$target_real"
done

if [[ -f "$DOCTOR" ]]; then
  python3 "$DOCTOR" --source "$SRC_REAL" --target-home "$TARGET_HOME" --strict --locale "$LOCALE"
fi
