---
name: "code-to-images"
description: "Convert code files to A4-ratio PNG/SVG images with line numbers and syntax highlighting, then merge to PDF. 支持中英文双语说明。"
---

# Code → A4 图片 + PDF / A4 Images + PDF

**v2.0.5** — Brace-depth indentation · Auto word-wrapping

---

📖 [中文](#chinese) · [English](#english)

---

## 中文说明 / Chinese

> 🇨🇳 中文 | [中文](#chinese)

将源代码文件转换为多页 A4 比例图片（SVG+PNG），然后合并为一个 PDF。

### 功能

- ✅ **行号** — 自适应装订线宽度
- ✅ **语法高亮** — 关键字、寄存器、宏、数字、字符串、注释分别着色
- ✅ **6 种等宽字体** — Cascadia Code / Fira Code / JetBrains Mono / Consolas / Courier New / Source Code Pro
- ✅ **字号自动适配** — 根据最长行自动缩放，填满 A4 宽度
- ✅ **每页行数自适应** — 根据字号和行高自动计算
- ✅ **大括号深度缩进** — 按 `{}` 嵌套层级决定缩进，每级 4 字符宽度
- ✅ **代码超宽自动换行** — 在 `;,(){}[]` 标点后折行，续行不产生新行号
- ✅ **Tab 制表位** — 正确按制表位对齐
- ✅ **多行注释识别** — `/* */` 跨界注释完整处理
- ✅ **固定 A4 比例** — 794×1123px (96 DPI)
- ✅ **PDF 输出** — 每个源文件一份 PDF

### 依赖

```bash
npm install -g @resvg/resvg-js
pip install img2pdf
```

### 使用

1. 编辑 `gen_code_pdfs.py` 顶部的 `FILES` 列表，填入源文件名
2. 按需修改 `FONT_KEY`、`FONT_SIZE` 等配置
3. 运行：`python gen_code_pdfs.py`
4. 输出：`文件名.pdf` + `文件名_images/` 目录（中间 SVG/PNG）

### 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FONT_KEY` | `cascadia` | 字体：`cascadia`/`firacode`/`jetbrains`/`consolas`/`courier`/`sourcecode` |
| `FONT_SIZE` | `14` | 基础字号 (px)，超宽代码自动缩小 |
| `LINE_HEIGHT_RATIO` | `1.65` | 行高系数 |
| `TAB_WIDTH` | `4` | Tab 制表位宽度 |
| `MIN_FONT_SIZE` | `7` | 自动缩小时的最小字号 |
| `WRAP_IDENT` | `2` | 续行额外缩进字符数 |

---

## English / English

> 🇬🇧 English | [中文](#chinese)

Convert source code files into multi-page A4-ratio images (SVG+PNG), then merge into a single PDF.

### Features

- ✅ **Line numbers** — Adaptive gutter width
- ✅ **Syntax highlighting** — Keywords, registers, macros, numbers, strings, comments
- ✅ **6 monospace fonts** — Cascadia Code / Fira Code / JetBrains Mono / Consolas / Courier New / Source Code Pro
- ✅ **Auto font size** — Scales to fill A4 width based on longest line
- ✅ **Auto lines per page** — Computed from font size and line height
- ✅ **Brace-depth indentation** — Indent level by `{}` nesting, each level = 4 char widths
- ✅ **Auto word-wrapping** — Breaks after `;,(){}[]`, continuation lines get no new line number
- ✅ **Tab stops** — Proper tab alignment
- ✅ **Multi-line comments** — Full `/* */` cross-line support
- ✅ **Fixed A4 ratio** — 794×1123px (96 DPI)
- ✅ **PDF output** — One PDF per source file

### Prerequisites

```bash
npm install -g @resvg/resvg-js
pip install img2pdf
```

### Usage

1. Edit the `FILES` list at the top of `gen_code_pdfs.py`
2. Configure `FONT_KEY`, `FONT_SIZE`, etc.
3. Run: `python gen_code_pdfs.py`
4. Output: `filename.pdf` + `filename_images/` directory (intermediate SVG/PNG)

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `FONT_KEY` | `cascadia` | Font: `cascadia`/`firacode`/`jetbrains`/`consolas`/`courier`/`sourcecode` |
| `FONT_SIZE` | `14` | Base font size (px), auto-reduces for wide code |
| `LINE_HEIGHT_RATIO` | `1.65` | Line height multiplier |
| `TAB_WIDTH` | `4` | Tab stop width |
| `MIN_FONT_SIZE` | `7` | Minimum font size when auto-reducing |
| `WRAP_IDENT` | `2` | Extra indent for continuation lines |

---

## Python Batch Script

Save as `gen_code_pdfs.py` and run with `python gen_code_pdfs.py`:

```python
#!/usr/bin/env python3
"""Batch convert code files -> A4 images + PDF. One PDF per source file."""
import os, sys, subprocess, json

# ===== CONFIG =====
FILES = [/* List source files here */]
FONT_KEY = '***'   # cascadia | firacode | jetbrains | consolas | courier | sourcecode
FONT_SIZE = 14; LINE_HEIGHT_RATIO = 1.65; TAB_WIDTH = 4; MIN_FONT_SIZE = 7; WRAP_IDENT = 2

FONT_NAMES = {'cascadia':'Cascadia Code','firacode':'Fira Code','jetbrains':'JetBrains Mono',
    'consolas':'Consolas','courier':'Courier New','sourcecode':'Source Code Pro'}
A4_W, A4_H = 794, 1123; HDR_H = 60; PAD_R = 36; PAD_T = 72; PAD_B = 28
CONTENT_H = A4_H - PAD_T - PAD_B; CHAR_RATIO = 0.60; WRAP_PUNCT = set(';,(){}[]')
KW = {'void','char','int','u8','u16','u32','uchar','unsigned','for','if','else','while',
      'switch','case','break','return','static','bit','sbit','xdata','idata','code','interrupt',
      'do','default','continue','struct','typedef','enum','const','#ifndef','#define','#endif','#ifdef','extern'}
RG = {'P0','P1','P2','P3','P4','P5','P6','P7','RST','SCLK','IO','SCK'}
CO = {'keyword':'#d63384','register':'#e8590c','macro':'#099268',
      'number':'#2b8a3e','string':'#099268','comment':'#868e96','var':'#1971c2','text':'#212529'}
BG='#ffffff'; HDR_BG='#f1f3f5'; HDR_BD='#dee2e6'; GT_BG='#f8f9fa'; GT_BD='#e9ecef'; LN_COLOR='#868e96'

# [Full script at: https://github.com/yon-gjun/code-to-images/blob/master/gen_code_pdfs.py]
# Run the script directly from the repo for the complete, tested version.
```
