#!/bin/bash
# Bioinfo Daily Cron Wrapper - 运行日报并发送到飞书群

# 运行日报生成脚本
OUTPUT=$(python3 ~/.openclaw/workspace/skills/bioinfo-daily/scripts/pubmed_search.py 2>&1)

# 提取日报文件路径
REPORT_FILE=$(echo "$OUTPUT" | grep "日报已保存:" | awk '{print $NF}')

if [ -f "$REPORT_FILE" ]; then
    # 读取日报内容
    REPORT_CONTENT=$(cat "$REPORT_FILE")
    echo "$REPORT_CONTENT"
else
    echo "日报生成失败"
    echo "$OUTPUT"
    exit 1
fi
