#!/bin/bash
# 使用 CodeFlicker 执行任务
# 用法: run.sh "任务描述"

TASK="$1"

if [ -z "$TASK" ]; then
    echo "用法: run.sh \"任务描述\""
    exit 1
fi

# 检查是否安装
if ! command -v flickcli &> /dev/null; then
    echo "❌ flickcli 未安装，请先安装"
    exit 1
fi

echo "🤖 正在执行: $TASK"
echo ""

flickcli -q "$TASK"