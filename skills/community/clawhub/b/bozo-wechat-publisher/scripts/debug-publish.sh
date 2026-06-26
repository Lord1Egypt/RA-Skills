#!/usr/bin/env bash
# 调试版本：打印实际发送到微信的 HTML 内容

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_DIR="/Volumes/AI/AIGC/aigc/Skills/bozo-wechat-publisher"
THEME_FILE="$SKILL_DIR/themes/card-tech-dark.html"
MARKDOWN_FILE="$1"

if [ -z "$MARKDOWN_FILE" ]; then
    MARKDOWN_FILE="$SKILL_DIR/example.md"
fi

echo -e "${BLUE}=== 调试：检查发送的 HTML 内容 ===${NC}"
echo "Markdown 文件: $MARKDOWN_FILE"
echo "主题文件: $THEME_FILE"
echo ""

# 1. 使用 wenyan-cli 渲染
echo -e "${YELLOW}[1] 使用 wenyan-cli 渲染 Markdown...${NC}"
TMP_HTML=$(mktemp)
wenyan render -f "$MARKDOWN_FILE" -t default -h dracula --no-mac-style > "$TMP_HTML"
echo "✓ 渲染完成"
echo ""

# 2. 提取 body 内容
echo -e "${YELLOW}[2] 提取 body 内容...${NC}"
BODY_CONTENT=$(sed -n '/<body>/,/<\/body>/p' "$TMP_HTML" | sed '1d;$d')
echo "✓ Body 内容长度: $(echo "$BODY_CONTENT" | wc -c) 字节"
echo ""

# 3. 提取主题 CSS
echo -e "${YELLOW}[3] 提取主题 CSS...${NC}"
THEME_CSS=$(sed -n '/<style>/,/<\/style>/p' "$THEME_FILE" | sed '1d;$d')
echo "✓ CSS 长度: $(echo "$THEME_CSS" | wc -c) 字节"
echo ""

# 4. 组合最终内容
echo -e "${YELLOW}[4] 组合最终内容...${NC}"
FINAL_CONTENT="<style>${THEME_CSS}</style>${BODY_CONTENT}"
echo "✓ 最终内容长度: $(echo "$FINAL_CONTENT" | wc -c) 字节"
echo ""

# 5. 保存到文件供检查
OUTPUT_FILE="$SKILL_DIR/debug-output.html"
echo "$FINAL_CONTENT" > "$OUTPUT_FILE"
echo -e "${GREEN}✓ 已保存到: $OUTPUT_FILE${NC}"
echo ""

# 6. 显示前 1000 字符
echo -e "${YELLOW}[5] 显示前 1000 字符...${NC}"
echo "========================================"
echo "$FINAL_CONTENT" | head -c 1000
echo "..."
echo "========================================"
echo ""

# 7. 检查是否有问题
echo -e "${YELLOW}[6] 检查潜在问题...${NC}"

# 检查是否有可见内容
if echo "$BODY_CONTENT" | grep -q "<p>\|<h1>\|<h2>\|<div"; then
    echo -e "${GREEN}✓ Body 包含可见内容${NC}"
else
    echo -e "${YELLOW}⚠ Body 可能缺少可见内容${NC}"
fi

# 检查 CSS 是否有问题
if echo "$THEME_CSS" | grep -q "color:#0a0e27\|background:#0a0e27"; then
    echo -e "${YELLOW}⚠ CSS 可能导致深色背景，文字可能不可见${NC}"
fi

# 清理
rm -f "$TMP_HTML"

echo ""
echo -e "${BLUE}=== 调试完成 ===${NC}"
echo "请在浏览器中打开 $OUTPUT_FILE 查看实际效果"
