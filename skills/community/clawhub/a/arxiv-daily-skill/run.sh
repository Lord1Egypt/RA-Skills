#!/bin/bash
# arXiv 每日论文精选 - 完整执行脚本
# 1. 获取论文列表
# 2. 输出紧凑目录
# 3. 对 Top 3 论文调用 ljg-paper 进行深度分析

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="/tmp/arxiv_daily_$(date +%Y%m%d).md"

echo "🔍 开始执行 arXiv 每日论文推送..."
echo ""

# 步骤 1: 获取论文列表
echo "步骤 1: 获取论文列表..."
python3 "$SCRIPT_DIR/fetch_arxiv.py" > "$OUTPUT_FILE" 2>&1

# 显示目录部分
echo ""
echo "✅ 论文获取完成！"
echo ""
echo "📋 目录预览:"
head -20 "$OUTPUT_FILE"

echo ""
echo "📄 完整报告已保存到：$OUTPUT_FILE"
echo ""
echo "💡 如需深度分析某篇论文，请说：'详解第 X 篇' 或 '分析 [论文标题]'"
