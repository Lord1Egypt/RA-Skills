---
name: format-flow
description: Seamless multi-format document conversion toolkit supporting Word ↔ PDF ↔ Markdown conversion, web page to Markdown, text formatting, Excel to JSON, and image processing (compression, format conversion, resizing). Use when user mentions converting documents, extracting text, formatting notes, converting Excel to JSON, or processing images. Keywords: format flow, convert, Word to PDF, Word to Markdown, PDF to Markdown, Markdown to Word, web to Markdown, text formatting, Excel to JSON, image compression, image conversion, image resizing, document conversion, format conversion, extract text, 文档转换, 格式转换, 格式流转, Word转PDF, Word转Markdown, PDF转Markdown, Markdown转Word, 网页转Markdown, 文本格式化, Excel转JSON, 图片压缩, 图片转换, 图片调整.
---

# Format Flow - 格式流转

多功能的文档格式转换工具集，支持文档、网页、文本、数据表格、图片等多种格式的相互转换。

## 核心功能

### 📄 文档转换（Word/PDF/Markdown）
- **Word → PDF**: 高质量转换，完美保留格式
- **Word → Markdown**: 自动提取图片、表格转换
- **PDF → Markdown**: 文本提取，保留布局
- **Markdown → Word**: 格式化文档生成

### 🌐 网页处理
- **网页 → Markdown**: URL/HTML 文件转 Markdown，智能提取内容

### 📝 文本格式化
- **文本格式化**: 8 种格式化操作（规范化、标题、段落、列表等）

### 📊 数据转换
- **Excel → JSON**: 4 种 JSON 格式（records、grouped、nested、array）

### 🖼️ 图片处理
- **图片压缩**: 可调质量参数
- **格式转换**: PNG/JPEG/WEBP/GIF/BMP 互转
- **尺寸调整**: 固定尺寸或比例缩放

## 触发词与使用场景

### 文档转换类

#### Word 转 PDF
**触发词**:
- 中文: "Word转PDF", "Word转换成PDF", "docx转pdf", "把Word转成PDF"
- 英文: "convert Word to PDF", "Word to PDF", "docx to pdf"
- 场景: "将Word文档转换为PDF", "我需要把这份Word转成PDF格式"

**使用示例**:
```bash
# 单文件
python scripts/convert.py word2pdf document.docx

# 批量转换
python scripts/convert.py word2pdf --batch ./documents --recursive
```

#### Word 转 Markdown
**触发词**:
- 中文: "Word转Markdown", "Word转MD", "docx转markdown", "提取Word文本"
- 英文: "convert Word to Markdown", "Word to Markdown", "docx to md"
- 场景: "把Word文档转成Markdown", "提取Word中的图片", "Word发布到GitHub"

**使用示例**:
```bash
# 转换并提取图片
python scripts/convert.py word2md document.docx

# 批量转换
python scripts/convert.py word2md --batch ./documents

# 不提取图片
python scripts/convert.py word2md document.docx --no-images
```

#### PDF 转 Markdown
**触发词**:
- 中文: "PDF转Markdown", "提取PDF文本", "PDF转MD", "PDF内容提取"
- 英文: "convert PDF to Markdown", "PDF to Markdown", "extract PDF text"
- 场景: "从PDF中提取文本", "PDF转成可编辑的Markdown"

**使用示例**:
```bash
python scripts/convert.py pdf2md document.pdf
python scripts/convert.py pdf2md --batch ./pdfs
```

#### Markdown 转 Word
**触发词**:
- 中文: "Markdown转Word", "MD转Word", "markdown转docx"
- 英文: "convert Markdown to Word", "Markdown to Word", "md to docx"
- 场景: "把Markdown转成Word文档", "Markdown转Word格式"

**使用示例**:
```bash
python scripts/convert.py md2word document.md
python scripts/convert.py md2word --batch ./markdown
```

### 网页处理类

#### 网页转 Markdown
**触发词**:
- 中文: "网页转Markdown", "网页转MD", "HTML转Markdown", "抓取网页", "保存网页"
- 英文: "convert web page to Markdown", "web to Markdown", "HTML to Markdown", "webpage to md"
- 场景: "把网页保存为Markdown", "抓取网页内容", "HTML转Markdown"

**使用示例**:
```bash
# 从URL转换
python scripts/convert.py web2md https://example.com

# 从HTML文件转换
python scripts/convert.py web2md page.html

# 批量转换HTML文件
python scripts/convert.py web2md --batch ./html_files
```

### 文本处理类

#### 文本格式化
**触发词**:
- 中文: "文本格式化", "格式化文本", "整理笔记", "文本规范化", "文本美化"
- 英文: "format text", "text formatting", "beautify text", "organize notes"
- 场景: "整理这份笔记", "格式化这段文本", "规范化文本格式"

**使用示例**:
```bash
# 完整格式化
python scripts/convert.py textfmt notes.txt --operations normalize titles paragraphs

# 添加行号
python scripts/convert.py textfmt code.txt --operations line_numbers

# 生成大纲
python scripts/convert.py textfmt document.txt --operations outline
```

**支持的格式化操作**:
- `normalize`: 规范化空白字符和标点
- `titles`: 格式化标题（添加下划线）
- `paragraphs`: 格式化段落（统一缩进）
- `lists`: 格式化列表
- `line_numbers`: 添加行号
- `outline`: 提取大纲
- `toc`: 生成目录
- `timestamp`: 添加时间戳

### 数据转换类

#### Excel 转 JSON
**触发词**:
- 中文: "Excel转JSON", "表格转JSON", "xlsx转json", "Excel数据导出"
- 英文: "convert Excel to JSON", "Excel to JSON", "xlsx to json"
- 场景: "把Excel表格转成JSON", "导出Excel数据为JSON格式"

**使用示例**:
```bash
# 记录格式（默认）
python scripts/convert.py excel2json data.xlsx --format records

# 分组格式
python scripts/convert.py excel2json data.xlsx --format grouped --group-by category

# 嵌套格式
python scripts/convert.py excel2json data.xlsx --format nested --group-by department,name

# 数组格式
python scripts/convert.py excel2json data.xlsx --format array

# 指定工作表
python scripts/convert.py excel2json data.xlsx --sheet "Sheet2"
```

**JSON 格式说明**:
- `records`: 对象数组 `[{"name": "Alice", "age": 30}, ...]`
- `grouped`: 按列分组 `{"group1": [records...], ...}`
- `nested`: 多级嵌套分组
- `array`: 行数组 `[[headers...], [row1...], ...]`

### 图片处理类

#### 图片压缩
**触发词**:
- 中文: "图片压缩", "压缩图片", "减小图片大小", "优化图片"
- 英文: "compress image", "image compression", "reduce image size"
- 场景: "压缩这张图片", "减小图片文件大小", "优化图片加载速度"

**使用示例**:
```bash
# 默认质量(85)
python scripts/convert.py imgcompress photo.jpg

# 指定质量(0-100)
python scripts/convert.py imgcompress photo.png --quality 70

# 批量压缩
python scripts/convert.py imgcompress --batch ./images --quality 80
```

#### 图片格式转换
**触发词**:
- 中文: "图片格式转换", "转换图片格式", "PNG转JPG", "图片转PNG", "图片转JPEG"
- 英文: "convert image format", "image format conversion", "PNG to JPG", "convert to PNG"
- 场景: "把PNG转成JPG", "转换图片格式为JPEG", "图片格式互转"

**使用示例**:
```bash
# 转换为JPEG
python scripts/convert.py imgconvert photo.png --format jpeg

# 转换为PNG
python scripts/convert.py imgconvert photo.jpg --format png

# 转换为WEBP
python scripts/convert.py imgconvert photo.jpg --format webp

# 批量转换
python scripts/convert.py imgconvert --batch ./images --format webp
```

#### 图片尺寸调整
**触发词**:
- 中文: "调整图片大小", "图片缩放", "修改图片尺寸", "调整图片分辨率"
- 英文: "resize image", "image resizing", "scale image", "change image size"
- 场景: "调整图片尺寸", "缩放这张图片", "修改图片大小"

**使用示例**:
```bash
# 固定尺寸
python scripts/convert.py imgresize photo.jpg --width 800 --height 600

# 只指定宽度（高度自动计算）
python scripts/convert.py imgresize photo.jpg --width 800

# 比例缩放
python scripts/convert.py imgresize photo.jpg --scale 0.5

# 批量调整
python scripts/convert.py imgresize --batch ./images --scale 0.8
```

## 功能状态检查

查看所有功能的可用性：
```bash
python scripts/convert.py --status
```

输出示例：
```
Document Converter v3.0 - Status Check

Document Conversions:
  Word → PDF:        Available (docx2pdf)
  Word → Markdown:   Available
  PDF → Markdown:    Available
  Markdown → Word:   Available (pypandoc)

Web Processing:
  Web → Markdown:    Available

Text Processing:
  Text Formatting:   Available

Data Conversion:
  Excel → JSON:      Available (openpyxl)

Image Processing:
  Image Compress:    Available (Pillow)
  Image Convert:     Available (Pillow)
  Image Resize:      Available (Pillow)
```

## 模块化架构

```
scripts/
├── convert.py                 # 主入口 (CLI)
│
├── converters/                # 转换器模块
│   ├── word_to_pdf.py        # Word → PDF
│   ├── word_to_markdown.py   # Word → Markdown
│   ├── pdf_to_markdown.py    # PDF → Markdown
│   ├── markdown_to_word.py   # Markdown → Word
│   ├── web_to_markdown.py    # 网页 → Markdown
│   ├── text_formatter.py     # 文本格式化
│   ├── excel_to_json.py      # Excel → JSON
│   └── image_processor.py    # 图片处理
│
└── utils/                     # 工具模块
    ├── dependencies.py        # 依赖管理
    └── helpers.py             # 辅助函数
```

## 转换质量矩阵

| 转换类型 | 文本质量 | 格式保留 | 图片处理 | 表格支持 | 综合评分 |
|---------|:-------:|:-------:|:-------:|:-------:|:-------:|
| **Word → PDF** | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | **5.0** |
| **Word → Markdown** | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | **4.8** |
| **PDF → Markdown** | ★★★★☆ | ★★★☆☆ | ✗ | ★★★☆☆ | **3.5** |
| **Markdown → Word** | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ | **4.5** |
| **Web → Markdown** | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★☆ | **4.2** |
| **Text Formatting** | ★★★★★ | ★★★★★ | - | - | **5.0** |
| **Excel → JSON** | ★★★★★ | ★★★★★ | - | ★★★★★ | **5.0** |
| **Image Processing** | - | ★★★★★ | ★★★★★ | - | **5.0** |

## 依赖管理

### 自动安装的依赖
```bash
pip install python-docx pdfplumber Pillow tqdm
```

### 可选依赖（增强功能）
```bash
pip install docx2pdf      # Word → PDF (Windows + MS Word)
pip install pypandoc      # 增强 Markdown → Word
pip install beautifulsoup4 # Web → Markdown
pip install openpyxl      # Excel → JSON
```

## 最佳实践

### 1. 选择合适的转换路径

**文档发布**: Word → Markdown (★★★★★)
**文档归档**: Word → PDF (★★★★★)
**内容编辑**: Markdown → Word (★★★★☆)
**内容提取**: PDF → Markdown (★★★☆☆)

### 2. 批量处理

处理大量文件时使用批量模式：
```bash
python scripts/convert.py word2md --batch ./documents --recursive
```

### 3. 自动化脚本

使用静默模式进行自动化：
```bash
python scripts/convert.py word2pdf document.docx --quiet
```

### 4. 图片处理建议

- **压缩**: 用于网页加载，质量 70-85
- **格式转换**: PNG 用于透明图，JPEG 用于照片
- **尺寸调整**: 网页图片宽度建议 800-1200px

## 常见问题

### 1. Word → PDF 在 Linux/macOS 失败
**原因**: docx2pdf 需要 Microsoft Word（仅 Windows）

**解决方案**: 安装 LibreOffice
```bash
# Ubuntu/Debian
sudo apt-get install libreoffice

# macOS
brew install libreoffice
```

### 2. PDF 文本提取质量差
**原因**: 扫描版 PDF 或复杂布局

**解决方案**: 使用 OCR 工具预处理
```bash
ocrmypdf input.pdf output.pdf
```

### 3. 网页转换失败
**原因**: 网络问题或网站反爬

**解决方案**: 
- 检查网络连接
- 使用本地 HTML 文件
- 添加 User-Agent（高级用法）

### 4. Excel 转换乱码
**原因**: 编码问题

**解决方案**: 确保源文件为 UTF-8 编码

## 版本历史

### v3.0 (当前版本)
- ✅ 新增网页转 Markdown 功能
- ✅ 新增文本格式化功能
- ✅ 新增 Excel 转 JSON 功能
- ✅ 新增图片处理功能（压缩/转换/调整）
- ✅ 完善依赖管理系统
- ✅ 扩展 CLI 支持 10 种转换类型

### v2.0
- ✅ 模块化架构重构
- ✅ 独立的转换器模块
- ✅ 改进错误处理和日志

### v1.0
- 初始版本，单文件结构

## 贡献指南

添加新转换类型的步骤：
1. 在 `scripts/converters/` 创建新模块
2. 实现 `convert_TYPE1_to_TYPE2()` 函数
3. 更新 `converters/__init__.py`
4. 在 `convert.py` 添加 CLI 命令
5. 更新文档和触发词

## 许可证

MIT License - 详见 LICENSE 文件

## 资源

### 脚本
- `scripts/convert.py` - 主入口
- `scripts/converters/` - 转换器模块
- `scripts/utils/` - 工具函数

### 文档
- `README.md` - 详细使用指南
- `SKILL.md` - 本文档

---

**快速开始**: `python scripts/convert.py --help`
