---
name: doc-genius
version: 1.2.0
description: 智能文档处理助手，支持PDF/Word/Markdown智能摘要、格式转换、批量处理。使用场景：(1) 文档智能摘要 (2) PDF/Word转Markdown (3) 批量文档处理 (4) 文档格式转换。Triggers: "文档摘要", "PDF转Markdown", "Word转换", "文档处理", "批量文档", "智能摘要", "format conversion"。
---

# Doc Genius - 智能文档处理助手

## 快速开始

### 智能摘要

```bash
# PDF摘要
python3 scripts/doc_processor.py summarize /path/to/document.pdf

# Word摘要
python3 scripts/doc_processor.py summarize /path/to/document.docx

# Markdown摘要
python3 scripts/doc_processor.py summarize /path/to/document.md --format json
```

### 格式转换

```bash
# PDF → Markdown
python3 scripts/doc_processor.py convert /path/to/document.pdf --output markdown

# Word → Markdown
python3 scripts/doc_processor.py convert /path/to/document.docx --output markdown

# Markdown → HTML
python3 scripts/doc_processor.py convert /path/to/document.md --output html
```

### 批量处理

```bash
# 批量转换文件夹
python3 scripts/doc_processor.py batch /path/to/folder --output markdown

# 批量摘要
python3 scripts/doc_processor.py batch /path/to/folder --action summarize
```

---

## 输出格式

### JSON格式（默认）

```json
{
  "file": "document.pdf",
  "type": "pdf",
  "summary": "这是文档的智能摘要...",
  "keywords": ["关键词1", "关键词2"],
  "word_count": 5000,
  "pages": 12
}
```

### Markdown格式

```bash
python3 scripts/doc_processor.py summarize document.pdf --format markdown
```

---

## 核心功能

### 1. 智能摘要

**支持格式：**
- ✅ PDF（PyPDF2）
- ✅ Word（.docx）
- ✅ Markdown
- ✅ 纯文本

**摘要算法：**
- 本地摘要（TextRank，速度快）
- AI摘要（OpenAI API，质量高）

**示例：**

```python
# 本地摘要
python3 scripts/doc_processor.py summarize document.pdf --method local

# AI摘要（需配置API Key）
export OPENAI_API_KEY="sk-xxx"
python3 scripts/doc_processor.py summarize document.pdf --method ai
```

---

### 2. 格式转换

**转换矩阵：**

| 输入格式 | 输出格式 | 状态 |
|---------|---------|------|
| PDF | Markdown | ✅ |
| PDF | HTML | ⚠️ 实验性 |
| Word | Markdown | ✅ |
| Word | HTML | ✅ |
| Markdown | HTML | ✅ |
| Markdown | Word | 🔜 计划中 |

**示例：**

```bash
# PDF → Markdown（推荐）
python3 scripts/doc_processor.py convert report.pdf --output markdown

# Word → HTML
python3 scripts/doc_processor.py convert report.docx --output html
```

---

### 3. 批量处理

**功能：**
- 文件夹扫描
- 并发处理
- 进度报告
- 错误日志

**示例：**

```bash
# 批量转换（默认并发数=5）
python3 scripts/doc_processor.py batch /path/to/docs --output markdown

# 指定并发数
python3 scripts/doc_processor.py batch /path/to/docs --output markdown --workers 10

# 生成报告
python3 scripts/doc_processor.py batch /path/to/docs --action summarize --report report.json
```

---

### 4. 结构化提取（实验性）

**提取内容：**
- 标题层级
- 目录
- 关键信息（日期、金额、人名）

**示例：**

```bash
python3 scripts/doc_processor.py extract document.pdf --fields title,toc,dates
```

---

## 高级用法

### 使用AI摘要

```bash
# 配置API Key
export OPENAI_API_KEY="sk-xxx"

# AI摘要（更智能）
python3 scripts/doc_processor.py summarize document.pdf --method ai --model gpt-4
```

### 自定义输出

```bash
# 指定输出文件
python3 scripts/doc_processor.py convert document.pdf --output markdown --out-file output.md

# 指定输出目录
python3 scripts/doc_processor.py batch /path/to/docs --output-dir /path/to/output
```

### 过滤处理

```bash
# 只处理PDF文件
python3 scripts/doc_processor.py batch /path/to/docs --filter "*.pdf"

# 排除文件
python3 scripts/doc_processor.py batch /path/to/docs --exclude "temp_*"
```

---

## 技术细节

### 依赖库

```
PyPDF2==3.0.1          # PDF处理
python-docx==1.1.0     # Word处理
markdown==3.5.1        # Markdown处理
beautifulsoup4==4.12.2 # HTML解析
aiofiles==23.2.1       # 异步文件处理
```

### 安装依赖

```bash
pip install PyPDF2 python-docx markdown beautifulsoup4 aiofiles
```

---

## 性能优化

### 并发处理

- 默认并发数：5
- 最大并发数：20
- 推荐：根据CPU核心数调整

### 内存优化

- 流式处理大文件（>10MB）
- 分块处理（避免内存溢出）

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `FileNotFoundError` | 文件不存在 | 检查路径 |
| `PermissionError` | 权限不足 | 检查文件权限 |
| `UnsupportedFormat` | 格式不支持 | 查看支持列表 |

### 日志级别

```bash
# 调试模式
python3 scripts/doc_processor.py summarize document.pdf --log-level debug
```

---

## 最佳实践

### 1. 大文件处理

```bash
# 分块处理
python3 scripts/doc_processor.py summarize large.pdf --chunk-size 1000
```

### 2. 批量处理优化

```bash
# 使用适当的并发数
python3 scripts/doc_processor.py batch /path/to/docs --workers $(nproc)
```

### 3. 输出格式选择

| 场景 | 推荐格式 |
|------|---------|
| 内容分析 | JSON |
| 人类阅读 | Markdown |
| 网页展示 | HTML |

---

## 使用场景

### 1. 研究人员
- 快速阅读大量论文
- 提取关键信息
- 生成文献摘要

### 2. 内容创作者
- 转换格式（PDF→Markdown）
- 提取素材
- 智能摘要

### 3. 企业用户
- 批量处理合同
- 文档格式统一
- 知识库构建

---

## 与其他技能配合

### scrapling-fetch
```bash
# 抓取网页 → 转换PDF → 智能摘要
python3 scrapling-fetch/scripts/fetch.py "https://example.com/article" --text > temp.md
python3 doc-genius/scripts/doc_processor.py summarize temp.md
```

---

## 更新日志

### v1.0.0 (2026-03-07)
- ✅ 初始发布
- ✅ 支持PDF/Word/Markdown摘要
- ✅ 支持格式转换
- ✅ 支持批量处理

---

## 反馈与支持

- GitHub Issues: [待补充]
- ClawHub: https://clawhub.com/skill/doc-genius
- Email: [待补充]

---

**Doc Genius - 让文档处理更智能** 📄✨
