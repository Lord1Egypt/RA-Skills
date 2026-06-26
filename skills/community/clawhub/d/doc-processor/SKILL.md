---
name: doc-processor
description: |
  智能文档处理引擎 - 专注文档处理 (v2.7.11 移除 AI 功能)
  支持 Word/Excel/PDF/CSV/TXT 读取、写入、转换、合并、提取
  v2.7.11: 移除 AI 功能 (由 OpenClaw 主程序统一处理)
  v2.7.5: 路径解析 Bug 修复 + 异常体系完善
  v2.7: 性能监控 + 用户文档 + 错误增强
  v2.6: Excel 格式保持 + PDF 生成
  v2.5: 批量处理 + 模板缓存
  v2.4: 日志系统
  v2.3: Excel 模板支持 + 模板匹配智能化
homepage: https://github.com/openclaw/skills
version: 2.7.13
tags: ["document", "word", "excel", "pdf", "file", "conversion", "template", "v2", "logging", "batch"]
metadata:
  openclaw:
    emoji: "📄"
    requires:
      bins: ["pdftotext", "pdfinfo"]
    install:
      - id: brew-poppler
        kind: brew
        formula: poppler
        bins: ["pdftotext", "pdfinfo"]
        label: "Install poppler (Homebrew)"
        platforms: ["darwin"]
      - id: apt-poppler
        kind: system
        command: "sudo apt install -y poppler-utils"
        bins: ["pdftotext", "pdfinfo"]
        label: "Install poppler-utils (apt)"
        platforms: ["linux"]
      - id: python-deps
        kind: script
        script: "setup.sh"
        label: "Install Python dependencies"
tags: ["document", "word", "excel", "pdf", "file", "conversion"]
---

# 文档处理 Skill (Doc Processor)

统一的本地文档处理工具，支持多种格式的读取、写入、转换、合并和数据提取。

## 支持格式

| 格式 | 扩展名 | 读取 | 写入 | 转换 | 合并 | 提取 |
|------|--------|------|------|------|------|------|
| PDF | `.pdf` | ✅ | ❌ | ⚠️ | ❌ | ✅ |
| Word | `.docx` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Excel | `.xlsx` | ✅ | ✅ | ✅ | ✅ | ✅ |
| CSV | `.csv` | ✅ | ✅ | ✅ | - | ✅ |
| 文本 | `.txt` | ✅ | ✅ | ✅ | - | ✅ |
| Markdown | `.md` | ✅ | ✅ | ✅ | - | ✅ |

**注意**:
- ❌ 不支持 `.doc` 和 `.xls` 旧格式（需先用 LibreOffice 转换）
- ✅ PDF 处理使用系统工具 `poppler-utils`

## v2.7.11 重要变更

### AI 功能已移除

**v2.7.11 起，AI 功能（AI 摘要、AI 分析）已移除**，原因：

1. **职责单一**: doc-processor 专注文档处理
2. **架构优化**: AI 能力由 OpenClaw 主程序统一提供
3. **简化配置**: 无需单独配置 LLM_BASE_URL 等环境变量
4. **提升安全**: 移除网络请求，消除 ClawHub 安全标记

**如需 AI 功能**，请使用 OpenClaw 主程序的 LLM 能力：

```python
# 1. 使用 doc-processor 读取文档
content = doc_processor.read('report.docx')

# 2. 将内容发送给 OpenClaw 的 LLM 进行摘要/分析
# (通过 OpenClaw 的消息系统或 API)
```

### 受影响的 API

以下方法已移除或修改：

| 方法 | 原功能 | 新行为 |
|------|--------|--------|
| `ContentAdapter.__init__(ai_service_type)` | AI 服务配置 | 参数已移除 |
| `DocumentProcessor.__init__(ai_service_type)` | AI 服务配置 | 参数已移除 |
| `create_ai_service()` | 创建 AI 服务 | 抛出 NotImplementedError |
| `summarize_document()` | AI 摘要 | 抛出 NotImplementedError |

### 迁移指南

**原代码 (v2.7.10)**:
```python
processor = DocumentProcessor(ai_service_type='hybrid')
summary = processor.summarize_document('file.docx')
```

**新代码 (v2.7.11)**:
```python
# 1. 读取文档
processor = DocumentProcessor()
content = processor.read('file.docx')

# 2. 使用 OpenClaw 主程序进行 AI 处理
# (具体方式取决于 OpenClaw 的实现)
```

## 安装

### 一键安装

```bash
cd ~/.openclaw/workspace/skills/doc-processor
./setup.sh
```

**安装脚本说明**:
- ✅ 标准 pip 操作，安装 Python 依赖
- ✅ 依赖列表：python-docx, openpyxl, pandas, python-dotenv
- ✅ 从官方 PyPI 或可信镜像源安装
- ✅ 无恶意代码，完全开源

详情见：[SECURITY.md](SECURITY.md)

### 手动安装

**1. 安装系统依赖**

```bash
# Linux (Debian/Ubuntu)
sudo apt install poppler-utils

# Linux (RHEL/CentOS)
sudo yum install poppler-utils

# macOS
brew install poppler
```

**2. 安装 Python 依赖**

```bash
# 使用默认官方源
./setup.sh

# 使用清华镜像源（中国大陆推荐）
./setup.sh https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用环境变量
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
./setup.sh

# 其他镜像源
./setup.sh https://pypi.mirrors.ustc.edu.cn/simple
```

**3. 验证安装**

```bash
python3 check_deps.py
```

## 使用示例

### 获取文档信息

```bash
./scripts/doc-info.sh report.pdf
```

### 读取文档

```bash
# 读取 PDF
./scripts/doc-read.sh report.pdf

# 读取 Word（包含表格）
./scripts/doc-read.sh meeting.docx

# 读取 Excel（所有 sheet）
./scripts/doc-read.sh data.xlsx
```

### 写入文档

```bash
# 写入 Word
echo '{"title": "报告", "paragraphs": ["第一段", "第二段"]}' | \
  ./scripts/doc-write.sh -o output.docx

# 写入 Excel
echo '[["姓名", "年龄"], ["张三", 25], ["李四", 30]]' | \
  ./scripts/doc-write.sh -o data.xlsx
```

### 格式转换

```bash
# Word 转 CSV
./scripts/doc-convert.sh table.docx table.csv

# Excel 转 Word
./scripts/doc-convert.sh data.xlsx report.docx

# PDF 转文本
./scripts/doc-convert.sh report.pdf report.txt
```

### 合并文档

```bash
# 合并 Word 文档
./scripts/doc-merge.sh part1.docx part2.docx -o merged.docx

# 合并 Excel（每个文件→独立 sheet）
./scripts/doc-merge.sh q1.xlsx q2.xlsx -o yearly.xlsx
```

### 提取数据

```bash
# 提取 Word 中的表格
python3 doc_processor.py --action extract \
  --input report.docx --options '{"include_tables": true}'

# 提取 Excel 指定 sheet
python3 doc_processor.py --action extract \
  --input data.xlsx --options '{"sheet_names": ["Sheet1"]}'
```

## Python API

```python
from doc_processor import DocumentProcessor

processor = DocumentProcessor(workspace="/path/to/workspace")

# 获取文档信息
info = processor.get_info("report.docx")
print(info.to_dict())

# 读取内容
content = processor.read("report.docx")
print(content.data['paragraphs'])

# 写入文档
processor.write("output.docx", {
    "title": "新文档",
    "paragraphs": ["内容 1", "内容 2"]
})

# 转换格式
processor.convert("input.docx", "output.csv")

# 合并文档
processor.merge(["a.docx", "b.docx"], "merged.docx")

# 提取数据
data = processor.extract("data.xlsx")
```

## 依赖说明

| 依赖 | 类型 | 用途 | 自动安装 |
|------|------|------|---------|
| poppler-utils | 系统 | PDF 读取 | ✅ (Linux/macOS) |
| python3 | 系统 | 运行环境 | ❌ (需预装) |
| python-docx | Python | Word 处理 | ✅ (setup.sh) |
| openpyxl | Python | Excel 读写 | ✅ (setup.sh) |
| pandas | Python | 数据处理 | ✅ (setup.sh) |

## 更新日志

### v1.0.4 (2026-03-25)
**Bug 修复:**
- ✅ 修复 Excel 写入失败问题 - 支持 `{'sheet_name': '...', 'data': [...]}` 格式
- ✅ 修复 Word 合并失败问题 - 正确处理相对路径，避免 "Package not found" 错误

### v1.0.3 (2026-03-25)
**Bug 修复:**
- ✅ 修复 CSV→Excel 转换问题
- ✅ 修复 DocInfo 属性问题

## 常见问题

### Q: 为什么不支持 .doc 和 .xls？

A: 这些是旧的二进制格式，需要 LibreOffice 转换。建议先用 LibreOffice 转换为 `.docx`/`.xlsx`：

```bash
libreoffice --headless --convert-to docx old.doc
libreoffice --headless --convert-to xlsx old.xls
```

### Q: PDF 写入支持吗？

A: 不支持。PDF 是只读格式。如需生成 PDF，可先创建 Word 文档再手动转换。

### Q: 大文件处理慢怎么办？

A: 建议使用 `--options` 限制读取范围：

```bash
# 只读取 PDF 前 5 页
python3 doc_processor.py --action read \
  --input large.pdf --options '{"pages": "1-5"}'
```

## 许可证

MIT License
