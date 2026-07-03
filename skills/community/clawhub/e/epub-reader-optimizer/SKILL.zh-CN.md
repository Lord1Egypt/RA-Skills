---
version: "1.0.0"
name: "epub-reader-optimizer"
description: "优化 EPUB 文件的阅读体验：重写 CSS、统一中英文双语段落排版、强制字体（如 LXGW WenKai）、美化代码块与表格、解决阅读器白底白字问题。当用户需要美化/优化 EPUB 排版、修复 EPUB 显示异常、调整 EPUB 字体或颜色时调用。"
---

# EPUB Reader Optimizer

本 skill 用于优化 EPUB 文件的阅读体验。核心做法是**不改变原 EPUB 的章节结构、HTML 文本与图片资源**，只通过重写 CSS 与必要的元数据来提升中文阅读体验、修复常见排版与渲染缺陷。


## ⚠️ 安全与副作用声明

| 行为 | 默认值 | 说明 |
|---|---|---|
| 网络访问 | 关闭 | 仅在用户明确同意后访问网络资源。 |
| 主机工具链安装 | 关闭 / 失败即止 | 不会自动运行 `pip install`、`npm install -g`、`apt install` 等。缺失依赖时报告给用户并等待手动确认。 |
| LaTeX `-shell-escape` | 关闭 | 默认不启用 `-shell-escape`；仅在用户明确同意、沙箱/容器化环境、受信内容三者同时满足时才可开启。 |

**核心原则：**

1. 默认离线，所有副作用需用户明确同意。
2. 缺失依赖时**失败即止**，不自动安装任何包。
3. 对不受信内容禁用 `-shell-escape`。
4. 远程获取资源时**固定版本/标签**，不追踪 master/main，并需用户批准。

## 灵活输入支持

本技能接受多种输入格式：

| 输入类型 | 说明 |
|---|---|
| Markdown / TXT 文件 | 最常见输入，直接处理。 |
| JSON 结构化数据 | 包含 `title`、`chapters[]`、`content` 字段时作为结构化大纲处理。 |
| 直接 LLM 上下文 | 当用户以对话方式提供内容时，自动从上下文提取大纲与正文。 |
| URL / 仓库地址 | 仅在用户明确同意后抓取远程内容。 |

## 何时调用

满足以下任一条件时调用本 skill：

- 用户提供 EPUB 文件并要求 "优化排版" / "美化样式" / "改字体" / "改颜色" / "改行距"。
- 用户反馈 EPUB 在某个阅读器/编辑器中文字看不见（白底白字、黑底黑字）、字体丑、行距太挤、图表错位、代码块乱、表格挤成一团。
- 用户希望把双语 EPUB（如中英文对照、机器翻译版）调整为"中文为主、英文为辅"或"英文在上、中文在下"的对照排版。
- 用户想给 EPUB 强制指定字体（如 LXGW WenKai 系列）。
- 用户希望整理或修复 EPUB 的 NCX 目录、封面、元信息。
- **用户反馈"公式只有一个字符也单独占一行""行内的 x/y 被强制居中换行"** —— 典型的"公式即图片"型 EPUB(常见于 Sigil/出版社流水线产出),需要先做 HTML 标签结构修复再调 CSS。

## 何时不调用

- 用户要求把 EPUB 转成 PDF / Word / Markdown 等其他格式 → 改用对应转换工具。
- 用户要求逐字重写、翻译或大幅修改正文 → 不属于排版优化，且涉及版权风险。
- 用户提供的不是 EPUB（如 mobi、azw3、纯 HTML、PDF）→ 先转 EPUB 再来。

## 工作流总览

```
1. 准备工作目录与解包 EPUB
2. 探查 EPUB 结构（content.opf / toc.ncx / 现有 CSS / 章节 XHTML 抽样）
3. 与用户对齐需求（字体、双语策略、颜色基调）
4. 重写主 CSS（stylesheet.css）+ 必要时改 page_styles.css
5. 视情况调整 OPF / NCX（罕见，多数只改 CSS）
6. 重新打包为合规 EPUB（mimetype 必须 STORED 且为第一个条目）
7. 自检：用 Python 验证 zip 结构；如可用 epubcheck 则进一步验证
8. 把成品放到用户的 workspace 目录并给出 computer:// 链接
```

如果是**公式即图片型 EPUB**（公式被栅格化为 GIF，alt 中含 LaTeX），在 4 之前增加：
- 4a. 用 `assets/optimize_formula_images.py` 处理 xhtml（包公式 img、加 code-block 类、自动给孤立公式段加 formula-block 类）。
- 4b. 用 `assets/subset_fonts.py` 把下载的 LXGW WenKai TTF 子集化为 WOFF2 嵌入。
- 4c. 用 `assets/stylesheet.formula-image.css` 作为基础 CSS（包含公式行内/块级双轨规则）。
- 4d. 在 `content.opf` 的 `<manifest>` 里登记 WOFF2 字体（`media-type="font/woff2"`）。

## 可复用 Asset

- `assets/build_epub.py` — 通用：把目录打包为合规 EPUB（mimetype STORED 优先）。
- `assets/stylesheet.template.css` — 通用：双语 EPUB 基础 CSS 模板。
- `assets/optimize_formula_images.py` — 公式即图片型 EPUB：HTML 标签结构修复脚本。
- `assets/subset_fonts.py` — 公式即图片型 EPUB（也适用其他场景）：TTF → 子集 WOFF2。
- `assets/stylesheet.formula-image.css` — 公式即图片型 EPUB：含公式双轨规则的 CSS。

## 环境与工具

- Python 3（必备）：用于 zipfile 重新打包。
- 7-Zip 或系统解压（解 EPUB 用，EPUB 就是 zip）。
- 可选：`epubcheck`（更严格的 EPUB 合规性检查）；没装也不阻塞，跳过即可。

不要使用 PowerShell 的 `Compress-Archive` 打包 EPUB，它产生的 zip 不满足 EPUB 规范（mimetype 顺序、压缩方式不对）。**必须用 Python zipfile**。

## 解包 EPUB

使用 7z 或 Python zipfile 解压：

```powershell
& 'C:\Program Files\7-Zip\7z.exe' x 'book.epub' '-oepub_extract' -y
```

或 Python：

```python
import zipfile
zipfile.ZipFile('book.epub').extractall('epub_extract')
```

解包后通常包含：

- `mimetype`（内容固定：`application/epub+zip`）
- `META-INF/container.xml`（指向 OPF）
- `content.opf` 或 `OEBPS/content.opf`（清单 + 阅读顺序 + 元数据）
- `toc.ncx`（EPUB2 导航）或 `nav.xhtml`（EPUB3 导航）
- `stylesheet.css`、`page_styles.css`（待重写）
- `OEBPS/html/*.xhtml`（章节正文）
- `OEBPS/images/...`（图片、SVG 公式）

## 探查与决策

读取 `content.opf` 与 `toc.ncx`，获取：

- 书名、作者、出版社、语言（`<dc:language>`）。
- 章节数量与顺序。
- 是否双语（lang 属性是否同时存在 `en` 与 `zh`，是否每段是英文+中文相邻排列）。

随机读 1～2 个章节 XHTML，确认：

- 段落是否用 `<p lang="en">` + `<p lang="zh">` 相邻成对出现。
- 代码块容器是 `.programcode` / `.fixedline` 还是其他类名。
- 表格容器是 `.tablestyle` / `.tablestyle1..7` 还是标准 `<table><thead><tbody>`。
- 公式是 SVG 图（如 Springer 用的 `*_TeX_Eq*.svg` / `*_TeX_IEq*.svg`）还是 **GIF/PNG 图片**（alt 属性带 LaTeX 代码，如 Sigil/出版社流水线产出）。
- 若发现「整本书只有 1 个巨大的 xhtml 文件」+「gif 图片是公式」，这是典型的**公式即图片型 EPUB**，必须先处理 HTML 结构再调 CSS。

根据探查结果决定哪些选择器需要重写。

## 与用户对齐需求（建议优先询问）

如果用户的需求未明确，使用 AskUserQuestion 工具询问：

1. **字体**：是否强制指定中文字体（如 LXGW WenKai、思源宋体、苹方）？是否需要等宽代码字体（如 LXGW WenKai Mono）？
2. **双语策略**：
   - 英文在前、中文在后（适合"以英文为主，中文当参考"）。
   - 中文在前、英文在后（适合"以中文为主"）。
   - 仅显示中文，隐藏英文（CSS `display:none`，但保留 DOM 以便切换回来）。
3. **颜色基调**：纯黑/纯蓝等高饱和纯色，还是浅灰柔和色？
4. **是否需要暗色模式**：很多编辑器会误触发 `prefers-color-scheme: dark`，造成白底白字。**默认应禁用暗色模式**，除非用户明确要求。

## 公式即图片型 EPUB 的处理（重要）

很多中文出版社/Sigil 流水线产出的技术书 EPUB，公式被栅格化为 **GIF 图片**嵌入正文，`<img alt="...">` 的 alt 属性里保存了 LaTeX 源码。整本书往往只有一个超大 xhtml 文件。这类 EPUB 的典型缺陷与修复策略如下。

### 缺陷一：行内的单字符公式被强制换行

**症状**：截图中能看到「线性回归通过训练学习得到一个线性模型来最大限度根据输入 *x*」中的 *x* 单独占了一整行，居中显示；下一行才接「拟合输出 *y*」。

**根因**：

1. 原 EPUB 的 `<img>` 没有任何提示是行内符号还是独立公式块。
2. 容易写出这样的"通用规则"：`img { display:block; margin:auto }`——结果所有 img 都被块化、独占一行。
3. 即使你写了"识别 LaTeX 命令"的脚本，单字符的 `alt="x"` / `alt="y"` 因为不含反斜杠、不含 `{}`，会被漏判成"普通图片"，仍走 block 规则。

**修复策略（两层防御）**：

#### 第一层：脚本层正确识别公式

`has_math_formula(alt)` 必须把「短拉丁/希腊字母」也判定为公式，而不是只看是否有 LaTeX 命令：

```python
def has_math_formula(alt: str) -> bool:
    if not alt or alt.strip() == "" or alt.strip() == "{%}":
        return False
    s = alt.strip()
    # 含 LaTeX 命令、上下标、括号
    if re.search(r"\\[a-zA-Z]+|[\\{}_^]", s):
        return True
    # 数学符号
    if any(c in s for c in "=+−×÷≤≥≠≈∞√∑∫∈⊂⊆∩∪σμθβαλγδπωε∂"):
        return True
    # 关键补丁：短(≤4 字符)的纯字母/数字也视为数学符号
    if len(s) <= 4 and re.fullmatch(r"[A-Za-zα-ωΑ-Ω0-9\s,\.\;]+", s):
        return True
    return False
```

把识别出的公式 img 包裹成 `<span class="math-inline">`，并把 `alt` 中的 LaTeX 源码保留到 `data-latex`：

```python
def wrap_formula(match):
    full = match.group(0)
    alt = re.search(r'alt="([^"]*)"', full).group(1)
    src = re.search(r'src="([^"]*)"', full).group(1)
    if not has_math_formula(alt):
        # 非公式 img: 标记为 content-img，CSS 默认行内
        return re.sub(r'<img ', '<img class="content-img" ', full, count=1)
    return (
        f'<span class="math-inline" data-latex="{html_escape(alt)}">'
        f'<img src="{src}" alt="{html_escape(alt)}" class="formula-img" />'
        f'</span>'
    )

content = re.sub(r"<img[^>]+/>", wrap_formula, content)
```

完整脚本见 `assets/optimize_formula_images.py`。

#### 第二层：CSS 公式行内/块级双轨

无论上述识别是否完美，CSS 都用"**默认行内，仅在 p.图 这种独立段落内才居中独占一行**"的双轨结构兜底：

```css
/* 默认行内 —— 公式跟随文字流，按文字基线对齐 */
span.math-inline,
span.math-formula {
  display: inline;
  line-height: inherit;
}
span.math-inline img.formula-img,
span.math-formula img.formula-img {
  display: inline;
  vertical-align: middle;
  max-height: 1.3em;   /* 紧贴文字高度 */
  width: auto; height: auto;
  margin: 0 0.1em;
}

/* 仅当父段落是 p.图 / p.sgc-11 / p.sgc-3 时才独占一行居中（原书已用此类标识"独立公式段"） */
p.图, p.sgc-11, p.sgc-3 {
  text-align: center;
  margin: 0.9em 0;
  line-height: 1.2;
  page-break-inside: avoid;
}
p.图 span.math-inline,
p.图 span.math-formula,
p.sgc-11 span.math-inline,
p.sgc-3 span.math-inline {
  display: inline-block;
  line-height: normal;
  max-width: 100%;
  overflow-x: auto;
}
p.图 img.formula-img,
p.图 > img,
p.sgc-11 img.formula-img,
p.sgc-3 img.formula-img {
  display: inline-block;
  vertical-align: middle;
  max-height: none;
  max-width: 95%;
  height: auto;
  margin: 0;
}

/* 内容图（非公式）也按同样思路：默认行内,只有独立段落里才居中独占 */
img.content-img {
  display: inline;
  vertical-align: middle;
  max-height: 1.3em;
  max-width: 100%;
  width: auto; height: auto;
  margin: 0 0.1em;
}
p.图 img.content-img,
p.sgc-11 img.content-img,
p.sgc-3 img.content-img {
  display: inline-block;
  max-height: none;
  max-width: 96%;
  margin: 0.4em auto;
}

/* 兜底：任何未加类的 img 在普通段落中也按行内处理 */
p > img:not(.content-img):not(.formula-img) {
  display: inline;
  vertical-align: middle;
  max-height: 1.3em;
  width: auto;
  margin: 0 0.1em;
}

span.math-tex { display: none; }  /* LaTeX 文本备份(将来 MathJax 用) */
```

### 缺陷二：原书没有给独立公式段落显式 class

如果原书既没有 `p.图` 也没有任何 class 标识独立公式段，需要在脚本里自动添加：

```python
# 段落唯一/主要内容是公式 img → 加 class="formula-block"
pattern = re.compile(r"<p(\s[^>]*)?>\s*<img([^>]+)/>\s*</p>")
content = pattern.sub(
    lambda m: f'<p class="formula-block"{m.group(1) or ""}><img{m.group(2)}/></p>',
    content,
)
```

然后 CSS 加：

```css
p.formula-block {
  text-align: center;
  margin: 0.9em 0;
  page-break-inside: avoid;
}
p.formula-block img { max-height: none; max-width: 95%; }
```

### 缺陷三：代码块缺乏样式（出版社转的 `<pre><code>` 通常裸跑）

给 `<pre>` 加 `code-block` 类，统一加边框 + 圆角 + 左侧高亮条 + 浅灰背景：

```python
content = re.sub(
    r"<pre(\s|>)",
    lambda m: f'<pre class="code-block"{m.group(1)}',
    content,
)
```

CSS：

```css
pre.code-block, pre.代码无行号 {
  font-family: "LXGW WenKai Mono", Consolas, monospace;
  font-size: 0.82em;
  line-height: 1.55;
  background-color: #f8f9fb;
  color: #2d2d2d;
  border: 1px solid #d4d8de;
  border-left: 4px solid #4a90d9;
  border-radius: 6px;
  padding: 0.9em 1em;
  margin: 1.3em 0;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  tab-size: 4;
  page-break-inside: avoid;
}
```

## 字体嵌入与子集化（重要）

强制字体只有"声明 `@font-face`"还不够——绝大多数移动端阅读器没有 LXGW WenKai 等字体。必须把字体文件**嵌入 EPUB**。但完整版的 LXGW WenKai 是 14 MB 的 TTF，两套(正文+等宽)就 28 MB，会让 EPUB 变成「小说级体积的字体包」。

**正确做法：先子集化再嵌入**。只保留 EPUB 实际用到的字符，把 14 MB TTF 压到 300 KB 左右的 WOFF2。

### 下载字体源文件

LXGW WenKai Lite（轻便版，更小）的下载地址：

- 正文：`https://github.com/lxgw/LxgwWenKai-Lite/releases/download/v1.522/LXGWWenKaiLite-Regular.ttf`
- 等宽：`https://github.com/lxgw/LxgwWenKai-Lite/releases/download/v1.522/LXGWWenKaiMonoLite-Regular.ttf`

> 提示：jsDelivr/raw.githubusercontent 取这两个文件往往 403/404，直接走 GitHub Releases。

### 子集化（依赖 fontTools + brotli）

依赖：`fonttools`、`brotli`。不要自动运行 `pip install`；报告缺失依赖并等待用户手动安装。

参考脚本 `assets/subset_fonts.py`：

```python
import re
from pathlib import Path
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

# 1. 从所有 xhtml 中收集实际使用到的字符
chars = set()
for xhtml in Path("OEBPS/Text").glob("*.xhtml"):
    txt = re.sub(r"<[^>]+>", " ", xhtml.read_text(encoding="utf-8"))
    chars.update(txt)
# 兜底：ASCII 可见、CJK 标点、全角 ASCII
chars.update(chr(c) for c in range(0x20, 0x7F))
chars.update(chr(c) for c in range(0x3000, 0x3040))
chars.update(chr(c) for c in range(0xFF00, 0xFFF0))

def subset(ttf_in, woff2_out):
    font = TTFont(ttf_in)
    opts = Options(); opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.layout_features = ["*"]; opts.name_IDs = ["*"]
    opts.notdef_outline = True; opts.recommended_glyphs = True
    sub = Subsetter(options=opts)
    sub.populate(text="".join(sorted(chars)))
    sub.subset(font)
    font.flavor = "woff2"
    font.save(woff2_out)

subset("Fonts/LXGWWenKaiLite-Regular.ttf",      "Fonts/LXGWWenKai.woff2")
subset("Fonts/LXGWWenKaiMonoLite-Regular.ttf",  "Fonts/LXGWWenKaiMono.woff2")
```

实测：1600+ 中文字符 + 全 ASCII 的子集，单个字体压到约 **310 KB**（TTF→44× 体积压缩）。

### 在 OPF 中登记字体

```xml
<item id="font_wenkai"      href="Fonts/LXGWWenKai.woff2"     media-type="font/woff2"/>
<item id="font_wenkai_mono" href="Fonts/LXGWWenKaiMono.woff2" media-type="font/woff2"/>
```

注意 media-type 必须是 `font/woff2`（不是 `application/font-woff2`，后者已废弃）。

### CSS 声明

```css
@font-face {
  font-family: "LXGW WenKai";
  src: url("../Fonts/LXGWWenKai.woff2") format("woff2");
}
@font-face {
  font-family: "LXGW WenKai Mono";
  src: url("../Fonts/LXGWWenKaiMono.woff2") format("woff2");
}
```


## CSS 重写要点（按优先级）

### 必做：解决"白字"问题

部分 EPUB 编辑器（Sigil、Calibre 内置编辑器）的预览 webview 会把浅色界面也判定为 dark scheme，触发 `@media (prefers-color-scheme: dark)` 块，把文字渲染为白色——白底白字看不见。

**默认必做的三层保护**：

```css
/* 1. 强制白底 */
html, body, section, article, div, p, span,
h1, h2, h3, h4, h5, h6, li, td, th, blockquote, figure, figcaption {
  background-color: #ffffff !important;
}

/* 2. 强制黑字（容器级） */
html, body, section, article, div, p, span,
h1, h2, h3, h4, h5, h6, li, td, th, blockquote, figcaption {
  color: #000000 !important;
}

/* 3. 不写 @media (prefers-color-scheme: dark) 块，避免被误触发 */
```

关键颜色规则（标题、中英文段落、链接）都加 `!important`。

### 强制字体（覆盖原 EPUB 字体）

使用 `!important` 覆盖原有的 Cambria/Times/SimSun 等：

```css
body, p, div, span, h1, h2, h3, h4, h5, h6, li, td, th, caption,
.calibre, .chaptertitle, .heading1, .heading2, .heading3, .heading4,
.heading5, .heading6, .heading8, .heading10,
.para, .para1, .para2, .para3, .simplepara, .simplepara1 {
  font-family:
    "LXGW WenKai", "LXGW WenKai Screen", "LXGW WenKai GB",
    "霞鹜文楷", "霞鹜文楷 GB",
    "Source Han Serif SC", "Noto Serif CJK SC",
    "Songti SC", "STSong", "SimSun", serif !important;
}

.programcode, .programcode1, .fixedline, .fixedline1,
.emphasisfontcategorynonproportional {
  font-family:
    "LXGW WenKai Mono", "霞鹜文楷等宽", "霞鹜文楷 Mono",
    "Source Code Pro", "JetBrains Mono",
    "Consolas", "Menlo", "Courier New", monospace !important;
}
```

字体名同时写中文与英文两种字符串（不同阅读器读到的字体名不同）。用户机器上若未安装目标字体，会自动回退到列表后续字体，不会出错。

### 双语段落排版

如果源 EPUB 已经把 EN 段落和 ZH 段落相邻排列（EN 在前），不需要改 DOM，**只靠 CSS 调整视觉权重**：

```css
[lang="en"], [xml\:lang="en"] {
  color: #0000cc !important;   /* 纯蓝，与中文区分 */
  font-size: 0.92em;
}

[lang="zh"], [xml\:lang="zh"] {
  color: #000000 !important;   /* 纯黑，正文主色 */
  font-weight: 500;
}

/* 给中文段落加左边线，强化"主读"地位 */
p[lang="zh"], p[xml\:lang="zh"],
div.collaboratorsection[lang="zh"],
div.para2[lang="zh"] {
  border-left: 3px solid #0000ff;
  padding: 0.15em 0.6em 0.15em 0.8em;
  margin: 0.4em 0 0.9em 0;
}

/* EN→ZH 之间收紧间距，让配对感更强 */
p[lang="en"] + p[lang="zh"],
div[lang="en"] + div[lang="zh"] {
  margin-top: 0.25em;
}
```

需要"隐藏英文只看中文"时：

```css
[lang="en"], [xml\:lang="en"] { display: none !important; }
```

### 代码块

加方框、等宽字体、自动换行、避免分页打断：

```css
.programcode, .programcode1 {
  display: block;
  background: #ffffff !important;
  border: 1.5px solid #000000;        /* 实线方框 */
  border-radius: 4px;
  padding: 0.8em 1em;
  margin: 1em 0;
  font-family: "LXGW WenKai Mono", "Source Code Pro", monospace !important;
  font-size: 0.92em;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #000000 !important;
  page-break-inside: avoid;
  break-inside: avoid;
}
```

**Springer EPUB 已知坑**：代码行有时被 `.copyrightpageissns` 包了一层造成行间距异常，需要重置：

```css
.programcode .copyrightpageissns,
.programcode1 .copyrightpageissns {
  display: block; padding: 0; margin: 0;
}
```

### 表格（booktabs 风格）

去掉繁杂边框，只保留顶/底两条粗线 + 行间细线；窄屏自动横向滚动：

```css
.table { display: block; overflow-x: auto; margin: 1em 0; }

.tablestyle {
  display: table;
  border-collapse: collapse;
  margin: 0.5em auto;
  border-top: 2px solid #000000;
  border-bottom: 2px solid #000000;
}

.tablestyle1, .tablestyle2, .tablestyle3, .tablestyle4,
.tablestyle5, .tablestyle6, .tablestyle7 {
  display: table-cell;
  padding: 0.45em 0.8em;
  vertical-align: top;
  text-align: left;
}

/* 表头 */
.tablestyle1, .tablestyle2, .tablestyle5 {
  font-weight: 700;
  color: #0000ff;
  border-bottom: 1.5px solid #000000;
}

/* 表体 */
.tablestyle3, .tablestyle4, .tablestyle6, .tablestyle7 {
  border-bottom: 1px solid #cccccc;
}
```

### 图片与公式

Springer 类 EPUB 给图片硬编码了固定 em 宽度，要覆盖为响应式：

```css
.imagestyle, .imagestyle1, .imagestyle2, /* ...直到 imagestyle19 */ {
  width: auto !important;
  max-width: 100% !important;
  height: auto;
}

img { max-width: 100%; height: auto; vertical-align: middle; }

/* 行内公式 SVG 按 1em 高度嵌入 */
img[src*="_TeX_IEq"] {
  display: inline-block;
  height: 1em;
  vertical-align: middle;
  margin: 0 0.15em;
}
```

### 标题层级

清晰的字号/颜色阶梯：

```css
.chaptertitle, .calibre1 { font-size: 1.7em; color: #0000ff !important; }
.heading2, .heading4, .heading5 { font-size: 1.3em; color: #0000ff !important; }
.heading1, .heading6, .heading8, .heading10 { font-size: 1.13em; color: #0000ff !important; }
```

中文版本的标题（`[lang="zh"]`）改成 `#000000` 黑色，让中文标题成为视觉锚点。

## 重新打包 EPUB（关键！）

**必须用 Python**，不能用 PowerShell `Compress-Archive`。EPUB 规范要求：

- `mimetype` 必须是 zip 中**第一个**条目。
- `mimetype` 必须 **STORED**（不压缩）、不能有 extra field。
- 其他文件可 DEFLATE 压缩。

参考脚本：

```python
import os, zipfile
from pathlib import Path

SRC = Path("epub_optimized")
OUT = Path("output.epub")

# 确保 mimetype 文件存在
(SRC / "mimetype").write_text("application/epub+zip", encoding="ascii")

if OUT.exists():
    OUT.unlink()

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
    # 1) 第一个写入 mimetype，且 STORED
    zi = zipfile.ZipInfo("mimetype")
    zi.compress_type = zipfile.ZIP_STORED
    zi.external_attr = 0o644 << 16
    zf.writestr(zi, "application/epub+zip")

    # 2) 其余文件 DEFLATE
    added = {"mimetype"}
    for root, _, files in os.walk(SRC):
        for name in files:
            full = Path(root) / name
            rel = full.relative_to(SRC).as_posix()
            if rel in added:
                continue
            zf.write(full, rel, compress_type=zipfile.ZIP_DEFLATED)
            added.add(rel)
```

## 自检

打包完成后用 Python 快速验证：

```python
import zipfile
z = zipfile.ZipFile("output.epub")
assert z.namelist()[0] == "mimetype", "mimetype 必须是第一个条目"
assert z.getinfo("mimetype").compress_type == zipfile.ZIP_STORED, "mimetype 必须未压缩"
assert z.read("mimetype") == b"application/epub+zip"
print("OK, 共", len(z.namelist()), "个条目")
```

如系统有 `epubcheck`，再跑一遍：`epubcheck output.epub`。没有也不阻塞。

## 文件放置规范

- 解包目录、临时脚本、原始 EPUB 副本 → 放工作目录（`{workspace}/...` 之外的临时区）。
- 最终优化后的 EPUB → 放到用户的 workspace 目录，给出 `computer://` 链接。
- 不要把 `epub_extract/` 留在用户 workspace 中污染目录。

## 交付回复模板

完成后用简洁的格式回复用户：

```markdown
已生成优化后的 EPUB：

📖 [打开优化后的 EPUB](computer://.../book_optimized.epub)

**本次优化要点**

- 字体：…
- 双语段落：…
- 代码块：…
- 表格：…
- 颜色：…
- 修复：…（如有）

如果在某个阅读器里仍显示异常，多半是阅读器开启了"使用阅读器字体/颜色"，关闭该开关即可。
```

## 常见问题速查

| 现象 | 根因 | 处理 |
|---|---|---|
| 文字变白看不见 | 编辑器误触发 dark scheme | 删除 `@media (prefers-color-scheme: dark)` 块；加 `color !important` |
| 字体没换 | 选择器优先级不够 | 加 `!important`；字体栈写中英文两种字符串 |
| 中文段落不突出 | 与英文混在一起没层级 | 加左边线 `border-left` + `padding-left` |
| 图片溢出页面 | 原 CSS 用了固定 em 宽度 | 覆盖 `.imagestyle*` 为 `width:auto; max-width:100%` |
| 代码块挤成一行 | 没设 `white-space` | `white-space: pre-wrap; word-wrap: break-word` |
| 表格挤变形 | 单元格内容长 | 外层 `.table { overflow-x: auto }`；表格 `border-collapse: collapse` |
| 打包后 EPUB 打不开 | mimetype 不是第一个 / 被压缩 | 必须用 Python zipfile 按规范打包，不要用 Compress-Archive |
| 章节首页 © 信息条太大太黑 | 原 CSS 用了大字号 | 缩小到 `font-size: 0.78em; color: #555` |
| **行内的单字符公式独占一行**（如 *x*、*y*） | `has_math_formula` 漏判短拉丁字母为公式；CSS `img{display:block}` 强制块化 | 脚本里把"≤4 字符的纯字母/数字"也判为公式；CSS 默认 `img { display:inline; max-height:1.3em }`，仅在 `p.图/p.sgc-11/p.sgc-3` 等独立段落里才居中 |
| 嵌入的 LXGW WenKai 让 EPUB 变成 30MB | 完整 TTF 太大 | 用 `fontTools` 做字符子集化转 WOFF2，单字体可压到 ~300 KB |
| OPF 注册字体后阅读器仍不加载 | media-type 用错 | WOFF2 必须用 `font/woff2`（非 `application/font-woff2`） |
| 公式独立成段没居中 | 原书没用 `p.图` 等标识独立公式 | 脚本里检测「段落只含一个 img」时自动加 `class="formula-block"`，CSS 给该类居中 |

## 禁止事项

- 不要重写原 EPUB 的章节正文文本（这属于改原作内容，且对受版权保护的书涉及侵权）。
- 不要用 `Compress-Archive` 打包 EPUB。
- 不要在没有 `!important` 时假定颜色规则会生效——阅读器主题非常爱覆盖颜色。
- 不要为了"现代感"在 EPUB 里写复杂的 flex/grid，老旧阅读器（如某些 Kindle 转换器、KOReader 老版本）不支持。
- 不要假设用户系统有指定字体，字体栈必须有降级回退。
