# 添加知识到知识库指南

本文档指导 AI Agent 如何将上传的文件添加到本地知识库。

## 工作流程

### 1. 检查临时上传文件

检查 `.openclaw/workspace/temp_file/` 文件夹，查找以下格式的上传文件：
- `.docx` (Word 文档)
- `.pdf` (PDF 文档)
- `.xlsx` (Excel 电子表格)
- `.pptx` (PowerPoint 演示文稿)

### 2. 文件格式转换

使用适当的工具将每个文件转换为 Markdown 格式：

| 文件格式 | 推荐工具 | 备选方案 |
|---------|---------|---------|
| docx | `officecli docx` skill | python-docx |
| pdf | pdfplumber, PyPDF2 | - |
| xlsx | `officecli xlsx` skill | openpyxl |
| pptx | `officecli pptx` skill | python-pptx |

**格式转换优先级**：
1. 优先使用 `officecli` 相关 skill（已注册的命令）
2. 无法使用 skill 时，使用对应的 Python 库

### 3. 保存转换后的文件

将转换得到的 Markdown 文件保存到：
```
.openclaw/workspace/memory/knowledge_base/
```

### 4. 文本清洗（重要）

**必须过滤乱码/乱字符**：
- 检测并移除 Mojibake（编码错误的字符）
- 检查常见的编码问题标志：
  - 大量 `�` 字符
  - 异常的 `\x` 转义序列
  - 非预期的 Unicode 替代字符
- **禁止写入**包含乱码的内容到 Markdown 文件

### 5. 生成文件元信息

为每个转换后的文件生成：
- **文件名**：使用语义化的中文名称，`.md` 后缀
- **摘要**：简洁描述文件的主要内容（中文，1-3 句话）

### 6. 更新知识库索引

在 `.openclaw/workspace/memory/knowledge_base_index.json` 中追加条目：

```json
{
  "name": "markdown文件名称.md",
  "description": "该文件主要讲述的内容（摘要）"
}
```

**注意事项**：
- 如果 `knowledge_base_index.json` 不存在，创建为空数组 `[]`
- 追加而非覆盖现有内容
- 保持 JSON 格式正确

### 7. 删除原始文件

转换并保存成功后，从 `.openclaw/workspace/temp_file/` 中删除原始文件：

```bash
# 删除原始文件（以 docx 为例）
rm .openclaw/workspace/temp_file/文件.docx
```

**注意**：仅在转换成功且已更新索引后才删除原始文件。

## 示例

假设 `temp_file/` 中有一个 `文件.docx`：

```bash
# 1. 转换 docx 为 markdown
# 使用 officecli docx skill 或 python-docx 读取并转换

# 2. 保存到知识库
# .openclaw/workspace/memory/knowledge_base/文件.md

# 3. 更新索引
# .openclaw/workspace/memory/knowledge_base_index.json
```

生成的索引条目：
```json
{
  "name": "文件.md",
  "description": "文件记录的主要内容摘要。"
}
```

## 质量检查清单

- [ ] 所有上传文件均已转换并保存
- [ ] Markdown 内容无乱码/乱字符
- [ ] 文件名语义化且使用中文
- [ ] 摘要简洁、准确描述内容
- [ ] 索引文件格式正确（有效 JSON）
- [ ] 新条目已正确追加到索引数组
- [ ] 原始文件已从 temp_file 中删除
