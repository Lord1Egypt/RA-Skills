---
name: content-batch-processor
description: 批量内容处理工具，支持文本格式化、摘要生成、关键词提取、多语言翻译等批量操作。
metadata:
  openclaw:
    requires:
      bins:
        - read
        - write
        - pdf
        - image
---

# 批量内容处理工具 v1.0.0

高效处理大量文本内容，支持多种批处理操作。

## 功能特性

### 1. 文本格式化
- Markdown 格式转换
- HTML 清理
- 统一换行符
- 移除多余空格

### 2. 内容摘要
- 单文档摘要
- 多文档合并摘要
- 可定制摘要长度

### 3. 关键词提取
- 自动提取关键词
- 词频分析
- 主题识别

### 4. 批量转换
- 文件格式转换（TXT ↔ MD ↔ HTML）
- 编码转换
- 批量重命名

### 5. 内容分析
- 字数统计
- 可读性评分
- 语言检测

## 快速使用示例

```javascript
// 批量格式化多个文件
const files = ['doc1.md', 'doc2.md', 'doc3.md']
files.forEach(f => {
  const content = read({path: f})
  const formatted = formatMarkdown(content)
  write({path: f, content: formatted})
})

// 批量生成摘要
const documents = ['report1.pdf', 'report2.pdf', 'report3.pdf']
const summaries = documents.map(doc => 
  pdf({pdf: doc, prompt: "生成 200 字摘要"})
)

// 批量提取关键词
const articles = readDirectory('./articles')
articles.forEach(article => {
  const keywords = extractKeywords(article.content, 10)
  console.log(`${article.name}: ${keywords.join(', ')}`)
})

// 批量翻译
const texts = ['文本 1', '文本 2', '文本 3']
const translated = texts.map(text => 
  translate(text, {from: 'zh', to: 'en'})
)

// 批量重命名文件
const files = getFiles('./downloads')
files.forEach((file, index) => {
  const newName = `document_${String(index+1).padStart(3, '0')}.md`
  rename(file.path, `./organized/${newName}`)
})
```

## 批处理模式

### 模式 1：顺序处理
```javascript
// 适合小批量任务
const results = []
for (const item of items) {
  results.push(process(item))
}
```

### 模式 2：并行处理
```javascript
// 适合大批量任务
const results = await Promise.all(
  items.map(item => process(item))
)
```

### 模式 3：流式处理
```javascript
// 适合超大文件
const stream = createReadStream('large-file.txt')
stream.on('data', chunk => {
  process(chunk)
})
```

## 使用场景

1. **内容创作** - 批量格式化文章、生成摘要
2. **研究分析** - 批量处理论文、提取关键词
3. **数据清洗** - 批量清理文本数据
4. **文档管理** - 批量重命名、分类整理
5. **多语言处理** - 批量翻译文档

## 性能优化建议

- 小批量（<10 个文件）：顺序处理
- 中批量（10-100 个文件）：并行处理（5-10 并发）
- 大批量（>100 个文件）：分批处理 + 进度保存

## 相关文件

- `CHANGELOG.md` - 版本历史
- `examples/` - 使用示例
- `templates/` - 处理模板

## 许可证

MIT-0 - 自由使用、修改和分发
