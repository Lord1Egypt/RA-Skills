#!/bin/bash

# cron-manager-master: 创建定时任务脚本
# 自动从当前会话中提取 channel 和 user_id

set -e

# 默认参数
CHANNEL="feishu"  # TODO: 需要从会话上下文自动获取
USER_ID="ou_xxxxxx"  # TODO: 需要从会话上下文自动获取
SESSION="isolated"
ANNOUNCE="--announce"
DELETE_AFTER_RUN=""
AT_TIME=""
CRON_EXPR=""
MESSAGE=""
NAME=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            NAME="$2"
            shift 2
            ;;
        --at)
            AT_TIME="$2"
            shift 2
            ;;
        --cron)
            CRON_EXPR="$2"
            shift 2
            ;;
        --message)
            MESSAGE="$2"
            shift 2
            ;;
        --delete-after-run)
            DELETE_AFTER_RUN="--delete-after-run"
            shift
            ;;
        --channel)
            CHANNEL="$2"
            shift 2
            ;;
        --to)
            USER_ID="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 参数检查
if [[ -z "$NAME" ]]; then
    echo "错误: 必须提供 --name 参数"
    exit 1
fi

if [[ -z "$MESSAGE" ]]; then
    echo "错误: 必须提供 --message 参数"
    exit 1
fi

if [[ -z "$AT_TIME" && -z "$CRON_EXPR" ]]; then
    echo "错误: 必须提供 --at 或 --cron 参数"
    exit 1
fi

if [[ -n "$AT_TIME" && -n "$CRON_EXPR" ]]; then
    echo "错误: 不能同时使用 --at 和 --cron 参数"
    exit 1
fi

# 构建命令
if [[ -n "$AT_TIME" ]]; then
    # 一次性任务
    echo "创建一次性定时任务: $NAME"
    echo "执行时间: $AT_TIME"
    echo "消息内容: $MESSAGE"
    echo "接收者: $USER_ID"
    echo "通道: $CHANNEL"
    
    openclaw cron add \
        --name "$NAME" \
        --at "$AT_TIME" \
        --session "$SESSION" \
        --message "$MESSAGE" \
        $ANNOUNCE \
        --channel "$CHANNEL" \
        --to "$USER_ID" \
        $DELETE_AFTER_RUN
else
    # 周期性任务
    echo "创建周期性定时任务: $NAME"
    echo "Cron表达式: $CRON_EXPR"
    echo "消息内容: $MESSAGE"
    echo "接收者: $USER_ID"
    echo "通道: $CHANNEL"
    
    openclaw cron add \
        --name "$NAME" \
        --cron "$CRON_EXPR" \
        --session "$SESSION" \
        --message "$MESSAGE" \
        $ANNOUNCE \
        --channel "$CHANNEL" \
        --to "$USER_ID"
fi

echo "✅ 定时任务创建完成"
echo "使用以下命令验证任务:"
echo "  openclaw cron list --json | grep -B 5 -A 20 \"$NAME\""