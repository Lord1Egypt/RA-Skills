#!/bin/bash
# Codex Runner - Start command
# 方案：使用 --dangerously-bypass-approvals-and-sandbox 完全跳过沙箱

TASK_NAME=${2:-codex-task}
TARGET_DIR=${3:-.}
LOG_DIR=~/.codex-logs
LOG_FILE=$LOG_DIR/codex-$TASK_NAME.log

mkdir -p $LOG_DIR

echo "启动 Codex 后台任务: $TASK_NAME"
echo "目标目录: $TARGET_DIR"
echo "任务描述: $1"

# 使用 --dangerously-bypass-approvals-and-sandbox 完全跳过沙箱
nohup bash -c "
  cd '$TARGET_DIR'
  
  export https_proxy=http://127.0.0.1:8118
  export http_proxy=http://127.0.0.1:8118
  
  codex \\
    --dangerously-bypass-approvals-and-sandbox \\
    exec '$1'
" > $LOG_FILE 2>&1 &

echo "任务已启动"
echo "日志位置: $LOG_FILE"
echo ""
echo "使用以下命令查看进度："
echo "  codex-runner log $TASK_NAME  # 查看日志"
echo "  codex-runner status          # 检查进程"
