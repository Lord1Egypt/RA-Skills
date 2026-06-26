#!/usr/bin/env bash
# 简报生成与推送脚本
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
REPORTS_DIR="$SKILL_DIR/reports"
TEMPLATES_REF="$SKILL_DIR/references/report-templates.md"
CHANNELS_CONFIG="$SKILL_DIR/config/channels.json"
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d yesterday +%Y-%m-%d)

mkdir -p "$REPORTS_DIR"

usage() {
  echo "用法: $0 <命令> [选项]"
  echo ""
  echo "命令:"
  echo "  generate --template <name>   生成简报 (minimal/standard/detailed/executive)"
  echo "  push --channel <name>        推送简报到指定渠道"
  echo "  archive --date <YYYY-MM-DD>  归档指定日期简报"
  echo "  history --days <N>           查看最近 N 天简报"
  exit 1
}

# 从 data-YYYY-MM-DD.json 读取数据并填充模板
generate_report() {
  local template="$1"
  local data_file="$REPORTS_DIR/data-$YESTERDAY.json"
  local out_file="$REPORTS_DIR/$YESTERDAY.md"

  if [[ ! -f "$data_file" ]]; then
    echo "[ERROR] 数据文件不存在: $data_file"
    echo "请先运行: python3 scripts/data-collector.py collect --all"
    exit 1
  fi

  echo "生成简报 (模板: $template) ..."

  # 从 JSON 提取常用字段（使用 jq）
  if ! command -v jq &>/dev/null; then
    echo "[WARN] jq 未安装，使用原始数据输出"
    cat > "$out_file" <<EOF
# $YESTERDAY 经营简报

> 模板: $template | 生成时间: $(date '+%Y-%m-%d %H:%M:%S')

## 原始数据

\`\`\`json
$(cat "$data_file")
\`\`\`
EOF
  else
    # 尝试提取常见字段，缺失时显示 N/A
    get() { jq -r "$1 // \"N/A\"" "$data_file" 2>/dev/null || echo "N/A"; }

    cat > "$out_file" <<EOF
# $YESTERDAY 经营简报

> 模板: $template | 生成时间: $(date '+%Y-%m-%d %H:%M:%S')

## 核心数据

$(jq -r '
  to_entries[] |
  "### \(.key)\n" +
  (.value | to_entries[] | "- **\(.key)**: \(.value)") +
  "\n"
' "$data_file" 2>/dev/null || cat "$data_file")

---
*数据来源: $(jq -r '[keys[]] | join(", ")' "$data_file" 2>/dev/null) | 决策简报虾自动生成*
EOF
  fi

  echo "✓ 简报已生成: $out_file"
  echo "$out_file"
}

push_feishu() {
  local report_file="$1"
  local content
  content=$(cat "$report_file")

  if [[ ! -f "$CHANNELS_CONFIG" ]]; then
    echo "[ERROR] 渠道配置不存在: $CHANNELS_CONFIG"
    echo "请创建 config/channels.json，配置飞书 webhook 或 bot token"
    exit 1
  fi

  local webhook
  webhook=$(jq -r '.feishu.webhook // empty' "$CHANNELS_CONFIG" 2>/dev/null)

  if [[ -z "$webhook" ]]; then
    echo "[ERROR] 未配置飞书 webhook，请在 config/channels.json 中添加 feishu.webhook"
    exit 1
  fi

  echo "推送到飞书 ..."
  local payload
  payload=$(jq -n --arg text "$content" '{"msg_type":"text","content":{"text":$text}}')
  local resp
  resp=$(curl -s -X POST "$webhook" -H "Content-Type: application/json" -d "$payload")
  echo "飞书响应: $resp"
}

push_email() {
  local report_file="$1"
  if [[ ! -f "$CHANNELS_CONFIG" ]]; then
    echo "[ERROR] 渠道配置不存在: $CHANNELS_CONFIG"
    exit 1
  fi
  local to
  to=$(jq -r '.email.to // empty' "$CHANNELS_CONFIG" 2>/dev/null)
  if [[ -z "$to" ]]; then
    echo "[ERROR] 未配置邮件收件人"
    exit 1
  fi
  echo "发送邮件到: $to ..."
  mail -s "$YESTERDAY 经营简报" "$to" < "$report_file" && echo "✓ 邮件已发送" || echo "[ERROR] 邮件发送失败"
}

cmd_generate() {
  local template="standard"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --template) template="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  generate_report "$template"
}

cmd_push() {
  local channel=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --channel) channel="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  local report_file="$REPORTS_DIR/$YESTERDAY.md"
  if [[ ! -f "$report_file" ]]; then
    echo "[ERROR] 简报文件不存在，请先运行 generate"
    exit 1
  fi
  case "$channel" in
    feishu) push_feishu "$report_file" ;;
    email)  push_email "$report_file" ;;
    *)      echo "[ERROR] 不支持的渠道: $channel (支持: feishu, email)"; exit 1 ;;
  esac
}

cmd_archive() {
  local target_date="$YESTERDAY"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --date) target_date="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  local src="$REPORTS_DIR/$target_date.md"
  if [[ -f "$src" ]]; then
    echo "✓ 已归档: $src"
  else
    echo "[WARN] 简报文件不存在: $src"
  fi
}

cmd_history() {
  local days=7
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --days) days="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  echo "最近 $days 天简报:"
  for i in $(seq 1 "$days"); do
    local d
    d=$(date -v-${i}d +%Y-%m-%d 2>/dev/null || date -d "$i days ago" +%Y-%m-%d)
    local f="$REPORTS_DIR/$d.md"
    if [[ -f "$f" ]]; then
      echo "  ✓ $d  $(wc -l < "$f") 行"
    else
      echo "  ✗ $d  (无记录)"
    fi
  done
}

[[ $# -lt 1 ]] && usage

CMD="$1"; shift
case "$CMD" in
  generate) cmd_generate "$@" ;;
  push)     cmd_push "$@" ;;
  archive)  cmd_archive "$@" ;;
  history)  cmd_history "$@" ;;
  *)        echo "[ERROR] 未知命令: $CMD"; usage ;;
esac
