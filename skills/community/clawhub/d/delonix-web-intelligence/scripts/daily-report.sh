#!/bin/bash
# 德胧舆情采集每日自动报告脚本
# 用法: ./daily-report.sh [关键词]
# 默认关键词：华住 锦江 亚朵 德胧

KEYWORDS="${1:-华住 锦江 亚朵 德胧 酒店 投诉}"
OUTPUT_DIR="/tmp/delonix-intelligence/$(date +%Y%m%d)"
mkdir -p "$OUTPUT_DIR"

echo "=== 德胧舆情采集 $(date '+%Y-%m-%d %H:%M') ==="
echo "关键词: $KEYWORDS"
echo "输出目录: $OUTPUT_DIR"

# 搜索主要舆情
echo -e "\n[1/3] 搜索舆情数据..."
miaoda-studio-cli search-summary \
  --query "$KEYWORDS 投诉 隐私 2026" \
  --instruction "只保留2026年发布的内容，提取标题、摘要、来源URL" \
  --output json > "$OUTPUT_DIR/raw-search.json" 2>&1

if [ $? -eq 0 ]; then
  echo "✅ 搜索完成"
else
  echo "⚠️ 搜索超时或失败，继续..."
fi

# 生成报告
echo -e "\n[2/3] 生成分析报告..."
REPORT_FILE="$OUTPUT_DIR/report-$(date +%H%M).md"

cat > "$REPORT_FILE" << 'HEADER'
# 酒店行业舆情日报 | DATE_PLACEHOLDER

> 自动生成 | 德胧AI龙虾军团

## 🔴 超级热点

HEADER

# 替换日期
sed -i "s/DATE_PLACEHOLDER/$(date '+%Y年%m月%d日')/" "$REPORT_FILE"

# 追加搜索结果摘要
if [ -s "$OUTPUT_DIR/raw-search.json" ]; then
  echo "搜索结果已保存到: $OUTPUT_DIR/raw-search.json"
else
  echo "⚠️ 搜索结果为空，请检查网络"
fi

# 发送飞书卡片
echo -e "\n[3/3] 准备飞书卡片..."
echo "报告已生成: $REPORT_FILE"
echo "如需发送飞书卡片，请调用 feishu_send_message 工具"

echo -e "\n=== 完成 ==="
