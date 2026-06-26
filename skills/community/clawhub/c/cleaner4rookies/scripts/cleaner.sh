#!/bin/bash
# ============================================================
# openclaw-cleaner
# OpenClaw 临时文件自动清理脚本
# 用法：./cleaner.sh [--config FILE] [--force]
# ============================================================

# # 安全模式：mv/rm 等危险操作加显式 || ，不用 set -e 避免误杀 (disabled for debugging)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
WORKSPACE="${HOME}/.openclaw/workspace"
CONFIG_FILE=""
DRY_RUN=true
WHITELIST=()

# ---------- 参数 ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)  DRY_RUN=false; shift ;;
    --config) CONFIG_FILE="$2"; shift 2 ;;
    *)        echo "[cleaner] 未知参数: $1"; exit 1 ;;
  esac
done

# ---------- 找配置文件 ----------
find_config() {
  [[ -n "$CONFIG_FILE" && -f "$CONFIG_FILE" ]] && { echo "$CONFIG_FILE"; return; }
  [[ -f "${WORKSPACE}/cleaner.yaml" ]] && { echo "${WORKSPACE}/cleaner.yaml"; return; }
  [[ -f "${SKILL_ROOT}/config.yaml" ]] && { echo "${SKILL_ROOT}/config.yaml"; return; }
  echo ""
}

CONFIG=$(find_config)
if [[ -z "$CONFIG" ]]; then
  echo "[cleaner] ❌ 未找到配置文件"
  exit 1
fi

# ---------- 解析 YAML 简化版 ----------
# 读取单个 scalar 值（去掉引号和空格）
read_val() {
  local key="$1" line
  line=$(grep "^${key}:" "$CONFIG" 2>/dev/null | head -1 || true)
  line="${line#*:}"; line="${line//\"/}"; line="${line//\'/}"
  echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

ARCHIVE_DIR="$(read_val "archive_dir")"
ARCHIVE_DIR="${ARCHIVE_DIR//\~/${HOME}}"
[[ -z "$ARCHIVE_DIR" ]] && ARCHIVE_DIR="${WORKSPACE}/cleaner-archive"

DRY_RUN_STR="$(read_val "dry_run")"
[[ "$DRY_RUN_STR" == "false" ]] && DRY_RUN=false

# ---------- 解析白名单 ----------
WHITELIST=()
while IFS= read -r line; do
  line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  [[ "$line" == "whitelist:" ]] && continue
  WHITELIST+=("${line//\~/${HOME}}")
done < <(grep -A 20 "^whitelist:" "$CONFIG" 2>/dev/null || true)

# ---------- 白名单检查 ----------
is_whitelisted() {
  local f="$1"
  for w in "${WHITELIST[@]:-}"; do
    [[ "$f" == "$w" || "$f" == "$w"/* ]] && return 0
  done
  return 1
}

# ---------- 解析所有规则 ----------
# 输出格式：action|pattern|age_days|comment（每行一条规则）
parse_all_rules() {
  local in_rule=false
  local p_action="" p_pattern="" p_age="0" p_comment=""

  while IFS= read -r line; do
    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    [[ "$line" == "rules:" ]] && continue
    [[ "$line" == "whitelist:" ]] && break

    if [[ "$line" =~ ^-[[:space:]]*pattern:[[:space:]]*(.+) ]]; then
      # 上一条规则输出
      if $in_rule && [[ -n "$p_pattern" && -n "$p_action" ]]; then
        echo "${p_action}|${p_pattern}|${p_age}|${p_comment}"
      fi
      local raw_pattern="${BASH_REMATCH[1]}"
      # 去掉引号和通配符格式
      raw_pattern="${raw_pattern//\"/}"
      raw_pattern="${raw_pattern//\'/}"
      p_pattern="$raw_pattern"
      p_age="0"; p_comment=""; p_action=""
      in_rule=true
    elif $in_rule; then
      if [[ "$line" =~ ^action:[[:space:]]*(.+) ]]; then
        p_action="${BASH_REMATCH[1]}"
        p_action=$(echo "$p_action" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      elif [[ "$line" =~ ^age_days:[[:space:]]*(.+) ]]; then
        p_age="${BASH_REMATCH[1]}"
        p_age=$(echo "$p_age" | sed 's/[^0-9]//g')
        [[ -z "$p_age" ]] && p_age="0"
      elif [[ "$line" =~ ^comment:[[:space:]]*(.+) ]]; then
        p_comment="${BASH_REMATCH[1]}"
        p_comment=$(echo "$p_comment" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      fi
    fi
  done < "$CONFIG"

  if $in_rule && [[ -n "$p_pattern" && -n "$p_action" ]]; then
    echo "${p_action}|${p_pattern}|${p_age}|${p_comment}"
  fi
}

# ---------- 处理单条规则 ----------
process_rule() {
  local rule="$1"
  local action pattern age_days comment
  action="${rule%%|*}"
  local rest="${rule#*|}"
  pattern="${rest%%|*}"
  rest="${rest#*|}"
  age_days="${rest%%|*}"
  comment="${rest#*|}"

  # 确定搜索目录
  local search_dir="$WORKSPACE"
  local find_name=""
  if [[ "$pattern" == "media/inbound/*" ]]; then
    search_dir="$WORKSPACE/media/inbound"
    find_name="*"
  else
    # 去掉 glob 格式中的多余空格，保留 * 号
    find_name=$(echo "$pattern" | tr -s ' ' | sed 's/\*/\*/g')
  fi

  [[ ! -d "$search_dir" ]] && return 0

  # 用 find 找文件
  local file_list
  file_list=$(mktemp)
  if [[ "$find_name" == "*" ]]; then
    find "$search_dir" -maxdepth 1 -type f 2>/dev/null > "$file_list"
  else
    # 逐个 glob 模式查找
    for pat in $find_name; do
      find "$search_dir" -maxdepth 1 -name "$pat" -type f 2>/dev/null >> "$file_list"
    done
  fi

  # 按时间过滤
  local cutoff=""
  if [[ "$age_days" -gt 0 ]]; then
    cutoff=$(($(date +%s) - age_days * 86400))
  fi

  local count=0
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    is_whitelisted "$f" && continue
    if [[ -n "$cutoff" ]]; then
      local mtime
      mtime=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
      [[ "$mtime" -lt "$cutoff" ]] || continue
    fi
    count=$((count + 1))
    local fname basename; basename "$(basename "$f")" 2>/dev/null || basename="$f"
    local fsize; fsize=$(du -h "$f" 2>/dev/null | cut -f1 || echo "?")
    if [[ "$DRY_RUN" == "true" ]]; then
      echo "    🔍 [dry-run] $basename ($fsize)"
    else
      if [[ "$action" == "archive" ]]; then
        mkdir -p "$ARCHIVE_DIR"
        mv "$f" "${ARCHIVE_DIR}/" 2>/dev/null && echo "    ✅ 归档 $basename" || echo "    ❌ 归档失败 $basename"
      else
        rm -f "$f" && echo "    🗑  删除 $basename" || echo "    ❌ 删除失败 $basename"
      fi
    fi
  done < "$file_list"
  rm -f "$file_list"

  [[ $count -gt 0 ]] && echo "  [$comment] ($count 个文件)"
}

# ---------- 主流程 ----------
main() {
  local archive_rules=() delete_rules=()
  while IFS= read -r rule; do
    [[ -z "$rule" ]] && continue
    local act="${rule%%|*}"
    if [[ "$act" == "archive" ]]; then
      archive_rules+=("$rule")
    else
      delete_rules+=("$rule")
    fi
  done < <(parse_all_rules)

  echo "━━ 归档规则 ━━"
  for r in "${archive_rules[@]:-}"; do process_rule "$r"; done
  echo ""

  echo "━━ 删除规则 ━━"
  for r in "${delete_rules[@]:-}"; do process_rule "$r"; done
  echo ""

  echo "═══════════════════════════════════════════"
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  🔍 dry-run 完成，以上是预览结果"
    echo "  要真正执行？加 --force 参数"
  else
    echo "  ✅ 清理完成"
  fi
  echo "═══════════════════════════════════════════"
  echo ""

  if [[ -d "$ARCHIVE_DIR" ]]; then
    local asize; asize=$(du -sh "$ARCHIVE_DIR" 2>/dev/null | cut -f1 || echo "?")
    echo "  归档目录: $ARCHIVE_DIR ($asize)"
  fi
}

main
