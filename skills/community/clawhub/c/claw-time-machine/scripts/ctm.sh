#!/usr/bin/env bash
# OpenClaw Time Machine - backup, restore, and migrate preserved state.

set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.ctm}"
ACTION=""
BACKUP_FILE=""
FORCE=0
DRY_RUN=0
REMOTE_DIR="~/.openclaw"
CLEAN_REMOTE_ARCHIVE=0
SCRIPT_NAME="$(basename "$0")"
SAFETY_PATH=""

SOUL_FILES=(
  "workspace"
  "credentials"
  "telegram"
  "skills"
  "cron"
  "openclaw.json"
  "identity"
)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ${NC}  $1"; }
log_ok() { echo -e "${GREEN}✓${NC}  $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
log_error() { echo -e "${RED}✗${NC}  $1" >&2; }

die() {
  log_error "$1"
  exit 1
}

usage() {
  cat <<EOF
🕐 OpenClaw Time Machine

Usage:
  $SCRIPT_NAME backup [filename] [--dry-run]
  $SCRIPT_NAME list
  $SCRIPT_NAME restore <index|filename|latest> [--force]
  $SCRIPT_NAME migrate <user@host> [--remote-dir <dir>] [--clean-remote-archive] [--force]

Commands:
  backup     Create a backup in $BACKUP_DIR
  list       List backups, newest first
  restore    Restore by index, filename, or 'latest'
  migrate    Create a fresh backup, copy it to a remote host, and restore there

Options:
  --force                  Skip interactive confirmation for destructive actions
  --dry-run                Show what would be backed up without creating an archive
  --remote-dir <dir>       Remote OpenClaw directory for migrate (default: ~/.openclaw)
  --clean-remote-archive   Delete the copied backup archive from the remote host after restore
EOF
}

require_cmd() {
  local missing=0
  for cmd in "$@"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      log_error "缺少依赖: $cmd"
      missing=1
    fi
  done
  (( missing == 0 )) || exit 1
}

ensure_backup_dir() {
  mkdir -p "$BACKUP_DIR"
}

generate_filename() {
  echo "openclaw-soul-$(date +%Y%m%d-%H%M%S).tar.gz"
}

collect_existing_items() {
  local item
  for item in "${SOUL_FILES[@]}"; do
    if [[ -e "$OPENCLAW_DIR/$item" ]]; then
      echo "$item"
    fi
  done
}

create_manifest() {
  local manifest
  manifest=$(mktemp)
  collect_existing_items > "$manifest"
  echo "$manifest"
}

list_backup_files() {
  ensure_backup_dir
  find "$BACKUP_DIR" -maxdepth 1 -type f -name 'openclaw-soul-*.tar.gz' -printf '%f\n' | sort -r
}

resolve_backup_file() {
  local input="${1:-}"
  [[ -n "$input" ]] || return 1

  if [[ "$input" == "latest" ]]; then
    local latest
    latest=$(list_backup_files | head -n 1)
    [[ -n "$latest" ]] || die "还没有备份可恢复"
    echo "$BACKUP_DIR/$latest"
    return 0
  fi

  local idx
  idx=$(echo "$input" | sed 's/\[//g; s/\]//g')
  if [[ "$idx" =~ ^[0-9]+$ ]]; then
    local selected
    selected=$(list_backup_files | sed -n "${idx}p")
    [[ -n "$selected" ]] || die "无效的备份序号: $idx"
    echo "$BACKUP_DIR/$selected"
    return 0
  fi

  if [[ -f "$input" ]]; then
    echo "$input"
    return 0
  fi

  if [[ -f "$BACKUP_DIR/$input" ]]; then
    echo "$BACKUP_DIR/$input"
    return 0
  fi

  return 1
}

confirm_or_exit() {
  local message="$1"
  if (( FORCE == 1 )); then
    log_warn "$message -- 已使用 --force，跳过确认"
    return 0
  fi

  echo
  log_warn "$message"
  read -r -p "继续? (yes/no): " confirm
  [[ "$confirm" == "yes" ]] || die "已取消"
}

create_safety_backup() {
  local manifest
  manifest=$(create_manifest)
  if [[ ! -s "$manifest" ]]; then
    rm -f "$manifest"
    log_info "当前没有可做安全备份的现有状态"
    return 0
  fi

  SAFETY_PATH="${OPENCLAW_DIR}.bak.$(date +%s)"
  mkdir -p "$SAFETY_PATH"
  log_info "创建安全备份: $SAFETY_PATH"

  while IFS= read -r item; do
    mkdir -p "$SAFETY_PATH/$(dirname "$item")"
    cp -a "$OPENCLAW_DIR/$item" "$SAFETY_PATH/$item"
  done < "$manifest"

  rm -f "$manifest"
}

remove_soul_items() {
  local item
  for item in "${SOUL_FILES[@]}"; do
    if [[ -e "$OPENCLAW_DIR/$item" ]]; then
      rm -rf -- "$OPENCLAW_DIR/$item"
    fi
  done
}

build_manifest_file() {
  local manifest_source="$1"
  local bundle_dir="$2"
  local manifest_target="$bundle_dir/manifest.txt"
  {
    echo "# Claw Time Machine backup manifest"
    echo "created_at=$(date -Iseconds)"
    echo "openclaw_dir=$OPENCLAW_DIR"
    echo "backup_dir=$BACKUP_DIR"
    echo "items="
    sed 's/^/ - /' "$manifest_source"
  } > "$manifest_target"
}

backup() {
  require_cmd tar mktemp du cp
  ensure_backup_dir

  local output_name="${BACKUP_FILE:-$(generate_filename)}"
  local output_file="$BACKUP_DIR/$output_name"
  local manifest bundle_dir
  manifest=$(create_manifest)

  if [[ ! -s "$manifest" ]]; then
    rm -f "$manifest"
    die "没有找到可备份的 OpenClaw 状态路径: $OPENCLAW_DIR"
  fi

  if (( DRY_RUN == 1 )); then
    log_info "Dry run: 将备份以下路径"
    sed 's/^/  - /' "$manifest"
    rm -f "$manifest"
    return 0
  fi

  bundle_dir=$(mktemp -d)
  while IFS= read -r item; do
    mkdir -p "$bundle_dir/$(dirname "$item")"
    cp -a "$OPENCLAW_DIR/$item" "$bundle_dir/$item"
  done < "$manifest"
  build_manifest_file "$manifest" "$bundle_dir"

  log_info "正在创建备份: $output_file"
  tar czf "$output_file" -C "$bundle_dir" .

  rm -rf "$bundle_dir"
  rm -f "$manifest"

  tar tzf "$output_file" >/dev/null
  local size
  size=$(du -h "$output_file" | cut -f1)
  log_ok "备份完成: $output_file ($size)"
}

list_backups() {
  require_cmd find sort du stat

  local files
  files=$(list_backup_files)
  if [[ -z "$files" ]]; then
    echo
    echo "📭 暂无备份"
    echo
    echo "💡 创建备份: $SCRIPT_NAME backup"
    return 0
  fi

  echo
  echo "📦 OpenClaw 备份列表（最新在前）"
  echo "════════════════════════════════════════════════════"
  echo

  local count=0
  local total_size=0
  local idx=1
  local filename file size size_bytes datetime_raw date_part time_part datetime

  while IFS= read -r filename; do
    [[ -n "$filename" ]] || continue
    file="$BACKUP_DIR/$filename"
    size=$(du -h "$file" | cut -f1)
    size_bytes=$(stat -c%s "$file")
    total_size=$((total_size + size_bytes))

    datetime_raw=$(echo "$filename" | grep -oE '[0-9]{8}-[0-9]{6}' || true)
    if [[ -n "$datetime_raw" ]]; then
      date_part="$(echo "$datetime_raw" | cut -c1-4)-$(echo "$datetime_raw" | cut -c5-6)-$(echo "$datetime_raw" | cut -c7-8)"
      time_part="$(echo "$datetime_raw" | cut -c10-11):$(echo "$datetime_raw" | cut -c12-13):$(echo "$datetime_raw" | cut -c14-15)"
      datetime="$date_part $time_part"
    else
      datetime="未知时间"
    fi

    echo "  [$idx] 📅 $datetime  💾 $size"
    echo "      $filename"
    if (( idx == 1 )); then
      echo "      最新备份"
    fi
    echo

    idx=$((idx + 1))
    count=$((count + 1))
  done <<< "$files"

  echo "════════════════════════════════════════════════════"
  if command -v numfmt >/dev/null 2>&1; then
    echo "📊 共 $count 个备份，总计 $(numfmt --to=iec "$total_size")"
  else
    echo "📊 共 $count 个备份，总计 ${total_size}B"
  fi
  echo
  echo "💡 恢复最新备份: $SCRIPT_NAME restore latest"
  echo "💡 按序号恢复:   $SCRIPT_NAME restore 1"
}

restore() {
  require_cmd tar
  [[ -n "$BACKUP_FILE" ]] || die "请指定备份序号、文件名或 latest"

  local full_path
  full_path=$(resolve_backup_file "$BACKUP_FILE") || die "备份文件不存在: $BACKUP_FILE"
  [[ -f "$full_path" ]] || die "备份文件不存在: $full_path"

  tar tzf "$full_path" >/dev/null

  confirm_or_exit "这会覆盖当前 OpenClaw 保留状态路径"
  mkdir -p "$OPENCLAW_DIR"
  create_safety_backup

  log_info "清理现有保留状态..."
  remove_soul_items

  log_info "从备份恢复: $full_path"
  tar xzf "$full_path" -C "$OPENCLAW_DIR"

  log_ok "恢复完成"
  if [[ -n "$SAFETY_PATH" ]]; then
    log_info "安全备份路径: $SAFETY_PATH"
  fi
  log_info "如需启动服务: openclaw gateway start"
}

migrate() {
  require_cmd tar scp ssh mktemp
  local target_host="$BACKUP_FILE"
  [[ -n "$target_host" ]] || die "请指定目标服务器，例如: $SCRIPT_NAME migrate user@host"

  log_info "准备迁移到: $target_host"
  local filename
  filename=$(generate_filename)
  local original_backup_file="${BACKUP_FILE:-}"
  BACKUP_FILE="$filename"
  backup
  BACKUP_FILE="$original_backup_file"

  local full_path="$BACKUP_DIR/$filename"
  [[ -f "$full_path" ]] || die "迁移前创建备份失败: $full_path"

  log_info "复制备份到目标服务器..."
  scp "$full_path" "${target_host}:~/"

  confirm_or_exit "即将在目标服务器上覆盖保留状态路径: $REMOTE_DIR"

  local remote_script
  remote_script=$(cat <<'EOS'
set -euo pipefail
REMOTE_DIR="__REMOTE_DIR__"
ARCHIVE="__ARCHIVE__"
FORCE="__FORCE__"
CLEAN_REMOTE_ARCHIVE="__CLEAN_REMOTE_ARCHIVE__"
SOUL_ITEMS="workspace credentials telegram skills cron openclaw.json identity"
SAFETY_DIR="${REMOTE_DIR}.bak.$(date +%s)"

confirm_or_exit() {
  local message="$1"
  if [[ "$FORCE" == "1" ]]; then
    printf '%s\n' "$message -- force mode enabled"
    return 0
  fi
  printf '%s\n' "$message"
  read -r -p "Continue? (yes/no): " ans
  [[ "$ans" == "yes" ]]
}

command -v tar >/dev/null 2>&1 || { echo "Missing dependency: tar" >&2; exit 1; }
mkdir -p "$REMOTE_DIR"
tar tzf "$ARCHIVE" >/dev/null

if ! confirm_or_exit "Remote restore will overwrite preserved state in $REMOTE_DIR"; then
  echo "Cancelled"
  exit 1
fi

if [ -d "$REMOTE_DIR" ]; then
  mkdir -p "$SAFETY_DIR"
  for item in $SOUL_ITEMS; do
    if [ -e "$REMOTE_DIR/$item" ]; then
      mkdir -p "$SAFETY_DIR/$(dirname "$item")"
      cp -a "$REMOTE_DIR/$item" "$SAFETY_DIR/$item"
    fi
  done
fi

for item in $SOUL_ITEMS; do
  if [ -e "$REMOTE_DIR/$item" ]; then
    rm -rf -- "$REMOTE_DIR/$item"
  fi
done

tar xzf "$ARCHIVE" -C "$REMOTE_DIR"

echo "Gateway start was not automated; start it manually on the remote host if needed"

if [[ "$CLEAN_REMOTE_ARCHIVE" == "1" ]]; then
  rm -f -- "$ARCHIVE"
fi

echo "Remote restore complete"
echo "Safety backup: $SAFETY_DIR"
if [[ "$CLEAN_REMOTE_ARCHIVE" == "1" ]]; then
  echo "Remote archive deleted: $ARCHIVE"
else
  echo "Remote archive kept: $ARCHIVE"
fi
EOS
)

  remote_script=${remote_script//__REMOTE_DIR__/$REMOTE_DIR}
  remote_script=${remote_script//__ARCHIVE__/~\/$filename}
  remote_script=${remote_script//__FORCE__/$FORCE}
  remote_script=${remote_script//__CLEAN_REMOTE_ARCHIVE__/$CLEAN_REMOTE_ARCHIVE}

  log_info "在目标服务器执行恢复..."
  ssh "$target_host" "bash -s" <<< "$remote_script"
  log_ok "迁移完成: $target_host"
  if (( CLEAN_REMOTE_ARCHIVE == 1 )); then
    log_info "远端备份文件已清理"
  else
    log_info "远端备份文件: ~/$filename"
  fi
}

parse_args() {
  [[ $# -gt 0 ]] || {
    usage
    exit 1
  }

  ACTION="$1"
  shift

  case "$ACTION" in
    backup)
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --dry-run)
            DRY_RUN=1
            shift
            ;;
          --force)
            FORCE=1
            shift
            ;;
          -h|--help)
            usage
            exit 0
            ;;
          *)
            if [[ -z "$BACKUP_FILE" ]]; then
              BACKUP_FILE="$1"
              shift
            else
              die "未知参数: $1"
            fi
            ;;
        esac
      done
      ;;
    list)
      while [[ $# -gt 0 ]]; do
        case "$1" in
          -h|--help)
            usage
            exit 0
            ;;
          *)
            die "list 不接受参数: $1"
            ;;
        esac
      done
      ;;
    restore)
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --force)
            FORCE=1
            shift
            ;;
          -h|--help)
            usage
            exit 0
            ;;
          *)
            if [[ -z "$BACKUP_FILE" ]]; then
              BACKUP_FILE="$1"
              shift
            else
              die "未知参数: $1"
            fi
            ;;
        esac
      done
      ;;
    migrate)
      while [[ $# -gt 0 ]]; do
        case "$1" in
          --force)
            FORCE=1
            shift
            ;;
          --remote-dir)
            shift
            [[ $# -gt 0 ]] || die "--remote-dir 需要一个路径参数"
            REMOTE_DIR="$1"
            shift
            ;;
          --clean-remote-archive)
            CLEAN_REMOTE_ARCHIVE=1
            shift
            ;;
          -h|--help)
            usage
            exit 0
            ;;
          *)
            if [[ -z "$BACKUP_FILE" ]]; then
              BACKUP_FILE="$1"
              shift
            else
              die "未知参数: $1"
            fi
            ;;
        esac
      done
      ;;
    -h|--help|help)
      usage
      exit 0
      ;;
    *)
      usage
      exit 1
      ;;
  esac
}

main() {
  parse_args "$@"
  case "$ACTION" in
    backup) backup ;;
    list) list_backups ;;
    restore) restore ;;
    migrate) migrate ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
