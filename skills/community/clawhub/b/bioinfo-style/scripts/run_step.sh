#!/bin/bash
# =====================================================================
# 生信分析步骤执行器
# 用法: bash run_step.sh <step_name> <script.sh>
# 示例: bash run_step.sh qc 01_qc.sh
# =====================================================================

STEP_NAME=${1:-"step"}
SCRIPT=${2:-""}
LOG_DIR="logs"

mkdir -p $LOG_DIR
LOG_FILE="${LOG_DIR}/${STEP_NAME}.log"

if [ -z "$SCRIPT" ]; then
    echo "用法: bash run_step.sh <步骤名> <脚本文件>"
    echo "示例: bash run_step.sh qc 01_qc.sh"
    exit 1
fi

if [ ! -f "$SCRIPT" ]; then
    echo "错误: 脚本 $SCRIPT 不存在"
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始执行: $SCRIPT" | tee $LOG_FILE
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 日志: $LOG_FILE" | tee -a $LOG_FILE

set -e
bash $SCRIPT 2>&1 | tee -a $LOG_FILE

EXIT_CODE=${PIPESTATUS[0]}
if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 完成: $SCRIPT" | tee -a $LOG_FILE
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 失败 (exit $EXIT_CODE): $SCRIPT" | tee -a $LOG_FILE
    exit $EXIT_CODE
fi
