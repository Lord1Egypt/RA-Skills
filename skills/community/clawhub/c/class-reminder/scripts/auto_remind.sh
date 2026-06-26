#!/bin/bash
# auto_remind.sh - 自动课程提醒脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEDULE_FILE="$SCRIPT_DIR/../data/schedule.xlsx"
SEMESTER_START="2026-03-09"

# 运行课程查询
RESULT=$(python3 "$SCRIPT_DIR/class_reminder.py" tomorrow "$SCHEDULE_FILE" --semester-start "$SEMESTER_START" 2>/dev/null)

# 提取格式化文本
FORMATTED=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('formatted', '查询失败'))")

# 输出提醒文本
echo "$FORMATTED"
