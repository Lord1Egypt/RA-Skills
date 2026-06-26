#!/bin/bash
# Codex Runner - Async Start (使用 sessions_spawn)
# 不阻塞主会话，在独立子会话中运行

TASK_NAME=${2:-codex-task}
TARGET_DIR=${3:-.}
LOG_DIR=~/.codex-logs
LOG_FILE=$LOG_DIR/codex-$TASK_NAME.log

mkdir -p $LOG_DIR

# 清理旧日志
> $LOG_FILE

echo "🚀 启动 Codex 异步任务: $TASK_NAME"
echo "📁 目标目录: $TARGET_DIR"
echo "📝 任务描述: $1"
echo "📄 日志: $LOG_FILE"

# 使用 sessions_spawn 在独立子会话运行 Codex
# 注意：这里输出 JSON 格式让 OpenClaw 执行 sessions_spawn
cat << JSON
{
  "runtime": "subagent",
  "task": "在 $TARGET_DIR 目录执行以下任务：$1\n\n要求：\n1. 先了解目录结构和现有代码\n2. 按要求实现功能\n3. 如果需要测试，先写测试再写代码\n4. 完成后汇报结果",
  "label": "codex-$TASK_NAME",
  "mode": "run"
}
JSON

echo ""
echo "✅ 任务已在独立子会话中启动，你可以继续发送消息"
echo "查看日志: codex-runner log $TASK_NAME"
