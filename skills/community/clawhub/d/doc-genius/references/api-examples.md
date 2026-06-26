# API 调用示例

## 基础用法

### 1. 智能摘要

**JSON输出（默认）**

```bash
python3 scripts/doc_processor.py summarize /path/to/document.pdf
```

**输出：**

```json
{
  "file": "document.pdf",
  "type": "pdf",
  "summary": "文档摘要内容...",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "word_count": 5000,
  "pages": 12
}
```

---

**Markdown输出**

```bash
python3 scripts/doc_processor.py summarize /path/to/document.pdf --format markdown
```

**输出：**

```markdown
# 文档摘要

**文件**: document.pdf  
**类型**: pdf  
**字数**: 5000  
**页数**: 12

---

## 摘要

文档摘要内容...

---

## 关键词

关键词1, 关键词2, 关键词3
```

---

**纯文本输出**

```bash
python3 scripts/doc_processor.py summarize /path/to/document.pdf --format text
```

**输出：**

```
文档摘要内容...
```

---

### 2. AI摘要（需要OpenAI API Key）

```bash
# 设置API Key
export OPENAI_API_KEY="sk-xxx"

# AI摘要
python3 scripts/doc_processor.py summarize /path/to/document.pdf --method ai --model gpt-4
```

**输出质量更高，但需要付费API。**

---

## 格式转换

### PDF → Markdown

```bash
python3 scripts/doc_processor.py convert /path/to/document.pdf --output markdown --out-file output.md
```

**输出示例：**

```markdown
# 文档标题

文档内容...

## 章节标题

章节内容...
```

---

### Word → Markdown

```bash
python3 scripts/doc_processor.py convert /path/to/document.docx --output markdown
```

---

### Markdown → HTML

```bash
python3 scripts/doc_processor.py convert /path/to/document.md --output html --out-file output.html
```

**输出示例：**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Converted Document</title>
</head>
<body>
    <h1>文档标题</h1>
    <p>文档内容...</p>
    <h2>章节标题</h2>
    <p>章节内容...</p>
</body>
</html>
```

---

## 批量处理

### 批量摘要

```bash
python3 scripts/doc_processor.py batch /path/to/docs --action summarize --output json --report report.json
```

**生成的报告（report.json）：**

```json
[
  {
    "file": "doc1.pdf",
    "type": "pdf",
    "summary": "摘要1...",
    "keywords": ["关键词1", "关键词2"],
    "word_count": 3000,
    "pages": 10
  },
  {
    "file": "doc2.docx",
    "type": "word",
    "summary": "摘要2...",
    "keywords": ["关键词A", "关键词B"],
    "word_count": 2500,
    "pages": null
  }
]
```

---

### 批量转换

```bash
# 转换到指定目录
python3 scripts/doc_processor.py batch /path/to/docs --action convert --output markdown --output-dir /path/to/output

# 并发处理
python3 scripts/doc_processor.py batch /path/to/docs --action convert --output markdown --workers 10
```

---

## 高级用法

### 1. Python调用

```python
from pathlib import Path
from doc_processor import DocumentProcessor

# 初始化
processor = DocumentProcessor(method="local")

# 摘要
result = processor.summarize(Path("document.pdf"))
print(result["summary"])

# 转换
markdown_text = processor.convert(Path("document.pdf"), "markdown")
print(markdown_text)
```

---

### 2. 使用AI摘要

```python
import os
from pathlib import Path
from doc_processor import DocumentProcessor

# 设置API Key
os.environ["OPENAI_API_KEY"] = "sk-xxx"

# 初始化（使用AI）
processor = DocumentProcessor(method="ai", model="gpt-4")

# AI摘要
result = processor.summarize(Path("document.pdf"), output_format="json")
print(result["summary"])
```

---

### 3. 批量处理（Python）

```python
from pathlib import Path
from doc_processor import DocumentProcessor

processor = DocumentProcessor()

# 批量摘要
results = processor.batch_process(
    Path("/path/to/docs"),
    action="summarize",
    output_format="json",
    workers=5
)

# 输出结果
for result in results:
    if "error" not in result:
        print(f"✅ {result['file']}: {result['word_count']}字")
    else:
        print(f"❌ {result['file']}: {result['error']}")
```

---

## 集成到其他技能

### 与scrapling-fetch配合

```bash
# 1. 抓取网页
python3 scrapling-fetch/scripts/fetch.py "https://example.com/article" --text > temp.md

# 2. 智能摘要
python3 doc-genius/scripts/doc_processor.py summarize temp.md
```

---

### 自动化工作流

```bash
#!/bin/bash

# 批量处理工作流

# 1. 扫描文件夹
DOCS_DIR="/path/to/docs"
OUTPUT_DIR="/path/to/output"

# 2. 批量转换
python3 doc-genius/scripts/doc_processor.py batch $DOCS_DIR \
  --action convert \
  --output markdown \
  --output-dir $OUTPUT_DIR \
  --workers 5

# 3. 生成摘要报告
python3 doc-genius/scripts/doc_processor.py batch $OUTPUT_DIR \
  --action summarize \
  --output json \
  --report summary.json

# 4. 发送通知
echo "✅ 处理完成！共处理 $(cat summary.json | jq length) 个文件"
```

---

## 错误处理

### 常见错误

**1. 文件不存在**

```bash
❌ 错误: FileNotFoundError: document.pdf
```

**解决方案：** 检查文件路径是否正确

---

**2. 格式不支持**

```bash
❌ 错误: ValueError: 不支持的格式: .xlsx
```

**解决方案：** 查看支持的格式列表（PDF/Word/Markdown/Text）

---

**3. API Key未设置**

```bash
⚠️ 未设置OPENAI_API_KEY，自动切换到本地模式
```

**解决方案：**

```bash
export OPENAI_API_KEY="sk-xxx"
```

---

## 性能优化

### 大文件处理

```bash
# 分块处理
python3 scripts/doc_processor.py summarize large.pdf --chunk-size 1000
```

### 并发处理

```bash
# 根据CPU核心数调整
python3 scripts/doc_processor.py batch /path/to/docs --workers $(nproc)
```

---

## 定价参考

| 操作 | 定价 | 说明 |
|------|------|------|
| 智能摘要（本地） | 免费 | 无限次 |
| 智能摘要（AI） | $0.01/次 | 需API Key |
| 格式转换 | $0.005/次 | 本地处理 |
| 批量处理 | $0.003/文件 | 批量优惠 |

---

*最后更新: 2026-03-07*
