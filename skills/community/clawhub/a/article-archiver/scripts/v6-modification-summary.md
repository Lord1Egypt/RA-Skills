# html-to-markdown-v6.js 修改完成

## 任务完成情况

✅ 已成功修改脚本，实现 contentBlocks 数组记录功能

## 主要改动

### 1. 数据结构变化
- **旧版本**：输出 `{ title, author, content, images[] }`
- **新版本**：输出 `{ title, author, contentBlocks[] }`

### 2. contentBlocks 格式
```json
{
  "contentBlocks": [
    { "type": "text", "content": "..." },
    { "type": "image", "url": "https://..." },
    { "type": "text", "content": "..." }
  ]
}
```

### 3. 核心逻辑改动

**旧版本**：
- 先收集所有图片到数组
- 遍历 DOM 时按索引插入图片

**新版本**：
- 维护 `contentBlocks` 数组和 `currentText` 缓冲区
- 遍历 DOM 时：
  - 遇到文本：累积到 `currentText`
  - 遇到图片：
    1. flush `currentText` 到 contentBlocks（如果非空）
    2. 添加图片块到 contentBlocks
    3. 清空 `currentText`
- 遍历结束后：flush 最后的 `currentText`

### 4. 保留的功能
- ✅ 粗体、斜体、代码块等格式处理
- ✅ 列表、标题等结构化内容
- ✅ 图片 URL 处理（添加 `?format=jpg&name=large`）
- ✅ 原有选择器（`[data-testid="twitterArticleRichTextView"]`）

## 测试结果

### 测试用例
使用模拟 HTML 测试（`test-contentblocks.js`），包含：
- 普通文本段落
- 粗体文本
- 3 张图片
- 列表

### 输出示例（前 5 个 blocks）
```json
[
  {
    "type": "text",
    "content": "这是第一段文本。\n\n        **这是粗体文本。**"
  },
  {
    "type": "image",
    "url": "https://pbs.twimg.com/media/image1.jpg?format=jpg&name=large"
  },
  {
    "type": "text",
    "content": "这是图片后的文本。"
  },
  {
    "type": "image",
    "url": "https://pbs.twimg.com/media/image2.jpg?format=jpg&name=large"
  },
  {
    "type": "text",
    "content": "这是第二张图片后的文本。\n\n        \n\n          - 列表项 1\n\n          - 列表项 2"
  }
]
```

## 文件位置

- **新脚本**：`/root/.openclaw/workspace/skills/article-archiver/scripts/html-to-markdown-v6.js`
- **测试脚本**：`/root/.openclaw/workspace/skills/article-archiver/scripts/test-contentblocks.js`

## 验证方法

```bash
# 运行测试脚本
cd /root/.openclaw/workspace/skills/article-archiver
node scripts/test-contentblocks.js

# 查看前 5 个 blocks
node scripts/test-contentblocks.js | jq '.contentBlocks[:5]'
```

## 注意事项

1. **图片识别**：只识别包含 `pbs.twimg.com/media` 的图片
2. **文本累积**：所有非图片内容都会累积到 currentText，直到遇到图片或遍历结束
3. **格式保留**：Markdown 格式（粗体、列表等）会保留在文本块中
4. **空白处理**：flush 时会 trim 文本，避免空白块
