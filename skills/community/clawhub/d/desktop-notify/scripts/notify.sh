#!/usr/bin/env bash
# desktop-notify for macOS / Linux
# 用法: bash notify.sh "<内容>" "<标题>"
#   $1 = 内容 (默认: 任务完成，请查看)
#   $2 = 标题 (默认: WorkBuddy)

MESSAGE="${1:-任务完成，请查看}"
TITLE="${2:-WorkBuddy}"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: 通知中心
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\""
    echo "通知已发送 (macOS)"
elif command -v notify-send >/dev/null 2>&1; then
    # Linux: libnotify
    notify-send "$TITLE" "$MESSAGE"
    echo "通知已发送 (Linux)"
else
    # 降级：终端响铃 + 打印
    printf '\a'
    echo "[$TITLE] $MESSAGE"
    echo "notify-send 未安装，已用终端响铃替代"
fi
