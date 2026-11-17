---
name: docx-typesetting-from-markdown
description: 当用户需要将 Markdown 文档转换为排版精良的 DOCX 时使用。支持多级标题、列表、表格、引用块、提示块、分页控制，生成层次清晰、避免孤行寡行的 Word 文档。
---

# Markdown 转精排版 DOCX

## 概述

该 skill 用于把 Markdown 源文件转换为格式规范、适合阅读/打印的 DOCX 文档。核心解决两类问题：

1. **视觉层级不清**：标题、正文、提示、表格使用统一字号/粗细，导致整篇文档看起来"一团粗"。
2. **分页断行不自然**：标题与正文被分页断开、列表项跨页断开、表格行被拦腰截断、章标题被挤到页面底部。

通过逐行解析 Markdown 并应用 8 级排版层级 + 多层分页控制，输出可直接交付的 Word 文档。

## 适用场景

- 用户说"把这篇 Markdown 排成 Word"、"帮我生成一个好看的 docx"、"排版太丑了重新弄"。
- 文档包含 `#`/`##`/`###` 标题、`-` 列表、`1.` 有序列表、`| 表格 |`、提示块 `> [提示]` 等。
- 文档需要避免 AI 生成文档常见的"AI 味"（过度粗体、模板化配色、断裂分页）。

## 使用方法

1. 确认源文件是 `.md` 格式。
2. 调用脚本：

```bash
python scripts/md_to_docx.py "input.md" -o "output.docx"
```

3. 生成后用 DOCX 阅读器/WorkBuddy 预览检查，重点看：
   - 大标题是否清晰（主副两行，不 awkward 换行）。
   - **章标题是否在新页面顶部**（不是被挤到上一页底部）。
   - 章/节标题是否与正文在同一页。
   - 列表项、提示段落、表格行是否被分页断开。

## 排版层级

| 元素 | 字号 | 粗细 | 颜色 | 特殊处理 |
|---|---|---|---|---|
| 文档主标题 | 22pt | 粗体 | #111111 | 居中，与副标题同页 |
| 文档副标题 | 14pt | 常规 | #666666 | 居中，与主标题同页 |
| 章标题 `##` | 16pt | 粗体 | #111111 | **强制新页开始**，与下段同页 |
| 节标题 `###` | 14pt | 粗体 | #111111 | 与下段同页 |
| 方法标题 `**方法X**` | 12pt | 粗体 | #111111 | 与下段同页 |
| 子标题 `**XXX**` | 11pt | 粗体 | #111111 | 与下段同页 |
| 正文 | 10.5pt | 常规 | #333333 | 段中不分页；标题后首段与标题同页 |
| 无序/有序列表 | 10.5pt | 常规 | #333333 | 段中不分页；连续项同页 |
| 表格 | 10pt | 表头粗体 | #333333 | 表头灰底、单元格边框、行不跨页 |
| 提示块 `> [提示]` | 9.5pt | 标签粗体 | #666666 | 左侧竖线、整体不分页 |

## 分页控制（核心逻辑）

分页控制是本 skill 的核心难点。脚本使用以下 4 种机制协同工作：

### 1. `page_break_before` — 章标题强制新页

**场景**：章标题（`##`）被挤到上一页底部，标题和正文分离。

**方案**：给所有 `##` 章标题段落设置 `paragraph_format.page_break_before = True`，强制每个章节从新页面开始。

```python
p.paragraph_format.page_break_before = True
```

**踩坑**：只设 `keep_with_next` 不够——Word 可能会把标题连同下一段一起推到页面底部，视觉上标题仍然"挂"在上一页末尾。`page_break_before` 才能彻底解决。

### 2. `prev_was_heading` 状态追踪 — 标题与首段正文粘连

**场景**：标题设了 `keep_with_next`，但如果标题后第一段正文本身很长，Word 可能仍把它们分到不同页。

**方案**：用一个 `prev_was_heading` 布尔变量在逐行解析时追踪"上一段是否为标题"。当遇到正文段落时，如果 `prev_was_heading == True`，则给该正文段落也设 `keep_with_next = True`，确保标题+首段正文作为一个整体不被分页。

```python
# 初始化（while 循环前）
prev_was_heading = False

# 每种标题处理后
prev_was_heading = True

# 正文段落处理时
if prev_was_heading:
    set_keep_with_next(p, True)
    prev_was_heading = False
```

**关键**：所有非标题元素（正文、列表等）处理后都要把 `prev_was_heading` 重置为 `False`，避免状态泄漏。

### 3. 连续列表项 `keep_with_next` — 列表不被跨页拆散

**场景**：有序/无序列表跨页时，前几项在上一页、后几项在下一页。

**方案**：对每个列表项，检查下一行是否也是列表项。如果是，给当前项设 `keep_with_next = True`，让连续列表项作为一个整体保持同页。

```python
if i + 1 < len(lines) and re.match(r'^\d+\.\s', lines[i + 1].strip()):
    set_keep_with_next(p, True)
```

### 4. `keep_together` + `cantSplit` — 段落和表格行内部不断裂

- **`keep_together`**：每个段落（正文、列表项、提示行）内部不跨页断开。
- **`cantSplit`**（表格行 `trPr`）：表格行不跨页断开。

## 去除"AI 味"的排版原则

以下原则来自实际用户反馈，是多次迭代后的经验总结：

1. **全文统一黑体**：不用宋体/微软雅黑混排，正文和标题都用黑体，靠字号和粗细区分层级。
2. **不用蓝白配色**：避免"企业报告"模板感。用深灰系（#111111 标题、#333333 正文、#666666 提示）。
3. **去掉项目符号黑点**：无序列表用 `·` 代替默认的 `•`，视觉更轻。
4. **提示段落用小字+左侧竖线**：不用色块背景，用 `9.5pt` 小字 + `#999999` 左侧竖线，既醒目又不抢主内容。
5. **分隔符精简**：`---` 分隔符只画一条浅灰底线，不要多余的装饰。
6. **方法标题加粗但不加大**：`**方法X**` 用 `12pt` 粗体，比正文（10.5pt）稍大但不夸张。
7. **表格文字居中**：所有单元格内容水平居中对齐。
8. **行内粗体只在需要时用**：`**文本**` 解析为行内粗体，不滥用。

## 踩坑经验

### 坑 1：只设 `keep_with_next` 仍会出现标题在页底

**症状**：设置了 `keep_with_next = True`，但章标题仍然出现在页面底部，与正文一起被推到下一页。

**根因**：Word 的 `keep_with_next` 只保证"当前段与下一段同页"，但如果当前段（标题）本身就在页面底部区域，Word 会把两段一起推到下一页——结果标题虽然和正文在一起了，但视觉上标题在页面最底部，体验很差。

**修复**：对章标题额外设置 `page_break_before = True`，强制新页开始。`page_break_before` 是最彻底的方案。

### 坑 2：`prev_was_heading` 忘记初始化

**症状**：脚本运行时 `prev_was_heading` 变量未定义，报 `NameError`。

**根因**：在 `build_doc()` 的 while 循环前忘记初始化变量。

**修复**：在循环前添加 `prev_was_heading = False`。

### 坑 3：`prev_was_heading` 状态泄漏

**症状**：非标题段落也被设置了 `keep_with_next`，导致不相关的段落被强制同页。

**根因**：某些非标题元素（列表、提示块）处理后忘记重置 `prev_was_heading = False`。

**修复**：确保所有非标题元素处理分支末尾都重置 `prev_was_heading = False`。

### 坑 4：全文 BOLD 问题

**症状**：生成的 DOCX 中所有文字都变成粗体。

**根因**：在解析行内 `**粗体**` 标记时，如果上下文的 `bold` 参数传递有误，会导致普通文本也被设为粗体。

**修复**：确保 `parse_inline_text()` 中非粗体片段的 `bold` 参数正确传递为 `False`。从源 Markdown 重新生成可彻底解决。

### 坑 5：文件被占用无法覆盖

**症状**：`PermissionError: [Errno 13] Permission denied`。

**根因**：DOCX 文件被其他程序（如腾讯文档预览、Word）打开占用。

**修复**：每次生成使用新文件名（如 `_v2.docx`、`_v3.docx`），或先关闭占用程序。

### 坑 6：修改后只改了项目脚本，没同步到 skill 脚本

**症状**：项目脚本 `reformat_docx.py` 已修复但 skill 脚本 `md_to_docx.py` 仍是旧版，导致下次使用 skill 时问题复现。

**根因**：项目脚本和 skill 脚本维护了两份代码，修改时只改了项目脚本。

**修复**：每次修复项目脚本后，同步更新 `scripts/md_to_docx.py`。两份代码的分页控制逻辑应保持一致。

## 验证方法

生成 DOCX 后，可通过以下 Python 脚本快速验证分页属性是否正确设置：

```python
from docx import Document

doc = Document("output.docx")
chapter_count = 0
keep_next_count = 0
keep_together_count = 0

for p in doc.paragraphs:
    pf = p.paragraph_format
    if pf.page_break_before:
        chapter_count += 1
    if pf.keep_with_next:
        keep_next_count += 1
    if pf.keep_together:
        keep_together_count += 1

print(f"章标题(page_break_before): {chapter_count}")
print(f"keep_with_next: {keep_next_count}")
print(f"keep_together: {keep_together_count}")
```

## 依赖

- Python 3.8+
- `python-docx>=1.1.0`

## 自定义

如需调整字体、字号或颜色，直接编辑 `scripts/md_to_docx.py` 顶部的常量区（`FONT_*`、`COLOR_*`、`SZ_*`）。

## 文件结构

```
docx-typesetting-from-markdown/
├── SKILL.md              # 本文件——skill 说明 + 踩坑经验
└── scripts/
    └── md_to_docx.py     # Markdown 转 DOCX 核心脚本
```

## 维护须知

- 每次在实际项目中修复排版问题后，**必须同步更新本 skill 的 `scripts/md_to_docx.py`**。
- 如果发现了新的踩坑经验，追加到上方"踩坑经验"章节。
- 排版层级表和分页控制逻辑如有变更，同步更新对应章节。
