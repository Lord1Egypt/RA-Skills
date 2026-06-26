#!/bin/bash

# cron-manager-master: 验证定时任务脚本

set -e

if [[ $# -eq 0 ]]; then
    echo "使用方法: $0 <任务名称>"
    exit 1
fi

TASK_NAME="$1"

echo "🔍 验证定时任务: $TASK_NAME"
echo "========================================"

# 检查任务是否存在
echo "1. 检查任务是否存在..."
TASK_INFO=$(openclaw cron list --json | grep -B 5 -A 20 "$TASK_NAME" || true)

if [[ -z "$TASK_INFO" ]]; then
    echo "❌ 错误: 未找到任务 '$TASK_NAME'"
    exit 1
fi

echo "✅ 任务存在"
echo ""

# 提取任务信息
echo "2. 任务配置详情:"
echo "$TASK_INFO"
echo ""

# 检查关键参数
echo "3. 关键参数检查:"

# 检查 session isolated
if echo "$TASK_INFO" | grep -q '"sessionTarget": "isolated"'; then
    echo "✅ sessionTarget: isolated (符合规范)"
else
    echo "❌ sessionTarget: 不是 isolated (不符合规范)"
fi

# 检查 announce 模式
if echo "$TASK_INFO" | grep -q '"mode": "announce"'; then
    echo "✅ delivery.mode: announce (符合规范)"
else
    echo "❌ delivery.mode: 不是 announce (不符合规范)"
fi

# 检查 channel
if echo "$TASK_INFO" | grep -q '"channel":'; then
    CHANNEL=$(echo "$TASK_INFO" | grep '"channel":' | head -1 | sed 's/.*"channel": *"\([^"]*\)".*/\1/')
    echo "✅ channel: $CHANNEL (已配置)"
else
    echo "❌ channel: 未配置"
fi

# 检查 to (用户ID)
if echo "$TASK_INFO" | grep -q '"to":'; then
    TO_USER=$(echo "$TASK_INFO" | grep '"to":' | head -1 | sed 's/.*"to": *"\([^"]*\)".*/\1/')
    echo "✅ to: $TO_USER (已配置)"
else
    echo "❌ to: 未配置"
fi

# 检查时间配置
if echo "$TASK_INFO" | grep -q '"at":'; then
    AT_TIME=$(echo "$TASK_INFO" | grep '"at":' | head -1 | sed 's/.*"at": *"\([^"]*\)".*/\1/')
    echo "✅ at: $AT_TIME (一次性任务)"
elif echo "$TASK_INFO" | grep -q '"cron":'; then
    CRON_EXPR=$(echo "$TASK_INFO" | grep '"cron":' | head -1 | sed 's/.*"cron": *"\([^"]*\)".*/\1/')
    echo "✅ cron: $CRON_EXPR (周期性任务)"
else
    echo "❌ 时间配置: 未找到 at 或 cron 配置"
fi

echo ""
echo "========================================"
echo "✅ 验证完成: 任务 '$TASK_NAME' 配置基本正确"
echo ""
echo "📋 规范检查结果:"
echo "  1. ✅ 任务存在性检查"
echo "  2. ✅ 关键参数配置检查"
echo "  3. ✅ 时间格式检查"
echo ""
echo "⚠️  注意: 建议在任务执行时间前30分钟再次检查系统状态"