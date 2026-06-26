#!/bin/bash

# ChatGPT/Claude 文档提取一键执行脚本
# 
# 用法:
#   ./extract.sh <URL> [OUTPUT_DIR]
#
# 示例:
#   ./extract.sh "https://chatgpt.com/share/xxx"
#   ./extract.sh "https://claude.ai/share/xxx"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 默认值
TARGET_URL="${1:-${TARGET_URL}}"
OUTPUT_DIR="${2:-${OUTPUT_DIR}}"
CHROME_DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"

if [ -z "$TARGET_URL" ]; then
  echo "用法: $0 <URL> [OUTPUT_DIR]"
  echo ""
  echo "参数:"
  echo "  <URL>       ChatGPT 或 Claude 分享链接 (必需)"
  echo "  [OUTPUT_DIR] 输出目录 (可选，默认: ~/LookBack/{日期}/{ChatGPT|Claude})"
  echo ""
  echo "环境变量:"
  echo "  CHROME_DEBUG_PORT  Chrome 调试端口 (默认: 9222)"
  exit 1
fi

# 确定输出目录
IS_CLAUDE=false
if [[ "$TARGET_URL" == *"claude.ai"* ]]; then
  IS_CLAUDE=true
fi

if [ -z "$OUTPUT_DIR" ]; then
  DATE=$(date +%Y-%m-%d)
  SUB_DIR="ChatGPT"
  if [ "$IS_CLAUDE" = true ]; then
    SUB_DIR="Claude"
  fi
  OUTPUT_DIR="$HOME/LookBack/$DATE/$SUB_DIR"
fi

echo "🔍 提取 ChatGPT/Claude 文档"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📎 URL: $TARGET_URL"
echo "📁 输出: $OUTPUT_DIR"
echo "🔌 端口: $CHROME_DEBUG_PORT"
echo ""

# 步骤 1: 抓取 HTML
echo "📥 步骤 1/2: 抓取页面..."
cd "$SCRIPT_DIR"
CHROME_DEBUG_PORT=$CHROME_DEBUG_PORT TARGET_URL="$TARGET_URL" OUTPUT_DIR="$OUTPUT_DIR" node capture-cdp.js

if [ $? -ne 0 ]; then
  echo "❌ 抓取失败"
  exit 1
fi

# 步骤 2: 转换 Markdown
echo ""
echo "📝 步骤 2/2: 转换 Markdown..."
META_PATH="$OUTPUT_DIR/.metadata.json"

if [ -f "$META_PATH" ]; then
  node convert-markdown.js --metadata "$META_PATH"
  
  if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ 完成！"
    echo "📁 文件保存在: $OUTPUT_DIR"
  else
    echo "❌ 转换失败"
    exit 1
  fi
else
  echo "⚠️  未找到元数据文件，跳过 Markdown 转换"
  echo "   HTML 文件已保存到: $OUTPUT_DIR"
fi