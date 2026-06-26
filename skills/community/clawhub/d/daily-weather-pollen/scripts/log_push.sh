#!/bin/bash
# 记录花粉推送日志
# 用法: log_push.sh <状态> <天气> <花粉浓度> [异常信息]

LOG_FILE="$HOME/.openclaw/workspace/memory/pollen-push-log.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

STATUS="${1:-未知}"
WEATHER="${2:-}"
POLLEN="${3:-}"
ERROR="${4:-无}"

# 确保日志文件存在
if [ ! -f "$LOG_FILE" ]; then
    echo "日志文件不存在，请先初始化"
    exit 1
fi

# 状态图标
if [ "$STATUS" = "成功" ]; then
    STATUS_ICON="✅ 成功"
elif [ "$STATUS" = "失败" ]; then
    STATUS_ICON="❌ 失败"
elif [ "$STATUS" = "部分成功" ]; then
    STATUS_ICON="⚠️ 部分成功"
else
    STATUS_ICON="$STATUS"
fi

# 查找并更新待执行行
if grep -q "| - | 待执行 | - | - | - |" "$LOG_FILE"; then
    # 替换第一个待执行行
    sed -i "0,| - | 待执行 | - | - | - |/s||| $TIMESTAMP | $STATUS_ICON | $WEATHER | $POLLEN | $ERROR ||" "$LOG_FILE"
else
    # 追加新行（在分隔线前）
    sed -i "/<!-- 新记录追加到下方 -->/i | $TIMESTAMP | $STATUS_ICON | $WEATHER | $POLLEN | $ERROR |" "$LOG_FILE"
fi

echo "日志已记录: $TIMESTAMP - $STATUS_ICON"
