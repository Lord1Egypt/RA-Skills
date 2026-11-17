---
name: easy-html
description: >
  Turn any content — Markdown, plain text, images, tables, Excel (.xlsx), Word (.docx) —
  into a polished single-page HTML, pick one of 19 built-in themes, set the page Title
  and FavIcon, then publish it as a live page. When the input is already a well-designed
  HTML page (or an image with a clear layout), it switches to "layout inheritance" mode:
  the original layout is kept intact and only the colour theme is swapped, instead of
  tearing it apart and rebuilding. Use when the user says "turn this into a web page",
  "make this an HTML page", "convert this doc/table/Excel to HTML", "make it pretty",
  "把这个转成网页", "做成 HTML 页面", "内容转 HTML".
---

# easy-html

- **Version**: 1.0.1
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/html-tool-suite
- **Website**: https://songhonglei.github.io/html-tool-suite/easy-html/

把「任意内容」变成「精美网页」的流水线：输入归一化 → 选样式 → 设 Title/FavIcon → 发布。

**不重造轮子**：19 套主题 CSS 复用姊妹项目 [html-golive](https://github.com/Songhonglei/html-golive)
（`pip install html-golive`），发布也可以用它。本 skill 只做「内容 → 语义化 HTML 骨架 → 套皮 → 发布」这条线。

## 安装

```bash
pip install html-golive        # 提供 19 套主题 CSS 引擎 + 可选的发布能力
pip install openpyxl           # 可选：读 .xlsx 时需要
```

引擎查找优先级（`scripts/_engine.py`）：
`EASY_HTML_CSS_ENGINE` 指定的文件 → 已安装的 `golive` 包 →
`EASY_HTML_GOLIVE_HOME` / `./html-golive` 源码目录。都找不到会明确报错并给安装指引，
**不会静默下载任何东西**。

产物默认写到 `./output/easy-html/`，可用 `EASY_HTML_OUT` 覆盖。

## 🔀 第 0 步：先判断走「重做」还是「继承」（关键）

输入进来**先判断它有没有已成型的优雅布局**，决定两条路径之一：

| 输入特征 | 路径 | 怎么做 |
|---|---|---|
| **已是布局优雅的成品 HTML**（自带栅格/banner/固定比例/精心间距，如导出的幻灯片、设计稿 HTML、已有网页） | **🅑 布局继承** | **保留原布局与结构**，只把配色接到主题变量，套 19 套时布局不变只换色。见下方「布局继承路径」 |
| **已是布局优雅的图片**（截图/海报/PPT 截图，有清晰版式但无 HTML 源） | **🅑 布局继承（图片版）** | 让 agent **照着图片的版式 1:1 复刻** HTML 骨架（沿用其栅格/banner/比例/留白），颜色用 `--eh-*` 变量，再走继承套主题。**不要**降级成通用卡片骨架 |
| **松散内容**（Markdown / 纯文字 / Excel / Word / 无版式的表格） | **🅐 重做** | 走下方「核心工作流（4 步）」，扫描可视化机会 → 生成 data-role 骨架 → apply_layout → apply_style |

**判断尺度**：原输入拿给设计师看，他若觉得「这版式本身已经很专业」→ 走继承（别毁掉它）；若觉得「这只是一堆没排过版的内容」→ 走重做。

> ⚠️ 反模式：把一份精心设计的横向三列幻灯片 HTML 打散重做成通用纵向卡片骨架，
> 结果三列折行、卡片框喧宾夺主，**比原稿丑**。原稿已优雅时，继承 > 重做。

## 🅑 布局继承路径

适用于输入已有优雅布局（HTML 成品 或 有清晰版式的图片）。

1. **拿到/复刻源 HTML**：
   - 源是 HTML → 直接用
   - 源是图片 → agent **照图 1:1 复刻** HTML（沿用其栅格列数/banner/比例/间距/对齐），不简化版式
2. **脱敏 / 改内容**（如需）：去掉客户名等敏感信息（grep 自查 0 残留）。
3. **把源 `:root` 颜色改成引用 7 个继承变量**（这是继承的契约）：
   `--eh-primary` / `--eh-primary-light` / `--eh-bg` / `--eh-surface` / `--eh-text` / `--eh-text-muted` / `--eh-border`。
   原有 class（`.cols`/`.hdr`/`.it`…）和布局 CSS **一律不动**，只在 `:root` 把硬编码色改成
   `--原变量名: var(--eh-xxx)`（保留旧变量名，下游 class 不用改）。
   ```bash
   python3 scripts/inherit_layout.py <html> --check   # 校验是否已接入 --eh-*
   ```
4. **逐主题套色 + 字体**（布局不变，只换 :root 配色 + 主题字体覆盖）：
   ```bash
   python3 scripts/inherit_layout.py <html> --style <key> -o <out>   # 19 套循环
   ```
   继承时会自动把主题的**正文/标题字体栈**也带过来（如故宫风的古风衬线、
   报纸风的杂志衬线、蒸汽朋克的罗马衬线），并注入字体加载链接。
   代码块 `<code>/<pre>` 和图标字体（Font Awesome 等）自动豁免，不会被主题字体覆盖。
5. 设 Title/FavIcon（同重做路径）→ 提醒发布。

继承路径**不调主题引擎的 enhance**（那会按 data-role 重排结构），只解析主题的 7 个语义变量
注入覆盖 `:root`，所以**原布局 100% 保留**。脚本是幂等的，可反复换主题。

## 核心工作流（4 步）

### 1. 输入归一化
按输入类型拿到结构化内容：

| 输入 | 怎么处理 |
|------|---------|
| 在线文档 | 先用你手边的工具导出为 Markdown，再走下面的 md 解析 |
| Markdown / 纯文字 | `python3 scripts/ingest.py <file>` 或 `--text "..."` / `--stdin` |
| 图片 | 嵌入（可访问 URL；本地图先传到任意图床/对象存储），或按数据用 CSS/SVG 重绘 |
| 表格（粘贴 / MD 表格） | 直接转 HTML `<table>`（带 data-role） |
| Excel `.xlsx` | `python3 scripts/ingest.py data.xlsx`（需 openpyxl，每 sheet 一个表格块） |
| Word `.docx` | `python3 scripts/ingest.py doc.docx`（零依赖解析，抓标题/段落/表格） |
| `.xls` / `.doc` 老格式 | ingest 会返回降级提示：让用户另存为 .xlsx/.docx 或粘贴文本 |

`ingest.py` 输出 JSON（blocks: heading/paragraph/table/raw + title_hint），据此理解内容。

### 2. 🔴 可视化机会扫描（强制，生成骨架前必做）
**这是「图文并茂」的关键，跳过会退化成原文搬运。** 先把内容当「要设计的素材」扫一遍：
识别关键数字/占比/排名/趋势/流程/对比/时间线 → 决定转成哪种**可视化组件或图表**，
而不是默认画成表格/纯文字。完整扫描表 + 信息层级 + 自检清单见 **references/VIZ_SCAN.md**（必读）。

### 3. 生成语义化 HTML 骨架（图文并茂）
按扫描结果生成结构，**优先用可视化组件/图表呈现数据**，表格只用于真·多维对照矩阵。
**只产语义结构 + data-role/组件 class，绝不写死配色/背景**（配色交给样式 CSS）。

> 🎨 **生成前必读 references/DESIGN.md**：设计 token（间距刻度/阴影分层/字重层级）、
> 标题区与卡片规范、**可视化选型决策表**（趋势→折线、排名→雅致血条，别用反了）、
> 雅致血条结构。这些规范决定产物是否"有设计感"。

- **可视化组件库**（大数字卡/进度条/环形/对比条/donut/流程/时间轴/标签云/VS/信息条）HTML 片段：见 **references/VIZ_COMPONENTS.md**
- **真图表**（Chart.js 折线/柱状/饼/雷达，多源 CDN 兜底）：见 **references/CHARTS.md**
- 内容类型 → 版式映射、0 遗漏等内容质量原则：见 **references/CONTENT_STRUCTURE.md**
- data-role 标注规范：见 **references/DATA_ROLE.md**
- 保存到 `./output/easy-html/<name>.html`（或 `$EASY_HTML_OUT`）

**⚠️ 然后必须注入基础资产**（关键步骤，别漏）：
```bash
python3 scripts/apply_layout.py <html>
```
原因：19 套主题 CSS **只写配色，明文禁止写布局**（width/padding/margin/grid 全被过滤）。
布局 + 可视化组件 + 图表助手必须由生成的 HTML 自带。`apply_layout.py` 一次注入三层：
- `layout_base.css`：居中容器 880px + 卡片网格 + 留白 + 表格 + 响应式
- `viz_components.css`：可视化组件库样式（用主题变量取色，深浅主题自适应）
- `chart_helper.js`：Chart.js 多源 CDN 兜底渲染器（页面含 `data-eh-chart` 时才生效）

三层都**只管布局/组件不碰主题配色**，和主题 CSS 各管一层、不冲突。

### 4. 选样式 + 设 Title/FavIcon
**选样式**：列 19 种 + 按内容智能推荐，让用户选（话术见 references/STYLES.md）。然后：
```bash
python3 scripts/apply_style.py <html> --style <key> -o <out>
# --list 查看 19 种
```
样式会自动打 data-role 标注 + 注入 CSS（深色样式如 bloomberg/palace 也安全）。

**设 Title**（自动从 ingest 的 title_hint 提取，可让用户改）：
```bash
python3 scripts/set_meta.py <html> --title "<标题>"
```

**设 FavIcon（可选，可跳过）**：不强制。用户想要简单图标时，用 emoji/单字生成：
```bash
FAV=$(python3 scripts/make_favicon.py --emoji 📊)   # 零依赖 SVG data URI
python3 scripts/set_meta.py <html> --title "<标题>" --favicon "$FAV"
```
跳过 favicon 时浏览器会用默认图标，无需处理。想用图片做图标，先传到图床拿 URL。

### 5. 提醒发布（确认后才发）
HTML 就绪后**提醒**用户可以发布成线上页面，**用户确认后**再发。
对外操作先问，不要直接发。详见 **references/PUBLISH.md**。

```bash
golive publish <html> --name "<页面名>"      # pip install html-golive
```
产物是自包含单文件 HTML，任何静态托管（GitHub Pages / Netlify / S3 / 本地 http.server）
都能直接用。把可访问 URL 给用户（业务名做锚文本）。

## 脚本清单

| 脚本 | 作用 |
|------|------|
| `scripts/ingest.py` | 统一输入解析：xlsx/docx/md/txt/text/stdin → 结构化 JSON；老格式降级提示 |
| `scripts/apply_layout.py` | 注入三层基础资产（布局骨架 + 可视化组件库 + 图表助手）；**生成骨架后必须调用**（`--no-chart` 可不注图表JS）|
| `scripts/apply_style.py` | 【重做路径】应用 19 种样式之一（复用 html-golive CSS 引擎，按 data-role 重排+套色）|
| `scripts/inherit_layout.py` | 【继承路径】保留源 HTML 原布局，只把 `--eh-*` 配色变量覆盖成主题色（不重排结构）；`--check` 校验契约 |
| `scripts/set_meta.py` | 幂等设置/替换 `<title>` 和 favicon |
| `scripts/make_favicon.py` | emoji/单字 → favicon SVG data URI（零依赖，可选） |
| `scripts/_engine.py` | CSS 主题引擎解析层（定位 html-golive 的 css_style_enhancer） |

## 依赖

- **Python** ≥ 3.8
- **[html-golive](https://github.com/Songhonglei/html-golive)**（`pip install html-golive`）——
  提供 19 套主题 CSS + data-role tagger + 可选的一键发布
  - 内部使用其 `css_style_enhancer` 的 4 个符号：`STYLE_MAP`（样式键表）、
    `load_css`（读 CSS）、`enhance`（打标+注入）、`FONT_PRELOADS`（字体预加载，缺失时自动跳过）
- **openpyxl**（可选，仅读 .xlsx 时需要）；.docx 用零依赖解析无需额外库

## 环境变量

| 变量 | 作用 | 默认 |
|---|---|---|
| `EASY_HTML_OUT` | 产物输出目录 | `./output/easy-html` |
| `EASY_HTML_CSS_ENGINE` | 直接指定 `css_style_enhancer.py` 路径 | 未设 |
| `EASY_HTML_GOLIVE_HOME` | html-golive 源码目录（未 pip 安装时） | 未设 |
| `window.EH_CHART_CDN` | （页面内 JS）自定义 Chart.js CDN 源列表 | 4 个公网源 |

## 边界（不做的事）

- ❌ 不做数据库查询 / BI 取数
- ❌ 不做纯数据看板可视化（那是看板工具的活）
- ❌ 不解析 .xls/.doc 老二进制格式（降级提示转格式）
- 专注「已有内容 → 排版成精美网页 → 发布」这一条线

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).
