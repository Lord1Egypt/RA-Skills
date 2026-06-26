#!/bin/bash
set -e
# ASR 热词挖掘入口脚本
# 用法:
#   bash run.sh                          # 默认提取前一天
#   bash run.sh --date 2026-04-26        # 指定日期
#   bash run.sh --start 2026-04-20 --end 2026-04-26  # 日期范围
#   bash run.sh --export-only -f prompt  # 仅导出热词表

cd "$(dirname "$0")"
python3 run.py "$@"
