# code-to-images

> 将源代码文件转换为带行号 + 语法高亮的 A4 图片，并合并为 PDF。
> Convert source code files into A4 images with line numbers, syntax highlighting, then merge to PDF.

**v2.0.5** — Brace-depth indentation · Auto word-wrapping · Bilingual docs

---

📖 [中文](#chinese) · [English](#english)

---

## 中文说明 / Chinese

> 🇨🇳 中文 | [English](#english)

将源代码文件（`.c`、`.h`、`.py`、`.js` 等）转换为带**行号**和**语法高亮**的 A4 比例图片，自动合并为一个 PDF。

### 功能

- ✅ **行号** — 自适应装订线宽度（千行文件自动加宽）
- ✅ **语法高亮** — 关键字、寄存器、宏、数字、字符串、注释分别着色
- ✅ **6 种等宽字体** — Cascadia Code / Fira Code / JetBrains Mono / Consolas / Courier New / Source Code Pro
- ✅ **字号自动适配** — 根据最长代码行自动缩放，填满 A4 宽度
- ✅ **每页行数自适应** — 根据字号和行高自动计算
- ✅ **大括号深度缩进** — 按 `{}` 嵌套层级决定缩进，每级 = 4 字符宽度
- ✅ **标点自动换行** — 超宽代码在 `;,(){}[]` 后折行，续行不产生新行号
- ✅ **Tab 制表位** — 正确按制表位对齐
- ✅ **多行注释支持** — `/* */` 跨行注释完整灰显
- ✅ **固定 A4 比例** — 794×1123px (96 DPI)，每页尺寸统一
- ✅ **PDF 输出** — 每个源文件一份 PDF

### 安装依赖

```bash
npm install -g @resvg/resvg-js
pip install img2pdf
```

### 使用

1. 编辑 `gen_code_pdfs.py` 顶部 `FILES` 列表，填入源文件名
2. 按需修改配置（`FONT_KEY`、`FONT_SIZE` 等）
3. 运行：`python gen_code_pdfs.py`
4. 输出：`文件名.pdf` + `文件名_images/` 目录（SVG + PNG）

#### 批量打印多文件

```python
FILES = ['main.c', 'adc.c', 'dma.c', 'spi.c', 'main.h', 'adc.h', 'dma.h', 'spi.h']
```

#### 提高打印质量（300 DPI）

```python
A4_W, A4_H = 2480, 3508  # A4 at 300 DPI
```

#### 切换字体

```python
FONT_KEY = '***'  # cascadia / firacode / jetbrains / consolas / courier / sourcecode
```

### 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `FONT_KEY` | `cascadia` | 字体选择 |
| `FONT_SIZE` | `14` | 基础字号 (px)，自动缩小到 `MIN_FONT_SIZE` |
| `LINE_HEIGHT_RATIO` | `1.65` | 行高 = 字号 × 系数 |
| `TAB_WIDTH` | `4` | Tab 制表位宽度 |
| `MIN_FONT_SIZE` | `7` | 自动缩小时的最小字号 |
| `WRAP_IDENT` | `2` | 续行额外缩进字符数 |

### 自动适配逻辑

1. **宽度适配**：扫描所有代码行，找到最长行（正确处理 Tab），计算字号使其刚好占满 A4 内容宽度，上限 `FONT_SIZE`，下限 `MIN_FONT_SIZE`
2. **缩进计算**：`compute_indent_levels()` 按 `{}` 大括号嵌套深度逐行计算缩进级别，注释/字符串内的括号跳过
3. **每页行数**：A4 可用高度 ÷ (`字号 × LINE_HEIGHT_RATIO`)
4. **标点换行**：超宽行在 `;,(){}[]` 后折行，可用宽度扣除深度缩进，续行不产生新行号
5. **渲染**：行号在 codeClip 外渲染（始终可见），代码在 clip 内渲染，font-family 正确引用

### 输出结构

```
filename.c_images/
├── code_page_1.svg      ← 矢量 SVG（可编辑）
├── code_page_1.png      ← PNG 图片
├── code_page_2.svg
├── code_page_2.png
└── ...
filename.c.pdf           ← 最终 PDF
```

---

## English / English

> 🇬🇧 English | [中文](#chinese)

> Convert source code files into A4 images with line numbers and syntax highlighting, then merge to PDF.

### Features

- ✅ **Line numbers** — Adaptive gutter width (auto-widens for 1000+ line files)
- ✅ **Syntax highlighting** — Keywords, registers, macros, numbers, strings, comments
- ✅ **6 monospace fonts** — Cascadia Code / Fira Code / JetBrains Mono / Consolas / Courier New / Source Code Pro
- ✅ **Auto font size** — Scales to fill A4 width based on longest line
- ✅ **Auto lines per page** — Computed from font size and line height
- ✅ **Brace-depth indentation** — Indent level by `{}` nesting, each level = 4 char widths
- ✅ **Auto word-wrapping** — Breaks after `;,(){}[]`, continuation lines get no new line number
- ✅ **Tab stops** — Proper tab alignment
- ✅ **Multi-line comments** — Full `/* */` cross-line support, rendered in gray
- ✅ **Fixed A4 ratio** — 794×1123px (96 DPI), uniform page dimensions
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
4. Output: `filename.pdf` + `filename_images/` directory (SVG + PNG)

#### Batch processing

```python
FILES = ['main.c', 'adc.c', 'dma.c', 'spi.c', 'main.h', 'adc.h', 'dma.h', 'spi.h']
```

#### Print quality (300 DPI)

```python
A4_W, A4_H = 2480, 3508  # A4 at 300 DPI
```

#### Change font

```python
FONT_KEY = '***'  # cascadia / firacode / jetbrains / consolas / courier / sourcecode
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `FONT_KEY` | `cascadia` | Font selection |
| `FONT_SIZE` | `14` | Base font size (px), auto-reduces to `MIN_FONT_SIZE` |
| `LINE_HEIGHT_RATIO` | `1.65` | Line height = font_size × ratio |
| `TAB_WIDTH` | `4` | Tab stop width (in spaces) |
| `MIN_FONT_SIZE` | `7` | Minimum font size when auto-reducing |
| `WRAP_IDENT` | `2` | Extra indent chars for continuation lines |

### Auto-fit Logic

1. **Width fit**: scan all lines, find the longest, calculate font size to fill A4 content width (capped at `FONT_SIZE`, floored at `MIN_FONT_SIZE`)
2. **Indent calculation**: `compute_indent_levels()` tracks braces per line (skipping comments/strings), each level renders at `TAB_WIDTH × cw` pixels
3. **Lines per page**: A4 available height ÷ (`font_size × LINE_HEIGHT_RATIO`)
4. **Word-wrapping**: lines exceeding available width break after `;,(){}[]`, continuation lines show no extra line number
5. **Rendering**: line numbers outside codeClip (always visible), code content inside clip, font-family properly quoted

### Output Structure

```
filename.c_images/
├── code_page_1.svg      ← Vector SVG (editable)
├── code_page_1.png      ← PNG image
├── code_page_2.svg
├── code_page_2.png
└── ...
filename.c.pdf           ← Final PDF
```

---

## License

MIT
