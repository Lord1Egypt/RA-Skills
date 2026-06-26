#!/bin/bash
# 完整的文章归档实现示例
# 展示所有关键步骤的正确实现方式

set -e

URL="$1"

if [ -z "$URL" ]; then
  echo "用法: $0 <article_url>"
  exit 1
fi

echo "📥 开始归档文章..."

# 1. 读取配置文件
source ~/.openclaw/workspace/skills/article-archiver/config/feishu-locations.sh
echo "✓ 配置加载完成"
echo "  归档位置: $DEFAULT_PARENT_NODE"

# 2. 使用 agent-browser 打开页面
echo "🌐 打开页面..."
agent-browser open "$URL"
sleep 3

# 3. 滚动加载所有图片
echo "📜 滚动加载图片..."
agent-browser scroll down 5000
sleep 2
agent-browser scroll down 5000
sleep 2

# 4. 提取文章标题
echo "📝 提取标题..."
TITLE=$(agent-browser eval 'document.title.split("|")[0].trim()' | tr -d '"')
echo "  标题: $TITLE"

# 5. 去重检查
echo "🔍 检查是否已存在..."
# TODO: 使用 feishu_wiki nodes 搜索同名文档

# 6. 提取图片 URL
echo "🖼️  提取图片..."
agent-browser eval 'JSON.stringify(
  Array.from(document.querySelectorAll("img"))
    .filter(img => !img.src.startsWith("data:") && 
                   !img.src.includes("avatar") && 
                   img.naturalWidth > 300)
    .map(img => img.src)
)' > /tmp/image-urls.json

IMAGE_COUNT=$(cat /tmp/image-urls.json | jq '. | length')
echo "  找到 $IMAGE_COUNT 张图片"

# 7. 提取文章内容（使用 web_fetch 或其他方式）
echo "📄 提取内容..."
# TODO: 使用 web_fetch 或 agent-browser 提取内容

# 8. 创建飞书文档
echo "📁 创建飞书文档..."
# TODO: 使用 feishu_wiki create 创建文档
# DOC_TOKEN=$(...)
# NODE_TOKEN=$(...)

# 9. 写入元数据头部
echo "✍️  写入元数据..."
feishu_doc append --doc-token "$DOC_TOKEN" --content "📄 原文：$URL
📅 归档时间：$(date +%Y-%m-%d)
✍️ 作者：$AUTHOR

---
"

# 10. 分批写入正文
echo "✍️  写入正文..."
# TODO: 使用 read 工具读取内容，分批 append

# 11. 上传图片
echo "🖼️  上传图片..."
cat /tmp/image-urls.json | jq -r '.[]' | while read img_url; do
  echo "  上传: $img_url"
  curl -s -o /tmp/img.jpg "$img_url"
  # TODO: 使用 feishu_doc upload_image --file_path /tmp/img.jpg
  sleep 0.3
done

# 12. 关闭浏览器
agent-browser close

# 13. 发送成功通知
echo "✅ 归档完成！"
echo "🔗 飞书链接: https://qingzhao.feishu.cn/wiki/$NODE_TOKEN"

# TODO: 使用 message 工具发送通知
