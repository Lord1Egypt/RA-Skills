---
name: bii-blackrock-note
description: 把 BII 范式的个股研判简报（A4 横向 · 封面+9 正册+12 增补册 · 左文字栏+右图表栏）整体重定向为「贝莱德智库（BlackRock Investment Institute）风格」，并一条龙产出 pptx + pdf + html 三件套。核心能力：① 全局色板重定向（35 类源色 → 品牌令牌，含 7 槽分类色相保真）；② 结构装饰注入（左侧黑书脊 / 顶部黑色色带 / 品牌黄书签 / 黑色持仓面板 / 黄头摘要框 / 三段式「免责声明｜页码｜文件编号」页脚）；③ 装饰件零净增量约束——保证 22 页版式不被挤爆；④ 七门体检，含「可见文本逐字零改动」比对。Use when 用户要求「把这份个股简报做成贝莱德智库风格」「按贝莱德智库的版式出 pptx/pdf/html」「给 BII 简报换个品牌风格」，或需要把已有 BII HTML 交付成三格式。
homepage: https://github.com/yjkj999999/bii-blackrock-note
author: 王东杰 (Wang Dong Jie) · yjkj999999
license: MIT-0
version: 1.1.0
agent_created: true
read_when:
  - 用户要求把 BII / 个股简报做成贝莱德智库（BlackRock）风格
  - 用户要求某份 BII 简报同时交付 pptx + pdf + html
  - 用户说「换个品牌风格」「按这种版式再来一份」
  - 需要给已有 BII HTML 加品牌色带 / 书签 / 文件编号页脚
metadata:
  openclaw:
    emoji: 🖤
    version: "1.1.0"
---

> **版本谱系**：本技能自 v1.0.1 起**取代** `brand-pdf-deck-replica`（已退休）。
> 后者面向「复刻**外部**品牌 PDF + 反解图表数值」；本技能面向「自家 BII 简报换品牌皮 + 三格式交付」，
> 是把前者的**视觉体系与交付管线**并进 BII 内容引擎后的合并产物。两份并存会造成路由歧义，故只保留本技能。
>
> **v1.0.2**：把维护者发布脚本移出技能目录（分发载荷里不应有能改远端状态的工具）。
>
> **v1.1.0**：全要素研读贝莱德《2026年第四季度全球投资展望》（MKTG0926-M-5961218-EXP0927，
> 21 页，pdffonts + pdftotext + 逐页位图色彩量化三路交叉验证），固化为：
> ① 实测色板扩展 14 色（深黄/浅紫/桃橙阶/鲑鱼带/轴灰等，`br_tokens.json` 的 `bii2026q4` 块）；
> ② 14 组 28 形态图表范式库（信号面板表 / 点阵量尺 / 2×2 象限 / 到期墙 / IQR 分布 / 双语气泡地图等）；
> ③ 6 个 opt-in 品牌组件（估计区 / 状态徽章 / 观点量尺 / 象限图 / 三栏映射 / 分位带），
>    零净增量纪律不变、不进 `required_structures`。研读全文见 `docs/br2026q4_design_study.md`。

# BII 简报 × 贝莱德智库风格（内容不动 · 只换视觉体系）

产出：**同一份 22 页个股简报**，套上贝莱德智库的视觉语言，并同时交付 `pptx + pdf + html`。

本技能是「**内容引擎 + 视觉层**」的组合，不是从零画报告：

| 层 | 来自 | 职责 |
|---|---|---|
| 内容与版式骨架 | `bii-equity-note` | 22 页结构、双栏骨架、5 canvas + 12 SVG 图表、全部正文与数据 |
| 视觉体系 | 本技能 | 品牌令牌、结构装饰、三格式交付、七门体检 |

> **不要**用本技能生成一份新简报的内容。内容先由 `bii-equity-note` 出 HTML，再用本技能上妆。

## 依赖

| 依赖 | 用途 |
|---|---|
| `bii-equity-note` | 产出源 BII HTML（本技能的输入） |
| `html-to-pdf-cdp/scripts/render_html_pdf.sh` | CDP 出 PDF（含 canvas 墨量验收） |
| `html-to-pdf-cdp/scripts/measure_pages.js` | 由 `inspect_pages.sh` 调用，逐页量高度定位溢出 |
| poppler（`pdfinfo/pdftotext/pdftoppm`） | 页数尺寸核对、备注全文、位图铺底 |
| python-pptx + Pillow | PPTX 封装 |

## 资产与脚本

```
bii-blackrock-note/
  assets/
    br_tokens.json          # 品牌令牌 + 色板映射表 + bii2026q4 实测块（★单一来源，脚本一律从这里读）
    blackrock-theme.css     # 结构装饰层（不含映射表，只管新增装饰；v1.1.0 增 opt-in 品牌组件）
  scripts/
    theme_inject.py         # ① 色板重定向 + 装饰注入（三条硬断言）
    inspect_pages.sh        # ② 逐页版式体检（定位溢出页 + 可选截 PNG）
    mkpptx.py               # ④ PDF → PPTX（满幅位图 + 演讲者备注）
    check_br.py             # ⑤ 七门体检
    pipeline.sh             # 一条龙（①→⑥）
  docs/
    br2026q4_design_study.md  # ★ v1.1.0：《2026Q4 全球投资展望》全要素研读（色板/字体/骨架/28 形态图表范式/注记惯例）
  examples/
    sz001337_case.md        # 实跑记录（四川黄金 · 22 页）
```

## 图表范式库与品牌组件（v1.1.0 新增）

**范式库**（14 组 28 形态，源自 2026Q4 逐页解剖，明细见 `docs/br2026q4_design_study.md`）：
柱状+均线+阈值虚线 · 多系列线 · 堆积柱+空心柱(假设值) · 长周期占比堆积 · 含负值堆积柱 ·
对数尺度+趋势虚线+估计段 · 指数化多线(基准=100) · **信号面板表(状态徽章)** · **2×2 象限图** ·
Z-score 条形 · 七币种堆积柱 · 收益率曲线双日对比 · 水平占比堆积+大数字 · 双轴组合 ·
**到期墙前瞻堆积** · 配置梯度图 · **IQR/十分位距分布** · **三栏驱动映射表** ·
**点阵量尺(低配/中性/超配+早期观点空心点)** · **双语气泡资产地图(中英对照)** · 战术观点表 …

**opt-in 品牌组件**（`blackrock-theme.css` 第六节，源稿显式用 class 才生效，不影响门禁）：

| class | 对应 2026Q4 范式 | 用法 |
|---|---|---|
| `.br-est` | 估计段（p7/p15） | 预测区容器：浅黄底+左虚线界+右上角「估计」角标 |
| `.br-sig` (+`-pos`/`-watch`) | 信号徽章（p8） | 乐观=黄底实心；观察中=描边 |
| `.br-gauge` (+`.early`) | 观点量尺（p17/19/20） | 低配—中性—超配轨道点；`.early`=早期观点空心点 |
| `.br-quad` (+`.c-*`) | 2×2 象限（p9） | 虚线十字中线；气泡按分类槽上色 |
| `.br-map3` (+`.t-*`) | 三栏驱动映射（p16） | 左主题卡彩色左规（inset 阴影，零层高） |
| `.br-iqr` (+`.br-iqr-med`) | 分位带（p15） | 鲑鱼色带 `#FFB5A1` + 中值黑线 |

**注记语法**（给内容引擎 `bii-equity-note` 的对齐约定）：估计段标注「估计」；免责前缀三态
（前瞻性估计可能不会实现 / 所示数据仅代表过往表现 / 仅供说明）；资料来源句式
`资料来源：贝莱德智库、[机构]，数据来自 [Haver Analytics|LSEG Datastream|彭博|…]，YYYY年M月。`；
指数化比较注明基准时点（=100）；空心柱=假设值、虚线=估计/阈值、浅带=分位区间。

---

## 一条龙（最常用）

```bash
bash ~/.workbuddy/skills/bii-blackrock-note/scripts/pipeline.sh \
  ~/Desktop/bii_sz001337_20260917.html \
  ./out
# → out/bii_sz001337_20260917_blackrock.{html,pdf,pptx}
```

分步执行见下。

## 步骤 1 · 注入（色板重定向 + 结构装饰）

```bash
PY=~/.workbuddy/binaries/python/envs/default/bin/python     # 需要 python-pptx
$PY ~/.workbuddy/skills/bii-blackrock-note/scripts/theme_inject.py \
  src.html out.html --report inject.json
```

做两件事，**其余字节不变**：

**① 全局色板重定向**（35 类源色，作用于 CSS / 内联样式 / SVG fill / canvas JS 全区域）

| 源色 | → 品牌色 | 语义 |
|---|---|---|
| `#FFB500` | `#FFCE00` | 品牌黄（贝莱德第一识别色） |
| `#C62828` | `#CE2A0A` | 涨 / 品牌红 |
| `#2E7D32` | `#00704A` | 跌 / 品牌绿 |
| `#2E6FAF` | `#3F6FA6` | 分类槽·钢蓝 |
| `#2E9E8F` | `#008B5C` | 分类槽·绿 |
| `#E07B39` | `#E8892B` | 分类槽·橙（MA5） |
| `#8E44AD` | `#9062BC` | 分类槽·紫（MA60） |
| `#FBE8C4 / #FAC775 / #EF9F27` | `#FFF3C4 / #FDDC6B / #F5C518` | 热力图暖色阶 |
| …（其余 27 类见 `br_tokens.json`） | | |

**② 结构装饰注入**

- `data-br-tab` 属性 → 每页顶部**品牌黄书签**（文案自动取页眉 `.rh-l`）
- `<span class="br-code">` → 每页页脚**文件编号**（自动读源件的「报告编号」，拼成 `BII-<报告编号>`）
- 封面品牌行改写 + 封面页脚加**版式来源声明**
- 主题 CSS 注入 `</head>` 之前

**三条硬断言**（不满足直接非零退出，不留半成品）：section 数 == 期望页数；每个页脚恰好 2 个 `<span>`；注入后无源色残留。

## 步骤 2 · 逐页版式体检（★装饰件最容易在这一步翻车）

```bash
bash ~/.workbuddy/skills/bii-blackrock-note/scripts/inspect_pages.sh out.html [png目录]
```

> 本脚本是**薄委托**，实际执行 `html-to-pdf-cdp/scripts/measure_pages_selfhost.sh`
> （Chrome 必须起在**同一个前台进程**里——受限沙箱会回收后台常驻 Chrome，
> 直接跑 `measure_pages.js` 会报 `fetch failed`）。

输出 `over` 列即「超出纸高多少」。**A4 横向的溢出阈值是 794px**（210mm）。
源稿通常刚好卡在 793.7px（= `min-height:210mm`），所以**任何正增量都会让那页多出一张纸**。

### 装饰件零净增量铁律（v1.0.0 血泪）

在一份 22 页源稿上首次注入时，三页溢出（+16.2 / +7.4 / +7.4px）。原因是装饰件引入了**行盒**：

| 坑 | 症状 | 正解 |
|---|---|---|
| **`display:inline-block` 胶囊标签** | 单这一项就 +7px | 行盒高 = `max(父级 strut, 标签高)`，父级 strut = 10.5px×1.66 ≈ 17.4px，远高于标签本身。**保持 `display:block` + `width:fit-content`** |
| **页脚改两行网格** | 每页 +4.5px | 文件编号改 `position:absolute; top:100%`，落进页面下内边距，行数不变 |
| **给块加 `border-bottom`/`padding-bottom`** | 每个块 +4px（3 个块 +12px） | 只改颜色，不加边线；或用 `box-shadow: inset` 代替真实边框 |

净效果：22 页全部回到 793.7px，`colL` 甚至比源稿小 4~6px。

> **不要**靠缩字号或减内边距去硬塞。先按上表把装饰件做成零增量。

## 步骤 3 · 出 PDF

```bash
bash ~/.workbuddy/skills/html-to-pdf-cdp/scripts/render_html_pdf.sh out.html out.pdf 3200 css
```

**不要加 `SKIP_VERIFY=1`**：本版面有 5 个 canvas，脚本自带的墨量验收是有效的真门（`ratio` 应落在 0.03~0.7）。

## 步骤 4 · 封 PPTX

```bash
~/.workbuddy/binaries/python/envs/default/bin/python \
  ~/.workbuddy/skills/bii-blackrock-note/scripts/mkpptx.py out.pdf out.pptx 200
```

- 幻灯片尺寸**自动探测** PDF 首页尺寸（本例 841.92×594.96pt = 11.69×8.26in），1:1 不缩放
- 每页 **200dpi 位图满幅铺底** —— 自绘 SVG/canvas 图表无法用 python-pptx 原生表达
- 每页写入**演讲者备注**（`pdftotext` 全文，剔除页脚固定件）→ PPTX 仍可检索、可复制文字
- **交付时必须向用户说明这一取舍**：要改字请改 HTML 重出，不要试图在 PPT 里改

## 步骤 5 · 七门体检

```bash
$PY ~/.workbuddy/skills/bii-blackrock-note/scripts/check_br.py out.html \
  --src src.html --pdf out.pdf --pptx out.pptx --pages 22
```

| # | 门 | 判据 |
|---|---|---|
| 1 | 结构完整性 | section 数 == 书签数 == 页脚编号数 == 期望页数 |
| 2 | 品牌令牌/装饰结构 | `br_tokens.json` 的 `required_structures` 全部命中 |
| 3 | 源色板无残留 | `forbidden_after_inject`（`#FFB500/#C62828/#2E7D32`）计数为 0 |
| 4 | 分类色相可区分 | 7 槽分类色一个不少（防止色相塌缩） |
| 5 | **内容零改动** | 可见文本词元多重集比对：产物只允许多出「本次注入的文案词元」 |
| 6 | PDF 页数/尺寸 | 页数 == 22；`841.92×594.96pt` |
| 7 | PPTX 结构 | 页数、宽高、每页恰 1 张图、备注非空 |

**门 5 是本技能的核心价值**。它把「只换视觉、不动内容」从口号变成可执行判据：任何正则误伤正文或图表脚本都会被它抓住。
白名单**不写死**，而是从 DOM 反推本次真正注入了什么（品牌行 / 风格声明 / 页脚编号）——
写死白名单只会掩盖真正的注入事故（v1.0.0 就是这么误报的）。

## 交付

用 `present_files` 一次给出：**PDF（第一顺位）→ PPTX → HTML**，并附上七门体检结果。
正文里必须带上：标的、报告期、**版式来源声明**（本报告为独立分析件，非贝莱德公司出品），以及免责声明。

---

## 常见故障速查

| 症状 | 根因 | 处置 |
|---|---|---|
| PDF 页数 > section 数 | 装饰件把某页挤爆 | `inspect_pages.sh` 看 `over` 列，按「零净增量铁律」改 CSS |
| 色板映射后两个系列色看起来一样 | 7 槽分类色塌缩成 5 色 | 查 `br_tokens.json` 的 `_categorical_note`；分类槽必须保留独立色相 |
| 胶囊标签一加就溢出 | `display:inline-block` 撑高行盒 | 改 `display:block; width:fit-content` |
| 页脚文件编号被裁掉 | 绝对定位超出页面下内边距 | 确认 `.page{padding-bottom}` ≥ 8mm；`top:100%` 落点应在内边距内 |
| 注入后 PDF 还是旧版面 | Chrome 复用旧 profile | 用 `render_html_pdf.sh` 自起模式（每次全新 profile） |
| 后台起 Chrome 量页面失败 | 沙箱回收后台进程 / GPU 进程 FATAL | 用 `inspect_pages.sh`——它把 Chrome 放在**同一个前台进程**里并 trap 收尾 |
| 门 5 报「产物多出非注入词元」 | 正则误伤正文，或注入文案改了没更新白名单 | 看 `bad_extra` 具体词元；**不要**直接放宽白名单 |
| 图表全白 | HTML 里没写进图表，或脚本被破坏 | grep 产物 HTML 的 `<canvas>`/`<svg>` 数量应与源件一致 |

## 与其他技能的关系

- 上游：`bii-equity-note`（出内容）→ 本技能（上妆 + 三格式交付）
- 已被本技能取代：`brand-pdf-deck-replica`（v1.0.1 起退休，已从 ClawHub 下架）——
  其「复刻外部品牌 PDF + 反解图表数值」的能力未并入本技能，如需该能力请从
  GitHub 历史版本取用，不要再与本技能并列挂在技能根目录下。
- 下游：`present_files` 交付

## 发布（维护者用）

本技能**不自带发布脚本**。维护者工具放进来有三个坏处，v1.0.1 三个都中了：

1. 每个安装者都会被 ClawHub 安全审计判为 `Review`（「ships a live maintainer publishing script that can mutate ClawHub and GitHub state」）；
2. 本地副本只要领先于已发布版本，就会把**旧修订**当新版发出去（v1.0.1 发出去的 `publish.sh` 是修复前的坏版本，含 2 处 `unbound variable`）；
3. 分发载荷里多一份与使用者无关的危险工具。

统一改用通用发布器：

```bash
export GITHUB_TOKEN=ghp_xxx      # 只用于建仓/查仓；绝不落盘
bash ~/.workbuddy/skills/skill-publish-clawhub-github/scripts/publish_skill.sh \
  --dir ~/.workbuddy/skills/bii-blackrock-note \
  --slug bii-blackrock-note \
  --name "BII 简报 × 贝莱德智库风格（pptx+pdf+html 三格式）" \
  --version <新版本号> \
  --gh-repo bii-blackrock-note \
  --go
```

不加 `--go` 是干跑（体检 + 打印动作）。

| 渠道 | 标识 | 说明 |
|---|---|---|
| ClawHub | `bii-blackrock-note` | 作者 `yjkj999999` |
| GitHub | `yjkj999999/bii-blackrock-note` | SSH 推送；GitHub API 调用必须 `--noproxy '*'` |

> **改动完必须复读校验**：同一条消息里对同一文件并行发两个 Edit 会互相覆盖，工具仍报 success。
> v1.0.1 的 frontmatter 就是这样静默丢失的。

## 本地许可

MIT-0 · Copyright (c) 2026 王东杰 (Wang Dong Jie) · yjkj999999
