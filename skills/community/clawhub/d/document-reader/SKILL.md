---
name: document-reader
description: "通用文档读取工具，支持 PDF/DOCX/XLSX/PPTX/RTF/ODT 等多种文档格式，也支持 ZIP/TAR.GZ/RAR/7Z 等主流压缩包内文档直接读取"
version: "1.0.0"
---

# Document Reader - 通用文档读取技能

读取各种格式文档的内容，直接输出文本供 AI 分析。支持压缩包内文档直接读取，无需手动解压。

## 📦 支持格式

### 文档
| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | `.pdf` | 支持文本提取，依赖 poppler-utils |
| Microsoft Word | `.docx` | 完整提取所有段落文本 |
| Microsoft Excel | `.xlsx` | 按 Sheet 输出，每个 Sheet 输出为表格文本 |
| Microsoft PowerPoint | `.pptx` | 按 Slide 分块输出 |
| Rich Text Format | `.rtf` |  |
| OpenDocument Text | `.odt` |  |
| HTML | `.html`/`.htm` | 提取正文文本 |
| 纯文本 | `.txt`/`.md`/`.json`/`.xml`/`.py`/`.js` 等 | 直接读取 |

### 压缩包
| 格式 | 扩展名 | 功能 |
|------|--------|------|
| ZIP | `.zip` | 列出文件 ➜ 读取指定文档 |
| TAR | `.tar`/`.tar.gz`/`.tgz`/`.tar.bz2` | 列出文件 ➜ 读取指定文档 |
| RAR | `.rar` | 列出文件 ➜ 读取指定文档 |
| 7-Zip | `.7z` | 列出文件 ➜ 读取指定文档 |

## 🚀 快速开始

### 依赖安装

**Python 包：**
```bash
pip install textract python-docx openpyxl python-pptx rarfile py7zr --break-system-packages
```

**系统依赖（Ubuntu/Debian）：**
```bash
apt-get install -y poppler-utils antiword unrtf tidy libxml2-dev libxslt1-dev
```

## 💡 使用示例

### 1. 直接读取本地文档

```bash
# 读取 PDF 文件
python {baseDir}/scripts/document_reader.py --file /path/to/document.pdf

# 读取 Word 文档
python {baseDir}/scripts/document_reader.py --file /path/to/report.docx

# 读取 Excel 文件（输出带 Sheet 分隔的表格文本）
python {baseDir}/scripts/document_reader.py --file /path/to/data.xlsx

# JSON 格式输出（方便程序处理）
python {baseDir}/scripts/document_reader.py --file /path/to/data.xlsx --format json
```

### 2. 处理压缩包

**先列出压缩包里有哪些文件：**
```bash
# 列出 ZIP 包内容
python {baseDir}/scripts/document_reader.py --list /path/to/archive.zip

# 列出 RAR 包内容
python {baseDir}/scripts/document_reader.py --list /path/to/archive.rar

# 列出 7z 包内容
python {baseDir}/scripts/document_reader.py --list /path/to/archive.7z
```

**读取压缩包里的指定文档：**
```bash
# 读取 ZIP 包内的 Word 文档
python {baseDir}/scripts/document_reader.py --file /path/to/archive.zip --inner-path document.docx

# 读取 7z 包内的 PDF
python {baseDir}/scripts/document_reader.py --file /path/to/archive.7z --inner-path report.pdf
```

### 输出示例

**读取文档：**
```
=== report.pdf ===

# 项目进度报告

## 本周完成

1. 完成了前端界面开发
2. 修复了三个 Bug
3. 编写了接口文档

...
```

**列出压缩包：**
```
Archive: data.zip
Found 3 file(s):

  readme.txt
  docs/report.pdf
  data/sheet.xlsx
```

## ✨ 特性

- 🎯 **开箱即用** — 装完依赖直接用，无需复杂配置
- 📦 **支持压缩包** — 不用手动解压，直接列出并读取内部文件
- 🔍 **模糊匹配** — 大小写不敏感匹配文件名，找不到精确匹配时自动尝试
- 🎨 **多种输出格式** — 人类可读文本 / JSON 程序接口都支持
- 🧩 **完整支持所有常用格式** — 办公文档+压缩包全覆盖

## 📝 使用场景

- AI 分析各种办公文档
- 批量读取压缩包内的文档内容
- 快速查看附件内容
- 数据提取和预处理

## 作者

Created by xiaoya Liu with OpenClaw
