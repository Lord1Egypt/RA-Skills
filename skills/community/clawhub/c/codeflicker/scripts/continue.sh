#!/bin/bash
# 继续与 CodeFlicker 对话
# 用法: continue.sh "继续的任务"

TASK="$1"

if [ -z "$TASK" ]; then
    echo "用法: continue.sh \"继续任务描述\""
    exit 1
fi

if ! command -v flickcli &> /dev/null; then
    echo "❌ flickcli 未安装"
    exit 1
fi

echo "🤖 继续对话: $TASK"
echo ""

flickcli -q -c "$TASK"