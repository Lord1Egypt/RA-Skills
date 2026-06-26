#!/bin/bash
# 归档长文章到飞书文档（支持多图片、完整格式）
# 用法: ./archive-long-article.sh <article_url> <doc_token>

set -e

ARTICLE_URL="$1"
DOC_TOKEN="$2"

if [ -z "$ARTICLE_URL" ] || [ -z "$DOC_TOKEN" ]; then
  echo "用法: $0 <article_url> <doc_token>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORK_DIR="/tmp/article-archiver-$$"

mkdir -p "$WORK_DIR"

echo "=== 归档长文章 ==="
echo "URL: $ARTICLE_URL"
echo "文档: $DOC_TOKEN"
echo "工作目录: $WORK_DIR"
echo ""

# 1. 读取 Cookie
COOKIE_FILE="$SKILL_DIR/config/twitter-cookies.txt"
if [ ! -f "$COOKIE_FILE" ]; then
  echo "❌ Cookie 文件不存在: $COOKIE_FILE"
  exit 1
fi

COOKIE=$(cat "$COOKIE_FILE")
echo "✅ Cookie 已加载"

# 2. 抓取文章内容（使用 html-to-markdown.js）
echo "📥 抓取文章内容..."
cd "$SKILL_DIR/scripts"
node html-to-markdown.js "$ARTICLE_URL" "$COOKIE" > "$WORK_DIR/article.json"

if [ $? -ne 0 ]; then
  echo "❌ 抓取失败"
  exit 1
fi

echo "✅ 抓取成功"

# 3. 解析文章数据
TITLE=$(jq -r '.title' "$WORK_DIR/article.json")
AUTHOR=$(jq -r '.author' "$WORK_DIR/article.json")
USERNAME=$(jq -r '.username' "$WORK_DIR/article.json")
CONTENT=$(jq -r '.content' "$WORK_DIR/article.json")

echo "标题: $TITLE"
echo "作者: $AUTHOR (@$USERNAME)"
echo ""

# 4. 提取图片 URL
echo "🖼️  提取图片..."
echo "$CONTENT" | grep -oP '!\[.*?\]\(\K[^)]+' > "$WORK_DIR/images.txt" || true
IMAGE_COUNT=$(wc -l < "$WORK_DIR/images.txt")
echo "发现 $IMAGE_COUNT 张图片"

# 5. 分段处理（按图片位置分段）
echo "📝 分段处理内容..."

# 生成段落清单
python3 <<EOF
import json
import re

# 读取内容
with open('$WORK_DIR/article.json', 'r') as f:
    data = json.load(f)
    content = data['content']

# 按图片分段
segments = []
parts = re.split(r'(!\[.*?\]\([^)]+\))', content)

for i, part in enumerate(parts):
    part = part.strip()
    if not part:
        continue
    
    # 检查是否是图片
    if part.startswith('!['):
        # 提取图片 URL
        match = re.search(r'!\[.*?\]\(([^)]+)\)', part)
        if match:
            segments.append({
                'type': 'image',
                'url': match.group(1)
            })
    else:
        # 文本段落
        segments.append({
            'type': 'text',
            'content': part
        })

# 保存清单
with open('$WORK_DIR/manifest.json', 'w') as f:
    json.dump(segments, f, indent=2, ensure_ascii=False)

print(f"生成 {len(segments)} 个段落")
EOF

# 6. 准备头部元数据
ARCHIVE_TIME=$(TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M:%S')
DOMAIN=$(echo "$ARTICLE_URL" | sed -E 's|https?://([^/]+).*|\1|')

HEADER="> **原始链接**：$ARTICLE_URL
> 
> **归档时间**：$ARCHIVE_TIME
> 
> **来源**：$DOMAIN
> 
> **作者**：$AUTHOR (@$USERNAME)

"

# 7. 写入飞书文档
echo "📤 写入飞书文档..."

# 写入标题和头部
echo "## $TITLE

$HEADER" > "$WORK_DIR/header.md"

# 使用 feishu_doc 工具写入（这里需要在 OpenClaw 环境中调用）
echo "⚠️  需要在 OpenClaw 环境中执行以下命令："
echo ""
echo "# 1. 写入头部"
echo "feishu_doc write --doc_token $DOC_TOKEN --content \"\$(cat $WORK_DIR/header.md)\""
echo ""
echo "# 2. 批量写入段落"
echo "jq -c '.[]' $WORK_DIR/manifest.json | while read segment; do"
echo "  TYPE=\$(echo \"\$segment\" | jq -r '.type')"
echo "  if [ \"\$TYPE\" = \"text\" ]; then"
echo "    CONTENT=\$(echo \"\$segment\" | jq -r '.content')"
echo "    feishu_doc append --doc_token $DOC_TOKEN --content \"\$CONTENT\""
echo "  else"
echo "    URL=\$(echo \"\$segment\" | jq -r '.url')"
echo "    feishu_doc upload_image --doc_token $DOC_TOKEN --url \"\$URL\""
echo "  fi"
echo "  sleep 0.3  # 避免 API 限流"
echo "done"
echo ""
echo "工作目录: $WORK_DIR"
echo "清单文件: $WORK_DIR/manifest.json"
