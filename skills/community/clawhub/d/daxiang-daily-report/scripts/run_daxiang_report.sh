#!/bin/bash
# 大象沟通日报定时任务执行脚本
# 使用方法: 添加到crontab中，每天早上6点执行

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/scripts/daxiang_daily_report.py"

# 执行日报生成
python3 "$PYTHON_SCRIPT"

# 输出完成日志
echo "大象日报生成完成: $(date)"
