---
name: doc-translate
description: Office文档翻译工具集。用于翻译和本地化办公文档（PPT/Word/PDF/Excel），保持原文档模板和格式不变。当用户说"翻译PPT"、"翻译Word文档"、"翻译PDF"、"翻译Excel"、"翻译文档"、"文档本地化"、"英文文档翻译成中文"时使用本技能。支持PPT/Word/PDF/Excel四种格式的英文到中文（或任意语言）的翻译任务。
---

# doc-translate

Office document translation toolkit / Office文档翻译工具集

Supports PPTX / DOCX / PDF / XLSX four formats, preserving original templates and styles / 支持四种格式，保持原模板不变。

---

## 工作流 / Workflow

### 通用流程 / General Process（所有格式 / All Formats）

```
1. 下载文件 / Download file      → 飞书附件 or 本地路径 / Feishu attachment or local path
2. 格式识别 / Detect format       → 根据扩展名判断 / Detect by extension
3. 解压解析 / Extract & parse     → ZIP解压 → XML/文本节点提取 / ZIP extract → XML/text node extraction
4. 翻译 / Translate              → 规则映射或AI翻译 / Rule mapping or AI translation
5. 重建 / Rebuild                → 重新打包，保留原样式 / Repack, preserve original styles
6. 发送 / Deliver                → 发送给用户或保存 / Send to user or save
```

---

## PPTX 翻译 / PPTX Translation

### 格式结构 / Format Structure

PPTX = ZIP压缩包，内含 / ZIP archive containing:
- `ppt/slides/slide1.xml` … slideN.xml — 幻灯片内容 / Slide content
- `ppt/theme/` — 主题样式 / Theme styles
- `[Content_Types].xml` — 内容类型声明 / Content type declarations

### 关键XML节点 / Key XML Nodes

| 节点 / Node | 说明 / Description |
|-------------|-------------------|
| `<a:t>` | 文本内容 / Text content（最常出现 / most common）|
| `<a:r>` | 文本段落 / Text run |
| `<p:sp>` | 形状（文本框等）/ Shape（text box etc.）|
| `<p:txBody>` | 文本正文 / Text body |

### 处理脚本 / Processing Script

```bash
python3 scripts/pptx_translate.py <pptx文件路径> [--output <输出路径>] [--src-lang en] [--tgt-lang zh]
```

---

## DOCX 翻译 / DOCX Translation

### 格式结构 / Format Structure

DOCX = ZIP压缩包，内含 / ZIP archive containing:
- `word/document.xml` — 主文档内容 / Main document content
- `word/styles.xml` — 样式 / Styles
- `[Content_Types].xml`

### 关键XML节点 / Key XML Nodes

| 节点 / Node | 说明 / Description |
|-------------|-------------------|
| `<w:t>` | 文本内容 / Text content |
| `<w:p>` | 段落 / Paragraph |
| `<w:r>` | 文本段 / Text run |

### 处理脚本 / Processing Script

```bash
python3 scripts/docx_translate.py <docx文件路径> [--output <输出路径>]
```

---

## XLSX 翻译 / XLSX Translation

### 格式结构 / Format Structure

XLSX = ZIP压缩包，内含 / ZIP archive containing:
- `xl/worksheets/sheet1.xml` — 工作表内容 / Worksheet content
- `xl/sharedStrings.xml` — 共享字符串表（单元格文本） / Shared strings table（cell text）
- `xl/styles.xml` — 样式 / Styles

### 处理脚本 / Processing Script

```bash
python3 scripts/xlsx_translate.py <xlsx文件路径> [--output <输出路径>]
```

---

## PDF 翻译 / PDF Translation

### 方法说明 / Method Notes

PDF不是XML格式，无法直接编辑文本。推荐方案 / PDF is not XML, cannot edit text directly. Recommended approach:

**方案A / Method A：PDF → Word → PDF（推荐 / Recommended）**
```
pdfplumber提取文本 → python-docx构建翻译后Word文档 → LibreOffice导出PDF
pdfplumber extract → python-docx build translated Word → LibreOffice export PDF
```

**方案B / Method B：直接覆盖（仅文本层PDF） / Direct overlay (text-layer PDFs only）**
使用 pdfplumber + pypdf2 / Using pdfplumber + pypdf2

### 处理脚本 / Processing Script

```bash
python3 scripts/pdf_translate.py <pdf文件路径> [--output <输出路径>] [--method word|direct]
```

---

## 飞书文件处理 / Feishu File Handling

### 下载飞书附件 / Download Feishu Attachment

```python
# 飞书消息附件下载（message_id 来自上下文）/ Feishu message attachment download
feishu_im_bot_image(message_id="om_xxx", file_key="file_v3_xxx", type="file")
# 返回 saved_path / Returns saved_path

# 飞书云盘文件下载 / Feishu drive file download
feishu_drive_file(action="download", file_token="xxx", output_path="/tmp/output.pptx")
```

### 发送文件给用户 / Send File to User

**方法1：消息附件发送（限制25MB）/ Method 1: Message attachment (25MB limit）**
```python
message(action="send", channel="feishu", file_path="/path/to/file.pptx", target="user:ou_xxx")
```

**方法2：分卷发送（文件>25MB时）/ Method 2: Split send (file > 25MB）**
```bash
# 分成10MB分卷 / Split into 10MB chunks
split -b 10m original.pptx part-
# 逐个发送 / Send one by one
message(action="send", file_path="part-aa", target="user:ou_xxx")
# 用户合并命令 / User merge command:
cat part-* > original.pptx
```

**方法3：上传飞书云盘 / Method 3: Upload to Feishu Drive**
```python
feishu_drive_file(action="upload", file_path="/path/to/file.pptx", file_name="翻译版.pptx")
```

---

## 翻译质量注意事项 / Translation Quality Notes

1. **医学/专业术语 / Medical/Technical Terms** — 必须使用人工翻译映射表，不能让模型自由发挥 / Must use manual translation mapping, not free-form AI
2. **商标/品牌 / Trademarks/Brands** — 保持原文，如 Medtronic、Harmonic 等 / Keep original, e.g. Medtronic, Harmonic
3. **数字+单位 / Numbers+Units** — 保持原样，如 7mm、150 procedures / Keep as-is, e.g. 7mm, 150 procedures
4. **脚注符号 / Footnote Symbols** — † ‡ § Ω 等保持不变 / Keep as-is: † ‡ § Ω
5. **格式占位符 / Format Placeholders** — 如 {name}、%s 等不替换 / Don't replace: {name}, %s

---

## 脚本列表 / Scripts

| 脚本 / Script | 功能 / Function | 输入 / Input | 输出 / Output |
|---|---|---|---|
| `pptx_translate.py` | PPTX全文翻译 / Full PPTX translation | .pptx文件 | .pptx（中文版 / Chinese version）|
| `docx_translate.py` | DOCX全文翻译 / Full DOCX translation | .docx文件 | .docx（中文版 / Chinese version）|
| `xlsx_translate.py` | XLSX全文翻译 / Full XLSX translation | .xlsx文件 | .xlsx（中文版 / Chinese version）|
| `pdf_translate.py` | PDF全文翻译 / Full PDF translation | .pdf文件 | .pdf（中文版 / Chinese version）|

All scripts use `--output` to specify output path / 所有脚本使用 `--output` 指定输出路径
