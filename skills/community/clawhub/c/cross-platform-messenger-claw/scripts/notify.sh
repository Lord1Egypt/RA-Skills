#!/usr/bin/env bash
# notify.sh — 跨平台消息推送脚本
# 用法: ./notify.sh --channel <渠道> --target <目标> --message <消息> [--media <路径>]
#
# 示例:
#   ./notify.sh --channel feishu --target ou_xxx --message "报警：CPU 超过 90%"
#   ./notify.sh --channel telegram --target @mygroup --message "日报已生成" --media ./report.pdf
#   ./notify.sh --channel whatsapp --target +8613800138000 --message "紧急通知"
#
# 批量推送:
#   cat targets.txt | ./notify.sh --channel feishu --message "群发通知"

set -euo pipefail

CHANNEL=""
TARGET=""
MESSAGE=""
MEDIA=""
SILENT=false
DRY_RUN=false
VERBOSE=false

usage() {
  cat <<EOF
用法: notify.sh [选项]

选项:
  -c, --channel <渠道>     消息渠道 (feishu/telegram/whatsapp/discord/slack/signal/imessage 等)
  -t, --target <目标>      接收者 (号码/ID/用户名，参考 channels.md)
  -m, --message <消息>     消息正文
  --media <路径>           附件路径或 URL
  --silent                 静默发送 (Telegram/Discord)
  --dry-run                仅打印命令，不实际发送
  -v, --verbose            详细输出
  -h, --help               显示帮助

标准输入: 如果未指定 --target，从 stdin 逐行读取目标列表（每行一个）

示例:
  # 单条推送
  ./notify.sh -c feishu -t ou_xxx -m "报警信息"

  # 带附件
  ./notify.sh -c telegram -t @channel -m "日报" --media ./report.pdf

  # 批量推送（从文件）
  ./notify.sh -c feishu -m "群发通知" < targets.txt
EOF
  exit 0
}

# 解析参数
while [[ $# -gt 0 ]]; do
  case "$1" in
    -c|--channel) CHANNEL="$2"; shift 2 ;;
    -t|--target)  TARGET="$2"; shift 2 ;;
    -m|--message) MESSAGE="$2"; shift 2 ;;
    --media)      MEDIA="$2"; shift 2 ;;
    --silent)     SILENT=true; shift ;;
    --dry-run)    DRY_RUN=true; shift ;;
    -v|--verbose) VERBOSE=true; shift ;;
    -h|--help)    usage ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

# 校验必填参数
if [[ -z "$CHANNEL" ]]; then
  echo "❌ 缺少 --channel 参数"
  exit 1
fi

if [[ -z "$MESSAGE" ]]; then
  echo "❌ 缺少 --message 参数"
  exit 1
fi

# 构建基础命令
build_cmd() {
  local target="$1"
  local cmd=(openclaw message send --channel "$CHANNEL" --target "$target" --message "$MESSAGE")

  if [[ -n "$MEDIA" ]]; then
    cmd+=(--media "$MEDIA")
  fi
  if [[ "$SILENT" == true ]]; then
    cmd+=(--silent)
  fi
  if [[ "$DRY_RUN" == true ]]; then
    cmd+=(--dry-run)
  fi
  if [[ "$VERBOSE" == true ]]; then
    cmd+=(--verbose)
  fi

  echo "${cmd[@]}"
}

# 发送单条
send_one() {
  local target="$1"
  local cmd
  cmd=$(build_cmd "$target")

  if [[ "$VERBOSE" == true ]]; then
    echo "📤 发送到 $CHANNEL:$target"
  fi

  eval "$cmd"
}

# 如果指定了 target，单条发送
if [[ -n "$TARGET" ]]; then
  send_one "$TARGET"
  exit 0
fi

# 否则从 stdin 读取目标列表，逐行发送
count=0
failed=0
while IFS= read -r line || [[ -n "$line" ]]; do
  # 跳过空行和注释
  line=$(echo "$line" | xargs)
  [[ -z "$line" || "$line" == \#* ]] && continue

  count=$((count + 1))
  if send_one "$line"; then
    :
  else
    echo "⚠️ 发送到 $line 失败"
    failed=$((failed + 1))
  fi
  # 间隔 1 秒避免频率限制
  sleep 1
done

echo "✅ 完成: $count 条发送, $failed 条失败"
