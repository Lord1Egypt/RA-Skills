---
name: doc-format-brush
description: 文档格式刷 skill。当用户需要将某个文档的格式调整成与另一个模板文档完全一致时使用，支持任意格式文档（Word、Markdown、纯文本）的格式整理。包括字体、字号、对齐方式、首行缩进、行距、段前段后间距、页边距等。更支持智能识别标题层级（标题、一级标题、二级标题、正文），应用不同格式。支持内置公文格式（GB/T 9704-2012）。触发场景：用户说"格式对齐到模板"、"参照某文件的格式"、"格式刷"、"格式和XXX文档一样"、"把文档改成公文格式"、"使用公文格式"、"把Markdown转成Word格式"等。
---

# 文档格式刷 (Doc Format Brush)

## 概述

本 skill 提供多格式文档格式整理功能：**提取**模板文档的格式 → **应用**到任意格式的目标文档。

### 核心功能

1. **多格式支持**：输入/输出支持 Word(.docx)、Markdown(.md)、纯文本(.txt)
2. **智能标题层级识别**：自动识别标题、一级标题（"一、"）、二级标题（"（一）"）、正文
3. **格式精确复制**：字体、字号、加粗、对齐、首行缩进（字符级）、段前间距、段后间距、行间距、页边距
4. **内置公文格式**：支持一键应用 GB/T 9704-2012 国家标准公文格式

---

## 使用方式

### 方式一：使用内置公文格式（推荐）

当用户需要将文档调整为标准公文格式时：

```bash
python apply_multi_format.py <输入文档> --official --output <输出文档>
```

**支持的输入格式**：.docx, .md, .txt
**支持的输出格式**：.docx, .md, .txt

**示例：**
```bash
# Markdown 转 Word 公文格式
python apply_multi_format.py 报告.md --official --output 报告_公文.docx

# 纯文本转 Markdown
python apply_multi_format.py 笔记.txt --official --output 笔记.md

# Word 转为 Word（使用公文格式）
python apply_multi_format.py 财务报告.docx --official --output 财务报告_公文格式.docx
```

---

### 方式二：参照模板文档

当用户提供了特定的模板文档时：

**从模板提取格式后应用到目标：**
```bash
python apply_multi_format.py <目标文档> <模板.docx> --output <输出文档>
```

**示例：**
```bash
# 参照 Word 模板，调整 Markdown 文件
python apply_multi_format.py 报告.md 模板.docx --output 报告_新格式.docx

# 参照模板，转换 Word 到 Word
python apply_multi_format.py 源文件.docx 模板.docx --output 目标文件.docx
```

---

### 方式三：使用格式描述文件

可以先提取模板格式为 JSON，然后复用：

```bash
# 提取格式
python extract_format.py 模板.docx --output 格式.json

# 应用格式
python apply_multi_format.py 输入.md --format-json 格式.json --输出 输出.docx
```

---

## 内置公文格式规范（GB/T 9704-2012）

| 段落类型 | 字体 | 字号 | 对齐 | 缩进 | 段前 | 段后 | 行距 |
|---------|------|------|------|------|------|------|------|
| 标题 | 方正小标宋体 | 22pt（二号） | 居中 | 0 | 0pt | 0pt | 1.5倍 |
| 文号 | 仿宋_GB2312 | 16pt（三号） | 居中 | 0 | 0pt | 0pt | 1.5倍 |
| 一级标题 | 黑体 | 16pt（三号） | 左对齐 | 0 | 0pt | 0pt | 1.5倍 |
| 二级标题 | 楷体_GB2312 | 16pt（三号） | 左对齐 | 0 | 0pt | 0pt | 1.5倍 |
| 正文 | 仿宋_GB2312 | 16pt（三号） | 两端对齐 | 2字符 | 0pt | 0pt | 1.5倍 |

**页面设置：**
- 纸张：A4（21cm × 29.7cm）
- 页边距：上 3.7cm，下 3.5cm，左 2.8cm，右 2.6cm

---

## 标题层级识别规则

### Word/文本识别规则

| 类型 | 识别规则 | 示例 |
|------|---------|------|
| 标题 | 第一个非空段落 | 关于xxx的请示 |
| 文号 | 第二个段落，符合公文号格式 | X发〔2024〕10号 |
| 一级标题 | 以"一、"、"二、"等开头 | 一、基本情况 |
| 二级标题 | 以"（一）"、"（二）"等开头 | （一）主要业绩 |
| 正文 | 其他段落 | 正文内容... |

### Markdown 识别规则

| Markdown 标记 | 对应层级 |
|--------------|---------|
| # Title | 标题 |
| ## Heading | 一级标题 |
| ### Subheading | 二级标题 |
| - List item | 正文（列表项） |
| 普通文本 | 正文 |

---

## 格式转换矩阵

| 输入格式 | 支持的输出格式 | 说明 |
|---------|---------------|------|
| .docx | .docx, .md, .txt | 保留格式信息 |
| .md | .docx, .md, .txt | 识别标题层级 |
| .txt | .docx, .md, .txt | 智能识别标题 |

---

## 脚本位置

本 skill 包含以下脚本：

| 脚本 | 功能 |
|------|------|
| `extract_format.py` | 从 Word 模板提取格式 → 输出 JSON |
| `apply_format.py` | 应用格式到 Word 文档 |
| `apply_multi_format.py` | **【推荐】**多格式统一处理入口 |
| `format_bridge.py` | 多格式文档读写核心库 |

脚本目录：`C:\Users\14032\.codebuddy\skills\doc-format-brush\scripts\`

---

## 常见错误与修正

| 错误现象 | 原因 | 修正方式 |
|----------|------|----------|
| 首行缩进显示为厘米而非字符 | 使用了 `Cm()` 而非 XML 属性 | 使用 `w:firstLineChars` 设置字符数 |
| 段后间距仍有 10pt | Word Normal 样式默认值未覆盖 | 强制 `pf.space_after = Pt(0)` |
| 对齐方式为左对齐而非两端对齐 | 未正确设置 JUSTIFY | 使用 `WD_ALIGN_PARAGRAPH.JUSTIFY` |
| 中文字体未变化 | 只设了 `font.name` | 同时设置 `w:eastAsia` 属性 |
| 文件保存报 PermissionError | 目标文件在 Word 中打开 | 换一个新文件名保存 |

---

## 典型对话示例

**用户 A：** "把这份 Markdown 报告改成公文格式 Word"

**AI：** 使用内置公文格式处理 Markdown：
```bash
python apply_multi_format.py 报告.md --official --output 报告_公文格式.docx
```

**用户 B：** "参照这个 Word 模板，调整我的笔记文件"

**AI：** 参照模板格式处理：
```bash
python apply_multi_format.py 我的笔记.md 模板.docx --output 笔记_整理.docx
```

**用户 C：** "把这个文本文件转成带格式的 Markdown"

**AI：** 使用内置格式输出 Markdown：
```bash
python apply_multi_format.py 原始笔记.txt --official --output 格式化笔记.md
```
