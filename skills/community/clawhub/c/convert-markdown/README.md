# convert-markdown

文档转换技能 - 基于 Microsoft MarkItDown 的多格式文档转 Markdown 工具。

## 简介

本技能支持将 PDF、Word、PowerPoint、Excel、图片、音频等多种格式文件批量转换为 Markdown 格式，适用于文档数字化、知识库构建、内容提取等场景。

## 功能特性

- **多格式支持**：PDF、DOCX、PPTX、XLSX、图片、音频、HTML、CSV、JSON、ZIP、EPub、YouTube URLs 等
- **结构化保留**：保持标题、列表、表格、链接等重要文档结构
- **批量处理**：支持目录递归处理和批量转换
- **OCR 能力**：图片和扫描 PDF 的文本识别
- **音频转录**：音频文件的语音转文本

## 安装

### 环境要求

- Python 3.10 或更高版本
- Node.js 14.0+（使用 NPX CLI 时需要）

### 安装步骤

```bash
# 创建虚拟环境（推荐）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装完整功能
pip install 'markitdown[all]'

# 或按需安装特定格式支持
pip install 'markitdown[pdf,docx,pptx]'
```

## 使用方法

### NPX CLI 方式（推荐）

本技能提供 NPX CLI 工具，可直接通过 npx 命令调用：

```bash
# 查看帮助
npx convert-markdown

# 转换单个文件
npx convert-markdown convert --input document.pdf --output document.md

# 转换目录
npx convert-markdown convert --input ./docs --output ./markdown

# 批量转换（指定格式）
npx convert-markdown batch --source ./docs --target ./markdown --include .pdf,.docx

# 覆盖已存在文件
npx convert-markdown convert --input document.pdf --output document.md --overwrite
```

**CLI 命令说明：**

| 命令 | 说明 | 参数 |
|------|------|------|
| `convert` | 转换文件或目录 | `--input`, `--output`, `--overwrite` |
| `batch` | 批量转换目录 | `--source`, `--target`, `--include`, `--exclude` |

### MarkItDown 命令行方式

```bash
# 转换单个文件
markitdown document.pdf > document.md
markitdown presentation.pptx -o slides.md

# 批量处理目录
markitdown ./docs/ --recursive -o ./output/
```

### Python API 方式

```python
from markitdown import MarkItDown

# 创建转换器实例
md = MarkItDown()

# 转换文件
result = md.convert("document.pdf")
print(result.text_content)

# 转换并保存
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
```

## 目录结构

```
convert-markdown/
├── bin/                   # NPX CLI 入口
│   └── convert-markdown.js
├── scripts/               # Python 脚本
│   ├── cli.py             # CLI 实现
│   ├── batch_convert.py   # 批量转换脚本
│   └── convert_markonverter.py
├── references/            # 参考文档
│   ├── API_REFERENCE.md   # API 参考
│   ├── FORMATS.md         # 支持格式列表
│   └── PDF_CONFIG.md      # PDF 配置指南
├── package.json           # Node.js 包配置
├── manifest.json          # 技能定义
├── SKILL.md               # 详细技能文档
└── README.md              # 本文件
```

## 快速示例

### 批量转换知识库文档

```bash
npx convert-markdown batch --source ./source_documents --target ./converted_docs
```

### 处理扫描版 PDF

```bash
pip install 'markitdown[pdf]'  # 包含 OCR 功能
npx convert-markdown convert --input scanned_document.pdf --output text.md
```

### 提取表格数据

```bash
npx convert-markdown convert --input financial_report.xlsx --output report.md
```

## 详细文档

更多使用方法和高级配置，请查看 [SKILL.md](SKILL.md)。

## 依赖说明

可选依赖组：
- `[all]` - 所有格式支持
- `[pdf]` - PDF 处理（包含 OCR）
- `[docx]` - Word 文档
- `[pptx]` - PowerPoint
- `[xlsx]` - Excel
- `[image]` - 图片 EXIF 和 OCR
- `[audio]` - 音频转录

## 版本信息

- 当前版本：1.0.2
- 基于：MarkItDown 0.1.0+

## 相关链接

- [MarkItDown PyPI](https://pypi.org/project/markitdown/)
- [GitHub 仓库](https://github.com/microsoft/markitdown)
