#!/bin/bash
# Content Matrix Publisher - 热点发现脚本

set -e

TOPIC="${1:-AI}"
OUTPUT_DIR="${2:-/tmp/content-matrix/discovery}"
MAX_RESULTS="${3:-10}"

mkdir -p "$OUTPUT_DIR"

echo "🔍 开始搜索热点: $TOPIC"
echo "📁 输出目录: $OUTPUT_DIR"

# 搜索小红书
echo "📱 搜索小红书..."
agent-reach search xiaohongshu \
  --query "$TOPIC" \
  --limit $MAX_RESULTS \
  --output "$OUTPUT_DIR/xiaohongshu.json" 2>/dev/null || echo "⚠️ 小红书搜索失败"

# 搜索微博
echo "🐦 搜索微博..."
agent-reach search weibo \
  --query "$TOPIC" \
  --limit 5 \
  --output "$OUTPUT_DIR/weibo.json" 2>/dev/null || echo "⚠️ 微博搜索失败"

# 搜索知乎
echo "📚 搜索知乎..."
agent-reach search zhihu \
  --query "$TOPIC" \
  --limit 5 \
  --output "$OUTPUT_DIR/zhihu.json" 2>/dev/null || echo "⚠️ 知乎搜索失败"

# 汇总结果
echo ""
echo "✅ 搜索完成！结果保存在: $OUTPUT_DIR"
echo "📊 汇总:"
echo "  - 小红书: $(cat "$OUTPUT_DIR/xiaohongshu.json" 2>/dev/null | jq 'length' 2>/dev/null || echo '0') 条"
echo "  - 微博: $(cat "$OUTPUT_DIR/weibo.json" 2>/dev/null | jq 'length' 2>/dev/null || echo '0') 条"
echo "  - 知乎: $(cat "$OUTPUT_DIR/zhihu.json" 2>/dev/null | jq 'length' 2>/dev/null || echo '0') 条"