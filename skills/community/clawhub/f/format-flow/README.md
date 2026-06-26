# Format Flow - 格式流转

无缝多格式文档转换工具，支持 Word、PDF、Markdown 之间的互相转换。

## 🎯 功能概览

### 支持的转换

| 转换类型 | 说明 | 特性 |
|---------|------|------|
| **Word → PDF** | Word 文档转 PDF | ✅ 完整格式保留<br>✅ 图片、表格、页眉页脚 |
| **Word → Markdown** | Word 文档转 Markdown | ✅ **图片自动提取**<br>✅ **表格完美转换**<br>✅ 标题、列表、格式保留 |
| **PDF → Markdown** | PDF 转 Markdown | ✅ 文本提取<br>✅ 布局保留<br>⚠️ 仅文本(不支持图片提取) |
| **Markdown → Word** | Markdown 转 Word | ✅ 样式转换<br>✅ 图片嵌入<br>✅ 表格支持 |

## 📦 安装

### 方法 1: 手动安装

将 `format-flow` 目录复制到:
- **用户级别**: `~/.workbuddy/skills/` (推荐)
- **项目级别**: `.workbuddy/skills/`

### 方法 2: 导入 Skill 包

```bash
unzip format-flow.zip -d ~/.workbuddy/skills/
```

### 安装依赖

```bash
pip install python-docx pypandoc pdfplumber Pillow tqdm
```

**额外依赖:**

对于 **Markdown 转 Word** 功能,需要安装 pandoc:
- **Windows**: 下载 https://pandoc.org/installing.html
- **macOS**: `brew install pandoc`
- **Linux**: `sudo apt-get install pandoc`

## 🚀 使用方法

### 在 WorkBuddy 中使用

直接向 WorkBuddy 提问即可自动触发:

```
"把这个 Word 文件转成 Markdown"
"Convert this docx to Markdown"
"提取这个 PDF 的文本内容"
"将 Markdown 文档转为 Word 格式"
"批量转换这个文件夹里的所有 Word 文档"
```

### 命令行使用

```bash
# 进入脚本目录
cd ~/.workbuddy/skills/doc-converter/scripts

# 查看帮助
python convert.py --help

# Word 转 PDF
python convert.py word2pdf document.docx

# Word 转 Markdown (提取图片和表格)
python convert.py word2md document.docx

# PDF 转 Markdown
python convert.py pdf2md document.pdf

# Markdown 转 Word
python convert.py md2word document.md

# 批量转换
python convert.py word2md --batch ./documents

# 递归批量转换
python convert.py pdf2md --batch ./pdfs --recursive
```

### Python API 使用

```python
import sys
sys.path.insert(0, '~/.workbuddy/skills/doc-converter/scripts')

from convert import (
    word_to_pdf,
    word_to_markdown,
    pdf_to_markdown,
    markdown_to_word,
    batch_convert
)

# Word 转 PDF
word_to_pdf('report.docx', 'report.pdf')

# Word 转 Markdown (自动提取图片)
word_to_markdown('manual.docx', 'manual.md')

# PDF 转 Markdown
pdf_to_markdown('paper.pdf', 'paper.md')

# Markdown 转 Word
markdown_to_word('notes.md', 'notes.docx')

# 批量转换
success, fail = batch_convert('./docs', 'word2md', recursive=True)
print(f"成功: {success}, 失败: {fail}")
```

## ✨ 核心功能详解

### 1. Word 转 Markdown (⭐ 推荐功能)

**特点:**
- ✅ **图片自动提取**: 所有图片保存到 `images/` 文件夹
- ✅ **表格完美转换**: Word 表格转为 Markdown 表格
- ✅ **格式保留**: 粗体、斜体、标题、列表等

**输出示例:**

```
document.md          # Markdown 文件
document_images/     # 图片文件夹
  ├── image_1.png
  ├── image_2.jpg
  └── ...
```

**Markdown 内容:**

```markdown
# 文档标题

## 第一章

这是一段**粗体**和*斜体*文本。

![图片说明](document_images/image_1.png)

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |

- 列表项1
- 列表项2
```

### 2. PDF 转 Markdown

**特点:**
- ✅ 文本提取,保留基本布局
- ✅ 多列支持
- ✅ 表格提取(基础)

**限制:**
- ⚠️ **不支持图片提取** (仅提取文本)
- ⚠️ 扫描版 PDF 需要 OCR 工具
- ⚠️ 复杂布局可能丢失部分格式

**对于扫描版 PDF:**

需要先进行 OCR 处理:
```bash
# 使用 Tesseract OCR
tesseract scanned.pdf output -l chi_sim+eng

# 或使用在线 OCR 工具
```

### 3. Markdown 转 Word

**特点:**
- ✅ 标题样式自动应用
- ✅ 图片嵌入文档
- ✅ 表格转换
- ✅ 代码块格式化

**需要 pandoc:**
```bash
# 安装 pandoc (推荐)
# Windows: 下载安装包
# macOS: brew install pandoc
# Linux: sudo apt-get install pandoc
```

## 📋 使用场景

### 场景 1: Word 文档转 Markdown 发布到 GitHub

```bash
python convert.py word2md Manual.docx README.md
# 生成 README.md 和 Manual_images/ 图片文件夹
# 直接推送到 GitHub 即可
```

### 场景 2: 从 PDF 论文中提取文本

```bash
python convert.py pdf2md paper.pdf paper.md
# 提取文本内容,方便引用和翻译
```

### 场景 3: Markdown 笔记转 Word 分享

```bash
python convert.py md2word meeting-notes.md meeting-notes.docx
# 转为 Word 格式,方便与同事分享
```

### 场景 4: 批量转换文档库

```bash
# 转换整个文档文件夹
python convert.py word2md --batch ./docs --recursive

# 递归处理所有子目录
python convert.py pdf2md --batch ./papers -r
```

## 🔧 高级配置

### 自定义图片提取路径

```python
from convert import word_to_markdown

# 指定图片保存路径
word_to_markdown('doc.docx', 'output.md', extract_images=True)
```

### 处理大型文档

对于超过 50MB 的大文件:
- 增加 Python 内存限制
- 分批处理
- 使用 `--quiet` 模式减少输出

## 🆘 常见问题

### 1. "pandoc not found" 错误

**问题**: Markdown 转 Word 时提示找不到 pandoc

**解决**:
```bash
# 下载安装 pandoc
# https://pandoc.org/installing.html

# 或使用 conda
conda install -c conda-forge pandoc
```

### 2. PDF 提取的文本格式混乱

**原因**: PDF 本身是排版格式,不包含结构信息

**解决**:
- 尝试不同的 PDF 阅读器(Adobe Reader, Chrome, Edge)
- 使用专业 PDF 转换工具
- 对于扫描版,先进行 OCR

### 3. Word 转 Markdown 图片丢失

**检查**:
- 确认 Word 文档中确实包含图片
- 查看是否有 `images/` 文件夹生成
- 检查 Markdown 中的图片引用路径

### 4. 表格转换不完美

**原因**: Markdown 表格功能有限

**解决**:
- 简单表格:转换效果好
- 复杂表格:需要手动调整
- 合并单元格:Markdown 不支持,需拆分

### 5. 中文 PDF 提取乱码

**解决**:
- 确认 PDF 使用了嵌入字体
- 尝试其他 PDF 库: `PyPDF2`, `pdfminer`
- 使用 OCR 工具重新识别

## 📊 转换质量对比

| 转换类型 | 文本 | 图片 | 表格 | 格式 | 评分 |
|---------|------|------|------|------|------|
| Word → PDF | ✅ 完美 | ✅ 完美 | ✅ 完美 | ✅ 完美 | ⭐⭐⭐⭐⭐ |
| Word → MD | ✅ 完美 | ✅ 提取 | ✅ 良好 | ✅ 良好 | ⭐⭐⭐⭐⭐ |
| PDF → MD | ✅ 良好 | ❌ 不支持 | ⚠️ 基础 | ⚠️ 基础 | ⭐⭐⭐ |
| MD → Word | ✅ 完美 | ✅ 嵌入 | ✅ 良好 | ✅ 良好 | ⭐⭐⭐⭐ |

## 🔄 批量转换示例

```bash
# 转换所有 Word 文档为 Markdown
python convert.py word2md --batch ./my-docs

# 递归转换所有子目录
python convert.py word2md --batch ./my-docs --recursive

# 安静模式批量处理
python convert.py pdf2md --batch ./pdfs -r -q
```

## 📝 更新日志

### v2.0.0 (2026-03-18)
- ✨ 新增 Word 转 Markdown (图片提取)
- ✨ 新增 PDF 转 Markdown
- ✨ 新增 Markdown 转 Word
- ✨ 批量转换支持
- ✨ 递归目录处理
- ✅ 自动依赖安装
- ✅ 进度条显示

### v1.0.0
- ✅ Word 转 PDF 基础功能

## 📄 许可证

MIT License

## 👨‍💻 作者

Created by WorkBuddy Skill Creator

---

**提示**: Word 转 Markdown 功能最成熟,推荐用于文档转换!
