---
name: boardgame-rulebook-zh
description: 将英文桌游 PDF 规则书汉化并保持原版图文位置。内置桌游术语表、表格/内嵌图标处理和自动 QA。Use when the user asks to translate or localize a board game rulebook PDF into Chinese, 汉化规则书，or when images/tables must stay aligned.
---

# 桌游规则书汉化

## 这个 skill 解决什么

把英文桌游 PDF 规则书翻译成中文，同时**不移动、不覆盖原版的插图、棋盘、卡牌图、图标、表格线和装饰**。译文按原段落的位置、字号、颜色和栏宽就地写回；表格单元、双栏、页眉页脚和内嵌图标都有专门处理。

它同时解决两个常见问题：

- **术语**：内置桌游术语表，区分 worker placement / deck-building / meeple / token / exhaust 等易错词，并提供项目术语库。
- **图文错位**：只擦除文字层，保留位图和矢量图；渲染后自动比对位图摘要、矢量图摘要和页面几何，任何插图移动都会报错。

## 适用 / 不适用

**适用**

- 有文字层（可选中文字）的英文 PDF 规则书，包括双栏、表格、图标、满版背景图、旋转页面。
- 用户要求“翻译成中文/汉化/保持原版排版/不要动图片”。
- 需要交付可打印 PDF，而不是重新排版的 Word/网页。

**不适用**

- 扫描版、纯图片 PDF、文字已转为矢量描边（无文字层）。本 skill 不会做覆盖式汉化，避免把中文盖在英文原图上。见 `references/scanned-pdfs.md`。
- 需要重排页面、改纸张尺寸、重画表格的“重新设计”任务。
- 连环画/漫画式对白、竖排文字、复杂表单/交互式 PDF（可尝试，但必须逐页目检）。

## 依赖

- Python 3.9+
- PyMuPDF（`pymupdf`，测试于 1.26.5）
- Pillow
- 系统中文字体（自动选择 Microsoft YaHei / PingFang / Noto Sans CJK；没有时退回 PyMuPDF 内置 CJK 字体）

```bash
python -m pip install -r requirements.txt
```

## 快速流程

```bash
# 1. 提取文字段、生成页面预览、术语命中和译文模板
python scripts/extract.py rulebook.pdf -o work

# 2. 阅读 work/source.md，填写 work/translations.tsv
#    同时检查/补充 work/termbase.tsv 与 work/glossary_hits.md

# 3. 渲染 + 自动 QA
python scripts/render.py rulebook.pdf -w work -o out

# 4. 看 out/qa/report.md 和 out/qa/pages/page_*.png
#    修译文或写 work/layout_overrides.json，重跑第 3 步
```

最终交付：`out/rulebook_zh.pdf`、`out/qa/report.md`、`work/termbase.tsv`。  
**QA 有 error 时不要交付。** 有 warning 时逐条复核；`termbase-mismatch` 是 info，只作参考。

## 第 1 步：提取

```bash
python scripts/extract.py rulebook.pdf -o work
```

输出：

| 文件 | 用途 |
| --- | --- |
| `work/source.md` | 按页/段列出原文、字号、对齐、bbox、表格/内嵌图标标记；带原页预览链接 |
| `work/segments.json` | 机器可读的分段数据（渲染用） |
| `work/translations.tsv` | 译文模板：`id<TAB>中文`；`=` 表示保留原文 |
| `work/termbase.tsv` | 项目术语库：`source<TAB>zh<TAB>category<TAB>note` |
| `work/glossary_hits.md` | 本 PDF 命中的术语表条目、建议译法、页码 |
| `work/original/page_*.png` | 原页预览 |
| `work/manifest.json` | 页数、字体、位图/矢量图摘要、警告 |

检查 `source.md` 顶部警告：

- **疑似扫描页 / 无文字层**：停止覆盖式汉化，见 `references/scanned-pdfs.md`。
- **页面大面积被图片覆盖**：确认文字是独立文字层还是烘焙在图片里。可选中文字 + 预览中文字与底图分离 = 可以继续；否则停止。
- **旋转文字**：逐行旋转的文字不会自动替换；页眉页脚/页码通常不受影响。
- **inline_art**：该段含内嵌图标/小插图；翻译要短，并对照原页确认图标顺序。

只提取部分页做试译：`--pages 1-3,5`。  
重新提取时默认要求 `--force`，并保留已有 `translations.tsv` / `termbase.tsv`；如果 id 变化，用 `--reset-translations` 重新生成。

## 第 2 步：术语库

先读 `references/glossary.csv`（推荐译法、avoid、wrong）和 `references/glossary-notes.md`（易混词解释）。

`work/termbase.tsv` 的规则：

- 第二列是**本项目**采用的译法。若官方中文版有固定译名，直接改第二列；QA 以本表为准。
- 把卡牌名、角色名、地名、组件名补进去；这些名称必须前后一致。
- 自动生成的行只是建议；`termbase-mismatch` 是 info，不是错误。
- **wrong 列**里的错译由 QA 判 error（如 meeple → 米普、deck-building → 甲板构筑）。如果某个词在本作中是特殊用法，把正确译法写进 termbase，QA 会把它视为显式覆盖。
- 官方中文版优先于本表。没有官方版时，用术语表 + 全篇一致；首次出现可加英文括号。

常用官方参考：`references/official-titles.md`。游戏名不要直译；没有把握就保留英文名。

## 第 3 步：翻译

`work/translations.tsv` 是唯一的译文入口：

- 第一列 id 不要改。
- `=`：保留原文（URL、版权行、纯页码、已经中文的段落）。
- 空白：缺失，QA 会报错（`--allow-missing` 仅用于预览）。
- 一行一段，不要写多行；换行会被合并为空格。
- 不要翻译图标、变量名、骰子记号（`2d6`）、数字。

翻译时同时读 `source.md` 和原页预览；**不要只看文字**，因为图标、表格、栏宽会决定译文长度。分段翻译建议每次 20–40 段，保持术语库一致；长书可按页分批，但不要在不同批次里换译名。

文风、句式、量词、标点、卡牌名规则见 `references/style.md`。核心要求：

- 用“你”，不用“您”；“players”=“玩家”，“each player”=“每名玩家”。
- `may`=可以，`must`=必须，`cannot`=不能，`up to`=至多，`at least`=至少，`instead`=改为。
- 中文标点全角；数字与量词之间不加空格（抽2张牌）。
- 卡牌用“打出”，游戏用“进行”，抽牌用“抽”，弃牌用“弃置”，移除用“移除”，摧毁用“摧毁”。
- 不要把 “draw”（抽牌）译成“绘制”；不要把 “deck”（牌库）译成“甲板”。
- 内嵌图标段：译文尽量短，不要把图标写掉；必要时用 `layout_overrides.json` 调整排版框。
- 译文通常比英文短；如果比原文长 1.5 倍以上，先精简。

术语/文风参考：
- `references/glossary.csv` — 机器可读术语表
- `references/glossary-notes.md` — 易混词深解释
- `references/style.md` — 文风与句式
- `references/official-titles.md` — 常见游戏官方中文名

## 第 4 步：渲染 + 自动 QA

```bash
python scripts/render.py rulebook.pdf -w work -o out
```

输出：

- `out/rulebook_zh.pdf`
- `out/qa/report.md`（中文）、`report.json`
- `out/qa/pages/page_0001.png`（左原文/右译文，逐页目检）
- `out/qa/contact_sheet.png`

渲染机制（简述，详见 `references/layout-and-qa.md`）：

- 只对每行文字 bbox 加 redaction，且 `fill=False`、`images=NONE`、`graphics=NONE`：**擦字不擦图**。
- 译文优先写回原段落 bbox；空间不够时向下借用空白，但不进入其他文字、图片、表格单元。
- 表格单元译文限制在单元格内；内嵌图标用绕图排版，并从右方借用安全空白。
- 自动缩放字号（0.25pt 步进）；低于 7pt 警告，低于 5.5pt 或放不下报错。
- 颜色、粗体、左/中/右对齐尽量沿用原样式。
- 字体自动选择系统 CJK；缺字会报 `missing-glyphs`，可用 `--font` / `--bold-font` 指定。

常用参数：

```bash
--font "C:/Windows/Fonts/simsun.ttc"     # 衬线/羊皮纸风格规则书
--bold-font "C:/Windows/Fonts/simsun.ttc"
--allow-missing                          # 只做部分预览，不算最终交付
--no-previews                            # 不生成预览（不建议用于最终交付）
--overrides work/layout_overrides.json   # 手动排版修正
```

## 第 5 步：目检 + 修正

自动 QA 通过不等于视觉通过。逐页打开 `out/qa/pages/*.png`，重点看：

1. 插图、棋盘、卡牌图、图标是否与原文同一位置；有没有被译文盖住。
2. 表格线是否完整，单元格文字有没有越界。
3. 双栏有没有串栏；标题/图注是否居中。
4. 内嵌图标与文字的先后顺序是否合理。
5. 有没有行首标点（`。，、；：！？` 出现在行首）。
6. 页眉页脚/页码是否在原位。

修正优先级：

- **先改译文**（精简/换词），不要先缩字号。
- 仍放不下，再写 `work/layout_overrides.json` 扩大/移动安全排版框。
- 最后才接受更小字号；低于 7pt 的正文要谨慎。

`layout_overrides.json` 示例（坐标是 PDF point，原点左上）：

```json
{
  "p003_s008": {
    "box": [28, 423, 292, 540],
    "font_size": 10.0,
    "align": "left",
    "note": "加宽 10pt，避免逗号落到行首"
  },
  "p003_s034": {
    "box": [297.64, 340.6, 545.0, 430.0],
    "note": "略收窄，避免句号落到行首"
  }
}
```

表格单元会被强制夹在 cell 内；overrides 不能越过表格边框。

## 质量门禁

`out/qa/report.md` 中：

- **error = 0 才能交付**。
- **warning** 逐条复核；`line-start-punctuation` 通常改译文或用 override 解决；`small-font` 要确认可读性。
- **info** 是提示（如术语库建议、自动换字体），不是错误；但仍建议看一遍。

重点错误：

| code | 含义 | 处理 |
| --- | --- | --- |
| `images-changed` / `vector-art-changed` | 位图/矢量图位置或内容变了 | 停止交付；检查是否扫描页/特殊 PDF |
| `geometry-changed` | 页面尺寸/旋转变了 | 停止；检查输入/输出 |
| `overflow` / `table-cell-overflow` | 译文放不下/越出表格 | 精简译文或 override |
| `art-covered` / `vector-covered` | 译文压住图标/插图 | 精简/override，绝不能忽略 |
| `text-overlap` / `text-overlap-source` | 译文互相压/压到未翻译原文 | 精简/override |
| `source-residue` | 原英文没擦干净 | 检查文字层/扫描页；重新渲染 |
| `text-not-found` | 输出里找不到完整译文 | 多为缺字/字体问题；换字体或改译文 |
| `missing-glyphs` | 字体缺字（emoji、生僻字） | 换字体或删掉非必要符号 |
| `missing-translation` | 漏译 | 补 `translations.tsv` |
| `glossary-wrong` | 命中明确错译 | 按 `references/glossary.csv` 改 |
| `line-start-punctuation` | 中文标点跑到行首 | 改译文或 override |
| `scanned-page` | 疑似扫描页 | 见 `references/scanned-pdfs.md` |

完整清单和逐条修法：`references/qa-checklist.md`。

## 扫描版 / 图片文字

如果 `extract.py` 报“没有提取到任何文字段”，或 `source.md` 标记扫描页：

**不要**直接跑渲染。扫描页上的英文是像素，擦除会破坏原图；把中文盖上去会造成图文重叠。  
可选方案：

1. 让用户提供有文字层的 PDF（出版社官网/官方中文版）。
2. 做双语对照版：保留原页，另附按页编号的中文译文。
3. 手动重排（InDesign/Affinity/Scribus）。
4. OCR 生成文字层后再评估；只有确认底图干净、可安全擦字时才覆盖。

详见 `references/scanned-pdfs.md`。

## 自测

```bash
python examples/selftest.py --negative
```

会生成一份合成样例规则书（双栏、表格、羊皮纸/插图、内嵌位图与矢量图标），跑完整流程，并验证：

- 0 error / 0 warning；
- 页数、页面几何不变；
- 位图摘要、位置不变；
- 矢量图摘要不变；
- 表格/内嵌图标识别；
- 负向测试能拦住错译（米普）、漏译、溢出、缺字形。

最后打印 `SELFTEST OK`。

## 交付建议

对用户说明：

- 翻译了哪些页、哪些段；保留原文多少段、缺失多少段；
- QA 错误/警告数量；是否逐页目检；
- 哪些页是扫描页/未覆盖；
- 术语库和 known limitations（如内嵌图标顺序需要人工确认）。

不要把受版权保护的原始 PDF 或整页译文提交到公开仓库；本仓库的 demo 是合成样例。

## 文件结构

```
SKILL.md
scripts/
  extract.py       # PDF → 分段/术语命中/译文模板
  render.py        # 译文 → 原位 PDF + QA
  pdf_common.py    # 字体、几何、术语、排版工具
references/
  glossary.csv     # 桌游术语表（推荐/avoid/wrong）
  glossary-notes.md
  style.md
  layout-and-qa.md
  qa-checklist.md
  scanned-pdfs.md
  official-titles.md
examples/
  make_sample.py   # 合成样例规则书
  selftest.py      # 端到端自测
  demo_page1.png   # 自测生成的 demo
```

## 许可

MIT。仅用于你有权翻译的文档。
