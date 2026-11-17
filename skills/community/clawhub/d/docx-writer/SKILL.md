---
name: docx-writer
description: 标准学术文档生成 — 通过 bayoo-docx（原生脚注支持）和模板 template.docx 生成符合学术排印规范的 Word 文档，含脚注、三线表、图片、LaTeX 公式（可输出 Word 原生可编辑公式 OMML 或 XeLaTeX 渲染图）等。当用户要生成/排版 Word（.docx）文档、学位论文、实验报告、新闻稿、推送稿、讲稿，或需要在 docx 里插入数学公式/LaTeX 公式/原生可编辑公式时使用
license: MIT
compatibility: opencode
metadata:
  audience: academic
  workflow: docx
---

# Skill: docx-writer — 标准学术文档生成

## 概述

通过 **bayoo-docx**（原生支持脚注的 python-docx 分支）+ **lxml** 生成符合学术规范的 Word 文档。脚注由库引擎原生创建，避免手工构造 OOXML 导致的格式问题。

## 前置条件

```powershell
pip install bayoo-docx lxml pyyaml pymupdf pillow
```

- **LaTeX 公式**（可选能力）：`omml` 模式需 **`pandoc`**；`image` 模式需 **`xelatex`**（TeX 发行版，如 MiKTeX/TeX Live）——见「LaTeX 公式」节。
- 视觉核验排版另需 LibreOffice（`soffice`）。

## 架构总览（配置驱动 / 内容与排版解耦）

```
docx-writer/
├── template.docx              # 默认基底（承载原生脚注样式），被 academic 模板引用
├── templates/                 # ★ 模板 = 一份 YAML 配置（页面 + 样式表 + 脚注 + 后处理）
│   ├── academic.yaml          #   标准学术/论文体例（含脚注）
│   ├── push.yaml              #   微信公众号推送稿体例
│   ├── news.yaml              #   清华新闻网简讯体例
│   └── script.yaml            #   演讲稿/答辩稿体例（大字号）
└── scripts/
    ├── docx_engine.py         # ★ 引擎：Template(读配置) + Builder(渲染)，不含任何内容
    ├── latex_formula.py       # ★ LaTeX → 紧裁 PNG（XeLaTeX+PyMuPDF；引擎与 CLI 共用）
    ├── build_from_content.py  # ★ 声明式渲染器：content.yaml/json → docx（CLI）
    └── build_docx.py          # 内容脚本示例（Python API 写法）
```

**三条解耦边界**：
1. **排版 ↔ 内容**：字体/字号/对齐/缩进/行距/颜色/页边距/背景/脚注全在模板 YAML 里；内容脚本只写文字与图片。
2. **模板 ↔ 引擎**：换体例只改 `Template.load('<name>')`，引擎代码不动。
3. **调用方式**：既可 Python API（`Builder`），也可声明式内容文件（`build_from_content.py`）。

## 模板配置结构（templates/\*.yaml）

| 段 | 字段 | 说明 |
|----|------|------|
| `name` | | 模板名 |
| `base_docx` | | 基底 docx 路径（承载脚注样式）；`null` = 空白文档 |
| `page` | `size` | A4 / LETTER / A3 / A5 |
| | `margin` | `{top,bottom,left,right}`，支持 cm/mm/pt/in |
| | `background` | `{color: "F7F7F7"}`（Word 页面底色） |
| | `orientation` | `portrait` / `landscape` |
| `styles` | 任意样式名 | 样式表，见下 |
| `footnote` | `enabled/cn/en/size/numbering/num_fmt` | 脚注字体、字号、编号（`per_page` 每页重编 / `continuous` 连续） |
| `features` | `fix_quotes` | 中文引号拆 run 校正字体（默认 true） |
| | `superscript_footnotes` | 正文脚注编号上标（默认 true） |

**样式字段**（`styles.<名字>`）：`cn`(中文字体) `en`(西文字体) `size` `bold` `italic` `color`(十六进制) `align`(left/center/right/justify) `indent`(首行缩进) `line_spacing`(数字=倍数 / `18pt`=固定) `space_before` `space_after`。
`image` 样式额外支持 `width`；`table` 样式支持 `mode`(three_line/grid) `word_style` `header` `cell`。

**加一套新模板**：复制任一 yaml → 改名 → 调字段即可，引擎与内容脚本无需改动。

## 引擎 API（scripts/docx_engine.py）

```python
from docx_engine import Template, Builder
b = Builder(Template.load('academic'))     # 或 yaml 绝对路径
b.title('标题')                            # = para(style='title')
b.heading('一、引言', level=1)              # level→h1/h2/h3
b.para('正文{F1}', style='body', fn_map={'F1': '注释文本'})   # {Fn} 占位转脚注
b.image('fig.jpg', caption='图1  示意', width='14cm')
b.formula(r'\alpha_0=\arctan(p_x/p_y)', caption='式(1)')          # 行间公式（默认 auto）
b.formula(r'E=mc^2', mode='omml')                                 # 强制 Word 原生可编辑公式
b.para('由 {X1} 可得', lx_map={'X1': r'P_e=P_1+P_2'})             # {Xn} 占位 → 行内公式
b.table(['列1','列2'], [['a','b']], caption='表1  示例')
b.para('文案丨xx', style='signature')
b.save('out.docx')
```

## 声明式渲染（scripts/build_from_content.py）

```powershell
python scripts/build_from_content.py --content content.yaml --out out.docx
python scripts/build_from_content.py --content content.json --template push --out out.docx
```

`content.yaml` 的 `blocks:` 支持：`title / heading{level} / para{style,fn,lx} / formula{latex,caption} / caption / note / image{path,caption,width} / table{headers,rows} / signature{lines} / blank / pagebreak`。输出 stdout 为 JSON。

---

## LaTeX 公式（scripts/latex_formula.py）

公式有**两种呈现**，由模板 `formula` 样式的 `mode`（或调用级 `mode=`）决定：

| mode | 产物 | Word 里可编辑 | 依赖 |
|------|------|:---:|------|
| `omml` | **Word 原生公式（OMML）** | ✅ | `pandoc` |
| `image` | XeLaTeX 紧裁 PNG | ❌（图片） | `xelatex` + PyMuPDF |
| `auto`（默认） | 有 `pandoc` 用 `omml`，否则 `image` | 视环境 | 视环境 |

- **`omml`（推荐，需编辑时用）**：LaTeX →（pandoc `-f markdown -t docx`）→ 抽取 `m:oMath`/`m:oMathPara` → 写入段落，Word 中可点选编辑。
- **`image`**：遵循 AGENTS.md「数学公式渲染（转图片）」——XeLaTeX `preview`+`tightpage` 紧裁 → PyMuPDF 转 PNG → 作为图片插入（任何环境可渲染，但不可编辑）。
- **行间公式**：`b.formula(latex, caption=None, mode=None)`。
- **行内公式**：段文本写 `{X1}` 占位 + `lx_map={'X1': r'...'}`（`b.para(..., lx_map=...)`，或 `build_docx.py` 的 `Lx(text, lx_map)`）。图片模式下可用模板 `formula` 样式的 `inline_scale`（默认 1.0）与 `inline_border`（默认 `1pt`）微调行距。
- **依赖**：`omml` 需 **`pandoc`**（定位顺序 `--pandoc` > `OPENCODE_PANDOC` > `PATH`）；`image` 需 **`xelatex`**（`--xelatex` > `OPENCODE_XELATEX` > `PATH`）+ **PyMuPDF**。缺失时给出明确报错。
- ⚠️ **字数**：Word 会把 **OMML 公式内容计入「字数」**（行间大公式尤甚）；**有字数上限的稿子**建议用 `mode: image`（公式为图片，**不计入字数**），或精简公式、把变量与单位集中说明。核对一律以 Word 状态栏为准。

```powershell
# 图片模式（也可被引擎 import：from latex_formula import render_formulas）
python scripts/latex_formula.py --latex "E=mc^2" "\int_0^1 x^2\,dx=\frac{1}{3}" --outdir .\formula_png
python scripts/latex_formula.py --input formulas.txt --outdir .\formula_png --dpi 300
# Word 原生公式（OMML）
python scripts/latex_formula.py --latex "E=mc^2" --omml
```

> 图片缓存在 `--outdir`（引擎默认 `<cwd>/_docx_formula_cache`），按「公式+样式+dpi+border」哈希命名，重复渲染自动复用。

---

## 文件管理

| 类型 | 路径 | 生命周期 |
|------|------|----------|
| SKILL 本体 | `skills/docx-writer/SKILL.md` | 长期 |
| 标准基底 | `skills/docx-writer/template.docx` | **不修改** |
| 模板配置 | `skills/docx-writer/templates/*.yaml` | 长期（可新增） |
| 持久脚本 | `skills/docx-writer/scripts/` | 长期 |
| 临时脚本 | 项目文件夹（历史遗留 `skills/docx-writer/tmp/` 保留不删） | 记录到 log.md |
| 输出 | 当前工作目录或 `--out` 指定处（历史遗留 `skills/docx-writer/output/` 保留待迁移） | 不写 skill 目录 |

## 引擎选择决策

| 需求 | 推荐 | 理由 |
|------|------|------|
| 创建含脚注的 docx | **bayoo-docx** | `paragraph.add_footnote()` 原生创建，编号/间距正确 |
| 格式化（字体/字号/缩进） | bayoo-docx + lxml | 字体用 `run.font` API，边框/样式用 lxml 微调 |
| 加载模板样式 | bayoo-docx | `Document(模板路径)` 继承模板的样式和页设置 |
| 脚注字体/字号设定 | 创建后遍历 `fn.findall('.//w:r')` | 显式设置 `w:sz=18` 和 `w:rFonts` |

**不要用的**：
- win32com（需要安装 Word，本环境没有）
- python-docx 原始版（无 `add_footnote`）
- 手工构造 `footnotes.xml`（编号/分隔线不可控）

---

## 生成流程

### 步骤 1：准备模板

SKILL 自带模板 `skills/docx-writer/template.docx`（已验证的初稿文件，含 Word 原生脚注）。该模板提供正确的 `footnote text`（样式ID=12）和 `footnote reference`（样式ID=20）样式。

脚本中引用方式：`TEMPLATE = os.path.join(SKILL_DIR, 'template.docx')`

### 步骤 2：编写内容

使用 `B('文本{F1}更多文本')` 语法，其中 `{F1}` 表示脚注。

**脚注编号规则**：
- 句号在前，脚注在后：`句子内容。{F1}` ✅
- 不可：`句子内容{F1}。` ❌

### 步骤 3：注册脚注文本

```python
FN_TEXT_MAP = {
    'F1': '作者. 标题. 期刊, 年份, 卷(期): 页码.',
}
```

### 步骤 4：排版函数

| 函数 | 用途 | 字体/字号 |
|------|------|-----------|
| `P(text, ...)` | 通用段落 | 宋体/Times New Roman 10.5pt |
| `B(text)` | 正文 | 宋体/Times New Roman 10.5pt |
| `Bs(text)` | 小字正文（摘要） | 宋体/Times New Roman 9pt |
| `H1(text)` | 一级标题 | 黑体/Arial 12pt |
| `H2(text)` | 二级标题 | 黑体/Arial 12pt |
| `H3(text)` | 三级标题 | 黑体/Arial 10.5pt |
| `Tc(text)` | 表题/图题 | 宋体/Times New Roman 9pt |
| `add_img(path, cap)` | 插入图片+图题 | 居中 |
| `Fx(latex, cap=None)` | 插入行间公式（XeLaTeX 渲染） | 居中，按公式宽度等比 |
| `Lx(text, lx_map)` | 含行内公式占位 `{X1}` 的正文段落 | 同正文 |
| `add_tbl(h, rows)` | 三线表格 | 小五号 |

### 步骤 5：保存

```python
doc.save('输出路径.docx')
```

---

## 脚本

**不要自己写引擎。** 排版逻辑固定在 `scripts/docx_engine.py`，体例固定在 `templates/*.yaml`，你只写内容。

| 文件 | 说明 | 路径 |
|------|------|------|
| `docx_engine.py` | 引擎（Template + Builder），**不修改、无 CLI** | `skills/docx-writer/scripts/docx_engine.py` |
| `build_from_content.py` | 声明式渲染器（content.yaml/json → docx，CLI） | `skills/docx-writer/scripts/build_from_content.py` |
| `build_docx.py` | 内容脚本模板（Python API 逐句写，CLI 可覆盖） | `skills/docx-writer/scripts/build_docx.py` |
| `latex_formula.py` | LaTeX → Word 原生公式（OMML，可编辑）或紧裁 PNG（pandoc / XeLaTeX+PyMuPDF，CLI + 可 import） | `skills/docx-writer/scripts/latex_formula.py` |
| `templates/*.yaml` | 模板配置（academic / push / news / script） | `skills/docx-writer/templates/` |

### scripts/latex_formula.py
用途：LaTeX 公式 → **Word 原生公式（OMML，可编辑）** 或 **紧裁 PNG**（XeLaTeX+PyMuPDF）。输出 stdout JSON。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--latex TEX [TEX ...]` | **输入**：一个或多个 LaTeX 公式字符串 | 二选一 |
| `--input FILE` | **输入**：公式文件（`.txt` 每行一条 / `.json` 字符串数组） | 二选一 |
| `--outdir DIR` | **输出** PNG 目录（默认 `./formula_png`，自动创建） | 否（仅图片模式） |
| `--dpi N` | 渲染 DPI（默认 300） | 否 |
| `--inline` | 行内公式（textstyle）；默认行间（displaystyle） | 否 |
| `--omml` | **改为输出 OMML XML**（Word 原生可编辑公式，需 pandoc） | 否 |
| `--xelatex PATH` | xelatex 路径（默认 `OPENCODE_XELATEX` 或 PATH） | 否 |
| `--pandoc PATH` | pandoc 路径（`--omml` 时用，默认 `OPENCODE_PANDOC` 或 PATH） | 否 |
| `--timeout N` | 单次编译超时秒（默认 180） | 否 |

示例：`python scripts/latex_formula.py --latex "E=mc^2" --outdir ./png`
输出：`{"status":"ok","count":N,"outdir":...,"items":[{"latex","png","width_px","height_px","width_pt","height_pt"}...]}`

### scripts/build_from_content.py
用途：声明式内容文件（YAML/JSON）→ docx。输出 stdout JSON。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--content FILE` | **输入**内容文件（YAML/JSON），内含 `template:` + `blocks:` | ✅ |
| `--out FILE` | **输出** docx 路径（默认：`当前工作目录/<content 名>.docx`） | 否 |
| `--template NAME` | 覆盖内容文件里的 `template`（academic/push/news 或 yaml 路径） | 否 |
| `--image-base DIR` | 图片相对路径基准目录（覆盖内容里的 `image_base`） | 否 |

示例：
```powershell
python scripts/build_from_content.py --content content.yaml --out out.docx
python scripts/build_from_content.py --content content.json --template push --out out.docx
python scripts/build_from_content.py --content content.yaml          # 输出到 当前目录/content.docx
```
输出：`{"status":"ok","out":abs_path,"template":"...","blocks":N}`（失败 `{"status":"error",...}` + exit 1）。

### scripts/build_docx.py
用途：内容脚本**模板**——复制到工作目录后改内容，用 `B/H1/H2/H3/Tc/add_img/add_tbl` 逐句写。所有参数可选，**不带参数时行为与原来完全一致**（输出 `输出路径.docx` 到当前工作目录）。

| 参数 | 说明 | 必填 |
|------|------|------|
| `--template NAME` | 模板名或 yaml/json 路径（默认 `academic`） | 否 |
| `--out FILE` | **输出** docx（默认 `输出路径.docx`，写当前工作目录） | 否 |
| `--fig-dir DIR` | 图片基准目录（默认 `图片目录`） | 否 |
| `--fn-map REF` | 脚注映射：JSON 文件路径或内联 JSON（默认文件内 `FN_TEXT_MAP`） | 否 |

示例：
```powershell
python scripts/build_docx.py                                   # 原样行为
python scripts/build_docx.py --template push --out 推送稿.docx
python scripts/build_docx.py --fig-dir .\imgs --fn-map fn.json
```
输出：进度 `Saved: <path>` 写 stderr；文档写 `--out`。

### scripts/docx_engine.py
用途：引擎库（`Template` / `Builder`），供 Python API 调用与上面两个脚本 import，**无 CLI、不修改**。用法见「引擎 API」节。

**写法 A（声明式，推荐）**：写一个 `content.yaml`（`template:` 指定体例 + `blocks:` 列表），跑 `build_from_content.py`。
**写法 B（API，复杂逻辑时）**：复制 `build_docx.py` → 改 `TEMPLATE_NAME`/`OUTPUT`/`FIG_DIR`/`FN_TEXT_MAP`（或走 CLI 参数）→ 在 `build_content()` 里用 `B/H1/H2/H3/Tc/add_img/add_tbl` 写 → 运行。

**不要修改** `scripts/docx_engine.py` 与 `templates/*.yaml` 的既有字段语义；要换体例，新增/复制模板 yaml 即可。输出/临时文件写**当前工作目录**或 `--out` 指定处，不写进 skill 目录。

---

## 排版规范（终稿样例标准）

### 页面设置
- 纸张：A4
- 页边距：上下 2.54cm，左右 3.18cm

### 字体字号行距总表

| 元素 | 中文 | 英文/数字 | 字号 | 对齐 | 缩进 | 行距 |
|------|------|----------|------|------|------|------|
| **文章标题** | 黑体 | Arial | 四号(14pt) | **居中** | 无 | 1.5倍 |
| **作者行** | 楷体 | Times New Roman | 五号(10.5pt) | **居中** | 无 | 1.5倍 |
| **摘要/关键词** | 宋体 | Times New Roman | **小五**(9pt) | 左对齐 | 首行缩进2字符 | 1.5倍 |
| **一级标题** | 黑体 | Arial | **小四**(12pt) | **居中** | **无** | 1.5倍 |
| **二级标题** | 黑体 | Arial | 小四(12pt) | 左对齐 | 首行缩进2字符 | 1.5倍 |
| **三级标题** | 黑体 | Arial | 五号(10.5pt) | 左对齐 | 首行缩进2字符 | 1.5倍 |
| **正文** | **宋体** | **Times New Roman** | **五号(10.5pt)** | 左对齐 | 首行缩进2字符 | **1.5倍** |
| **表题/图题** | 宋体 | Times New Roman | **小五(9pt)** | **居中** | **无** | 1.5倍 |
| **表内文字** | 宋体 | Times New Roman | 小五(9pt) | 居中 | — | 1.5倍 |
| **表注** | 宋体 | Times New Roman | 小五(9pt) | 左对齐 | 首行缩进2字符 | 1.5倍 |
| **脚注正文** | **宋体** | **Times New Roman** | **小五(9pt)** | 左对齐 | 无缩进 | **单倍行距** |
| **脚注编号（正文中）** | — | — | — | — | — | **上标** |

### 标题编号体系
- 一级标题：一、 二、 三、 四、
- 二级标题：（一）（二）（三）（四）
- 三级标题：1. 2. 3. 4.
- 四级标题：（1）（2）（3）（4）

### 脚注规范
1. **字体字号**：宋体/Times New Roman，**小五号(9pt)**，单倍行距
2. **上标**：正文中的脚注编号必须为上标（右上角）
3. **句号位置**：`句子内容。{F1}` — 句号在脚注标记**之前**，符点在前，注释号在后
4. **编号方式**：每页单独编号（Word 自动编号）
5. **分隔线**：仅在有脚注的页面显示，无需手动控制

### 表格规范
- 风格：**三线表**（仅上框线、下框线、表头下分割线，无内部竖线/横线）
- 表头：加粗
- 表内：居中对齐，小五号(9pt)
- 表题：在表格**上方**，居中，小五号(9pt)

### 图片规范
- 居中，无首行缩进
- 图题在图片**下方**，格式同表题
- ⚠️ **黑框陷阱**：用 python-docx `add_picture()` 直接生成的 `<wp:inline>` **缺少 `distT/distB/distL/distR` 与 `wp:effectExtent` 属性**，Word 会对这类不完整的 inline 图渲染出**黑色方框/边框**（LibreOffice 转 PDF 不显示，仅 Word 可见，极易漏检）。规避方法：
  1. **首选**：在用户原有 Word 文件上原位重构排版（抽离图片 run 到独立居中段落 + 图题，`p.addnext()` 插入），保留 Word 原生生成的 drawing XML（含 `distT/distB/distL/distR` 与 `wp:effectExtent`），不做 `add_picture` 重建
  2. 若必须用 python-docx 生成图片：在 `<wp:inline>` 上补 `distT="0" distB="0" distL="0" distR="0"`，并在 `<wp:extent>` 后补 `<wp:effectExtent l="0" t="0" r="0" b="0"/>`
  3. **全尺寸原图 + 零压缩（从 Word 原文件抽取）**：python-docx `add_picture` 无法解析相机照片的 EXIF（抛 `UnexpectedEndOfFileError`/`UnrecognizedImageError`，剥 EXIF 后常因缺 JFIF 仍失败）。做法：`docx.Document(用户原文件)` 提取其 `w:drawing` 元素 **deepcopy**（保留 Word 原生结构，天然含 `distT/effectExtent`），用 `Part(PackURI('/word/media/xxx.jpeg'), 'image/jpeg', 原始字节, package)` + `doc.part.relate_to(part, RT.IMAGE)` 得到 rId，改 `a:blip` 的 `r:embed` 后插入目标 run；图片显示尺寸沿用原 drawing 的 `wp:extent`。`deepcopy` 提取时须用 python-docx 解析过的元素（自带命名空间），不可直接 `etree.fromstring` 抽取片段（会 unbound prefix）
- ⚠️ **图片段慎用 `keep_with_next`**：`p.paragraph_format.keep_with_next = True` 虽能防止"图片在页尾、图题流到下一页"的孤行图题，但 Word 在"显示格式标记"时会在该段左侧渲染一个**小黑方块**（keep-with-next 的格式标记），用户会误以为是黑框/黑块。若不能接受，宁可不设 keep_with_next（代价是图片与图题可能分页）
- 新闻稿落款"供稿：XX"通常**右对齐**：`p.alignment = WD_ALIGN_PARAGRAPH.RIGHT`（枚举值 2），不用首行缩进

### 引用规范
- 全部使用**脚注**（注释体例），不设文末参考文献
- 顺序编号，格式遵循《清华大学学报（哲学社会科学版）》注释规范

### 引号规范
- 引号内含有**中文**（含中文标点，如逗号、句号、顿号等）：用**中文引号** `""`（U+201C/U+201D）；引号内再套引号时，内层用**中文单引号** `''`（U+2018/U+2019）
- 引号内为**纯英文/数字**（无任何 CJK 字符）：用**直引号** `""`（U+0022），字体随上下文（英文用 Times New Roman，中文用宋体）
- 同一段落中若出现多组引号，每组独立判断
- **字体铁律**：中文引号字符的 `eastAsia/ascii/hAnsi` 三个字体字段**必须设为所在段的中文字体**（正文宋体、标题黑体、副题楷体等），**禁止让中文引号使用 Times New Roman/Arial 等西文字体**——否则 Word 会把引号渲染成西文直引号样式（字形立、无中文引号弧度），属于排版不合格
- 实现方式（**所有 docx 生成的最后一步必须调用 `fix_quotes(parent)`**，同时处理双引号与嵌套单引号）：
  1. 生成阶段在正文文本中使用 ASCII 直引号 `"`（U+0022）；嵌套引号用 ASCII 单引号 `'`（U+0027）
  2. 输出前用 `fix_quotes(parent)` 遍历段落/表格，对每组引号内容做纯 ASCII 检测
  3. 含中文 → **将引号字符拆为独立 run**（从原 run 中切出），设该 run 的 `eastAsia/ascii/hAnsi` 均为所在段的中文字体（默认宋体）。原 run 的字体不受影响，英文保持 Times New Roman
  4. 纯英文 → 保留直引号，不额外拆分，与相邻文本 run 共用字体
  5. 嵌套单引号同样按 3/4 规则处理：内层中文内容拆 run、设中文字体；内层纯英文保留直引号
- ⚠️ **关键陷阱**：不能直接在原 run 上修改 `ascii`/`hAnsi` 为宋体，否则会覆盖 run 中英文单词的字体。必须拆分 run，只修改引号字符所在 run 的字体。引擎 `docx_engine.py` 已内置 `fix_quotes()`（双引号+嵌套单引号、字体跟随所在段中文字体）为标准后处理
- ⚠️ **字符串级转换不算完成**：在 Python 文本层把 ASCII 引号替换成中文弯引号（`replace`/正则/拼接）只解决了"字符对不对"，**没有解决"字体"**——中文引号仍会以 Times New Roman 渲染。字体问题必须在 OOXML run 层处理（拆分 run + 设 `rFonts`）。验证方法：生成后用脚本遍历 `w:r`，检查含引号字符的 run 其 `w:rFonts` 的 `ascii/hAnsi` 不得为 `Times New Roman`

### 常用代码对照

```python
def B(t):   return P(t)                              # 正文
def Bs(t):  return P(t, sz=Pt(9))                    # 小字
def H1(t):  return P(t, cn='黑体', en='Arial',       # 一级标题
                     sz=Pt(12), align='center', fi=None)
def H2(t):  return P(t, cn='黑体', en='Arial',       # 二级标题
                     sz=Pt(12))
def H3(t):  return P(t, cn='黑体', en='Arial',       # 三级标题
                     sz=Pt(10.5))
def Tc(t):  return P(t, sz=Pt(9), align='center',    # 表题/图题
                     fi=None)
```

### 脚本调用约定
- `B('文本{F1}')` — 正文带脚注，句号在脚注前
- `H1('一、标题')` — 一级标题
- `add_tbl(['列名'], [['数据']])` — 三线表
- `add_img('路径.png', '图1  标题')` — 图片+图题

## 编码规范

- **禁止使用全角空格**（`\u3000`）。正文缩进通过 `fi=Cm(0.74)` 控制，表格/标题用 `align` 参数控制。全角空格在不同字体和排版环境下表现不一致，会导致错位。
- 脚注编号与正文之间由 Word 自动处理，不要在脚本文本前加空格。

## 已知问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 脚注显示等线字体 | bayoo-docx 不自动设置中文字体 | 创建后遍历 `fn.findall('.//w:r')` 显式设 `rFonts`：`eastAsia=宋体, ascii=Times New Roman, hAnsi=Times New Roman` |
| 脚注五号字（应为小五） | 脚本文本 run 未设 `w:sz` | 显式设 `sz=18` 和 `szCs=18`（18 half-points = 9pt = 小五号） |
| 正文引用不上标 | bayoo-docx 的 `rStyle` 匹配不到模板的样式 ID | 后处理加 `vertAlign=superscript` |
| 句号位置 | 规范要求 `。{F1}` 而非 `{F1}。` | 写作时注意句号在脚注标记前 |
| 表格全框线 | `Table Grid` 样式默认全框 | 用 lxml 移除所有边框后加三线：header top、header bottom、last row bottom |
| 封面垂直居中 | `sectPr.vAlign=center` 在 python-docx 中无效 | 用单格表格 + 行高固定(`trHeight hRule=exact`，值≈14000 twips) + 单元格 `vAlign=center`，表格宽度设100%，边框全nil |
| 分节后 `add_table` 报错 | 手工创建的 `sectPr` 缺少 `page_width` 属性 | 用 `copy.deepcopy(原sectPr)` 克隆而非 `etree.Element()` 新建 |
| `footerReference.r:id` 报错 | 属性命名空间用错 | 用 `{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id`，不是 `w:id` |
| `B()` 不支持 `sz` 参数 | 函数定义未暴露字号参数 | 小字直接用 `P(text, sz=Pt(9))`，不用 `B()` |
| 全角括号 `（`(U+FF08) 导致 SyntaxError | Python 将全角括号识别为函数调用 | 必须用半角 `(`，字符串内用全角没问题 |
| 中文引号被渲染成西文直引号样式 | 引号字符所在 run 的 `ascii/hAnsi` 为 Times New Roman | 中文引号必须拆为独立 run，`eastAsia/ascii/hAnsi` 均设为所在段中文字体（`fix_quotes()` 已内置，含嵌套单引号） |
| 图片在 Word 中显示黑色方框（LibreOffice 正常） | python-docx `add_picture()` 生成的 `<wp:inline>` 缺 `distT/distB/distL/distR` 与 `wp:effectExtent` | 在用户原 Word 文件上原位重构保留 Word 原生 drawing XML；或手动补 `distT="0" distB="0" distL="0" distR="0"` 与 `<wp:effectExtent l="0" t="0" r="0" b="0"/>` |
| 图片段 `keep_with_next` 在 Word 中出现小黑方块 | 段落的**分页控制**属性（`keep_with_next` / `keep_together`），"显示格式标记"开启时显示 | 不可打印、不影响输出；**交付给用户的稿子**若在意观感，就不要给段落设这两个属性（代价：图片与图题可能分页） |
| python-docx `add_picture` 解析含 EXIF 的相机照片失败 | 抛 `UnexpectedEndOfFileError` 或 `UnrecognizedImageError`（EXIF/TIFF 解析缺陷；剥 EXIF 后缺 JFIF 仍可能失败） | 提取用户原文件 `w:drawing` deepcopy + 手动建 media part（原始字节）插入，保留 Word 原生结构且零压缩 |
| 图片在页尾、图题流到下一页（孤行图题） | 图片段与图题未保持同页 | 图片段设 `keep_with_next = True`（注意：会带来 Word 小黑方块格式标记，见上条） |
| **Word「字数」远大于正文估算**（如正文 340 字、Word 却显示 543） | Word 把**公式（OMML）内容也计入「字数」**，行间大公式（矩阵/分式）尤甚 | 有字数上限时：① 首选 `formula` 用 **`mode: image`**（公式转为**图片，不计入字数**）；② 或删行间公式、把变量与单位集中说明；③ 少用重复的行内公式。核对口径以 Word 状态栏为准 |
| OMML 公式内空格丢失（显示 `1.2m` 而非 `1.2 m`） | pandoc 输出的 `<m:t>` 未带 `xml:space="preserve"`，Word/LO 会吞掉首尾空格 | `latex_to_omml()` 已自动为含空格的 `m:t` 补 `xml:space="preserve"` |

## 长文档/行前手册排版规范

### 封面页
- 使用**单格无边框表格**实现垂直居中，不要依赖 `sectPr.vAlign`
- 表格行高设 `hRule=exact`，值约14000 twips（A4可用高度≈24cm）
- 表格宽度设100%（`tblW type=pct w=5000`）
- 单元格 `vAlign=center`，边框全 `val=nil`

### 分节与页码
- 三节结构：封面（无页码）→ 目录（无页码）→ 正文（有页码）
- 分节方法：`sectPr` + `type=nextPage`，必须 `copy.deepcopy(原sectPr)` 后修改
- 页码添加：在最后一节的 `sectPr` 中添加 `footerReference`，指向包含 `PAGE` 域的 footer part
- 前两节不加 `footerReference` 即可隐藏页码

### 目录点线
- 用 `tab_stops.add_tab_stop(Cm(15.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)` 实现
- 内容用 `label + '\t' + str(pnum)` 拼接

### 内容组织
- 每个点位标题另起一页，用 `page_break()` + `H1()`（居中，14pt黑体）
- 调研报告内容不得缩减，必须完整保留所有子主题和问题
- 子主题用 `H3()`（10.5pt黑体），问题用 `B()` 编号
- 队旗图片放在标识解读文字上方，用 `run.add_picture(FLAG, width=Cm(10))`

### 视觉核验
- 生成后先用 LibreOffice 转 PDF：`soffice.exe --headless --convert-to pdf`
- 再用 `pdf2image.convert_from_path(pdf, dpi=150)` 转图片
- 最后**用 Read 工具直接看图片**核验排版（当前模型自带视觉能力，无需视觉脚本）
