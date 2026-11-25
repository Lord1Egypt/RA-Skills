<!-- 本文件由 scripts/docgen.py 生成(来源=各命令 --help 实跑输出)。
     手改无效;改文档请改引擎 help 文案后重跑 docgen;新鲜度由 release_check C4 校验 -->

# 命令全量参考(自动生成)

> 决策表(10 秒选对命令)在 SKILL.md/SKILL_ZH.md;本文件=全量 flags 参考。

## palette_forge audit

> 外部页面机械体检(漂移带替换值/禁渐变/对比对/字号/AI 签名)

```
usage: palette_forge.py audit [-h] [--palette PALETTE] [--floor FLOOR]
                              [--out OUT]
                              page

positional arguments:
  page               外部页面 HTML

options:
  -h, --help         show this help message and exit
  --palette PALETTE  声明色板(给出即查漂移)
  --floor FLOOR      字号下限 px
  --out OUT          JSON 输出前缀
```

## palette_forge blind

> 盲评对比页(双盲候选,防先入为主)

```
usage: palette_forge.py blind [-h] --palette PALETTE
                              [--kind {protanopia,deuteranopia,tritanopia}]

options:
  -h, --help            show this help message and exit
  --palette PALETTE
  --kind {protanopia,deuteranopia,tritanopia}
```

## palette_forge card

> 单卡片样机(结构化信息卡)

```
usage: palette_forge.py card [-h] --palette PALETTE [--name NAME] [--out OUT]

options:
  -h, --help         show this help message and exit
  --palette PALETTE
  --name NAME
  --out OUT
```

## palette_forge chartpal

> 图表配色三型(分类/顺序/发散,色盲模拟验证)

```
usage: palette_forge.py chartpal [-h] --kind
                                 {categorical,sequential,diverging}
                                 [--palette PALETTE] [--theme THEME]
                                 [--series SERIES] [--reverse] [--name NAME]
                                 [--canvas CANVAS] [--out OUT]

options:
  -h, --help            show this help message and exit
  --kind {categorical,sequential,diverging}
  --palette PALETTE     候选色(分类≥2;发散=两端色)
  --theme THEME         主题包名(与 --palette 二选一)
  --series SERIES       系列数(2-12)
  --reverse             顺序板浅→深反转
  --name NAME
  --canvas CANVAS       目标画布 hex(默认 FFFFFF;系列色对画布 <3.0:1 降级,<1.5:1 FAIL)
  --out OUT             输出前缀(默认 chartpal)
```

## palette_forge check-image

> 图片审查(尺寸/格式/文字安全)

```
usage: palette_forge.py check-image [-h] [--n N] image

positional arguments:
  image       图片路径(封面/截图)

options:
  -h, --help  show this help message and exit
  --n N       取色数,默认 5
```

## palette_forge contrast

> 两色对比度查询(带判据说明)

```
usage: palette_forge.py contrast [-h] --fg FG --bg BG [--large]
                                 [--method {wcag,apca}]

options:
  -h, --help            show this help message and exit
  --fg FG
  --bg BG
  --large               large text threshold 3:1
  --method {wcag,apca}  apca=WCAG3 草案感知算法
```

## palette_forge critique

> 整页审美批评(按法则集逐条点名)

```
usage: palette_forge.py critique [-h] [--palette PALETTE]
                                 [--evidence EVIDENCE] [--out OUT]

options:
  -h, --help           show this help message and exit
  --palette PALETTE
  --evidence EVIDENCE  render_probe 采集的 evidence.json
  --out OUT
```

## palette_forge direct

> 整页配色机械度量(温度旅程/饱和曲线/主色戏剧;--render 渲染事实)

```
usage: palette_forge.py direct [-h] [--zones ZONES] [--manifest MANIFEST]
                               [--page PAGE] [--bold] [--render RENDER]

options:
  -h, --help           show this help message and exit
  --zones ZONES        hex:share,hex:share,...
  --manifest MANIFEST  lab_zones.json 批量裁决
  --page PAGE          页面名(写入报告头)
  --bold               品牌页(大域准入)
  --render RENDER      render_probe.js 采集的 evidence.json(zones 来自渲染像素,渲染事实审计)
```

## palette_forge directions

> 跨语域方向探索

```
usage: palette_forge.py directions [-h] [--brief BRIEF]
                                   [--registers REGISTERS] [--n N]
                                   [--out-dir OUT_DIR]

options:
  -h, --help            show this help message and exit
  --brief BRIEF         需求自然语言,如:素雅耐看的落地页
  --registers REGISTERS
                        逗号分隔语域,显式指定时跳过 brief
  --n N                 方向数 2-4
  --out-dir OUT_DIR
```

## palette_forge doctor

> 环境自检(依赖/字体/浏览器探活)

```
usage: palette_forge.py doctor [-h]

options:
  -h, --help  show this help message and exit
```

## palette_forge evidence

> 页面证据卷宗:静态 lint + 四闸合成 JSON+人读 HTML

```
usage: palette_forge.py evidence [-h] --palette PALETTE [--render RENDER]
                                 [--out OUT]
                                 page

positional arguments:
  page               已完成的页面 HTML

options:
  -h, --help         show this help message and exit
  --palette PALETTE  声明色板,逗号分隔 hex
  --render RENDER    render_probe.js 采集的 evidence.json(可选)
  --out OUT          输出前缀(默认 <page>.evidence)
```

## palette_forge exemplar

> 范例库检索注入(渲染评审过的成页样例)

```
usage: palette_forge.py exemplar [-h] [--kind KIND] [--register {light,dark}]
                                 [--list]

options:
  -h, --help            show this help message and exit
  --kind KIND           页面类型: landing/tech-landing/poster/editorial/narrative
  --register {light,dark}
                        明暗语域
  --list                只列范例目录
```

## palette_forge export

> 导出(ASE/JSON/图片)

```
usage: palette_forge.py export [-h] --palette PALETTE
                               [--format {css,tailwind,json,svg,w3c,context,prompt}]

options:
  -h, --help            show this help message and exit
  --palette PALETTE
  --format {css,tailwind,json,svg,w3c,context,prompt}
```

## palette_forge extract

> 从图片提取色板(聚类+去脏)

```
usage: palette_forge.py extract [-h] [--n N] image

positional arguments:
  image

options:
  -h, --help  show this help message and exit
  --n N
```

## palette_forge harmony

> 配色和谐度量(半径/跨度)

```
usage: palette_forge.py harmony [-h] --base BASE
                                [--mode {monochromatic,analogous,complementary,split-complementary,triadic,tetradic,square}]
                                [--theme {light,dark}] [--count COUNT]

options:
  -h, --help            show this help message and exit
  --base BASE
  --mode {monochromatic,analogous,complementary,split-complementary,triadic,tetradic,square}
  --theme {light,dark}
  --count COUNT
```

## palette_forge house

> 风格板(整页风格预览)

```
usage: palette_forge.py house [-h] --name NAME --hexes HEXES
                              [--from-proj FROM_PROJ]

options:
  -h, --help            show this help message and exit
  --name NAME
  --hexes HEXES
  --from-proj FROM_PROJ
                        来源项目名
```

## palette_forge loop

> 渲染评审闭环清单(截图三铁律/qc 对账/五镜/停止条件)

```
usage: palette_forge.py loop [-h] --palette PALETTE [--floor FLOOR] [--bg BG]
                             [--out OUT]
                             page

positional arguments:
  page               页面 HTML

options:
  -h, --help         show this help message and exit
  --palette PALETTE  声明色板,逗号分隔 hex
  --floor FLOOR      字号下限 px
  --bg BG            声明大底 hex(qc 对账用)
  --out OUT          检查单输出路径(默认 <page>.loop.md)
```

## palette_forge match

> 按 brief 出配色(排序主键=得分,所见即所排)

```
usage: palette_forge.py match [-h] --brief BRIEF
                              [--register {medical_teaching,pediatric_cover,frontend_soft,frontend_deep,frontend_bold,frontend_tech,frontend_heritage}]
                              [--no-flags] [--limit LIMIT]

options:
  -h, --help            show this help message and exit
  --brief BRIEF         需求自然语言,如:儿科教学页/素雅落地页/母婴封面
  --register {medical_teaching,pediatric_cover,frontend_soft,frontend_deep,frontend_bold,frontend_tech,frontend_heritage}
  --no-flags
  --limit LIMIT
```

## palette_forge matrix

> 主题色板矩阵(跨主题一次性看全)

```
usage: palette_forge.py matrix [-h] --palette PALETTE [--recommend]
                               [--method {wcag,apca}]

options:
  -h, --help            show this help message and exit
  --palette PALETTE
  --recommend
  --method {wcag,apca}  apca=WCAG3 草案感知算法
```

## palette_forge mutate

> 色板变异(单维扰动生成近亲板)

```
usage: palette_forge.py mutate [-h] --palette PALETTE [--shade SHADE]
                               [--sat SAT] [--hue HUE] [--temp TEMP]
                               [--lum LUM]

options:
  -h, --help         show this help message and exit
  --palette PALETTE
  --shade SHADE      -100..100 darken/lighten
  --sat SAT          -100..100 chroma delta
  --hue HUE          hue rotate degrees
  --temp TEMP        -100..100 cool..warm
  --lum LUM          -100..100 lightness delta
```

## palette_forge narrate

> 把实测闸门转成双语纯数字说明

```
usage: palette_forge.py narrate [-h] [--palette PALETTE] [--theme THEME]
                                [--name NAME] [--dark] [--out OUT]

options:
  -h, --help         show this help message and exit
  --palette PALETTE  色板,逗号分隔 hex
  --theme THEME      主题包名(与 --palette 二选一)
  --name NAME        板名(写入标题)
  --dark             按暗底推导角色
  --out OUT          输出 md 路径
```

## palette_forge patch

> 把审计结果变成字面替换对(--apply 直修并复检)

```
usage: palette_forge.py patch [-h] [--palette PALETTE] [--floor FLOOR]
                              [--apply] [--out OUT]
                              page

positional arguments:
  page               页面 HTML

options:
  -h, --help         show this help message and exit
  --palette PALETTE  声明色板(给出即查漂移)
  --floor FLOOR      字号下限 px
  --apply            备份 .bak 后应用机械补丁并复检
  --out OUT          补丁清单 JSON 输出路径
```

## palette_forge qc

> 截图对账(大底真伪/板外入侵带,渲染实况=声明)

```
usage: palette_forge.py qc [-h] [--tokens TOKENS] [--palette PALETTE]
                           [--bg BG] [--out OUT]
                           image

positional arguments:
  image              渲染截图 PNG

options:
  -h, --help         show this help message and exit
  --tokens TOKENS    tokens.json(令牌对账)
  --palette PALETTE  声明色板,逗号分隔 hex
  --bg BG            声明大底 hex(色板模式建议显式给)
  --out OUT          JSON 输出路径
```

## palette_forge ramp

> 单色明度坡(语义档生成)

```
usage: palette_forge.py ramp [-h] --base BASE [--steps STEPS]
                             [--direction {light,dark}]

options:
  -h, --help            show this help message and exit
  --base BASE           seed hue/lightness source
  --steps STEPS
  --direction {light,dark}
                        light: dark->light ramp; dark: light->dark
```

## palette_forge report

> 四道机械闸评分(可挂第五闸 drama)

```
usage: palette_forge.py report [-h] [--zones ZONES] [--bold] --palette PALETTE

options:
  -h, --help         show this help message and exit
  --zones ZONES      页面区域占比 hex:share,...(给出即加第五闸 drama)
  --bold             品牌页(drama 准入放宽)
  --palette PALETTE
```

## palette_forge roles

> OKLCH 角色派生(60-30-10+语义档)

```
usage: palette_forge.py roles [-h] --palette PALETTE [--theme {light,dark}]
                              [--css] [--semantic]

options:
  -h, --help            show this help message and exit
  --palette PALETTE
  --theme {light,dark}
  --css
  --semantic            derive success/warning/error/info from accent hue
```

## palette_forge scaffold

> 整页起点(五配方+AUTO 明暗路由)

```
usage: palette_forge.py scaffold [-h] [--theme THEME] [--palette PALETTE]
                                 [--recipe RECIPE]
                                 [--fonts {none,preset,auto}] [--brand BRAND]
                                 [--brand-en BRAND_EN] [--use-when USE_WHEN]
                                 [--out OUT]

options:
  -h, --help            show this help message and exit
  --theme THEME         主题包 name_en/name,如 Deep Pine
  --palette PALETTE     逗号分隔 hex(无主题时用)
  --recipe RECIPE       布局配方: AUTO(默认,按色板气质路由)/DARK-FOUR-ACT/EDIT-
                        SPLIT/BLUEPRINT/SWISS-POSTER/EDITORIAL-MAG
  --fonts {none,preset,auto}
                        字体资产: none(系统栈,禁 900)/preset(随包子集)/auto(现场子集,缺
                        fontTools 降级 preset)
  --brand BRAND         品牌名(默认取主题)
  --brand-en BRAND_EN
  --use-when USE_WHEN
  --out OUT             输出路径
```

## palette_forge scene

> 单场景样机(wallet/dashboard/landing…)

```
usage: palette_forge.py scene [-h] --kind KIND [--theme THEME]
                              [--palette PALETTE] [--name NAME] [--dark]
                              [--force] [--out OUT]

options:
  -h, --help         show this help message and exit
  --kind KIND        wallet/landing/dashboard/branding/typography/chart/ecom/e
                     mail/editorial/pattern
  --theme THEME      主题包 name_en/name
  --palette PALETTE  逗号分隔 hex(无主题时)
  --name NAME        色板显示名(默认取主题名)
  --dark
  --force            越过 AI 默认紫守门(留痕)
  --out OUT          输出路径
```

## palette_forge score

> 四闸评分明细

```
usage: palette_forge.py score [-h] --palette PALETTE

options:
  -h, --help         show this help message and exit
  --palette PALETTE
```

## palette_forge search

> 库内检索(brief/标签直达)

```
usage: palette_forge.py search [-h] [--style STYLE] [--min-likes MIN_LIKES]
                               [--no-flags] [--limit LIMIT]

options:
  -h, --help            show this help message and exit
  --style STYLE         comma list: warm,cool,dark,light,mid,pastel,vivid,mono
                        chromatic,multihue,deep
  --min-likes MIN_LIKES
  --no-flags            exclude palettes carrying any gate flag
  --limit LIMIT
```

## palette_forge selftest

> 引擎自测(结构不变量)

```
usage: palette_forge.py selftest [-h]

options:
  -h, --help  show this help message and exit
```

## palette_forge semantic

> 已并入 chartpal(兼容别名)

```
usage: palette_forge.py semantic [-h] [--count COUNT] [--base BASE]
                                 [--hue HUE]

options:
  -h, --help     show this help message and exit
  --count COUNT  deprecated: 图表/分类用色已并入 chartpal --kind categorical,本命令仅保留兼容
  --base BASE    基准色(取其色相)
  --hue HUE      无 --base 时的起始色相
```

## palette_forge showcase

> 场景图墙(多场景拼版)

```
usage: palette_forge.py showcase [-h] [--style STYLE] [--min-likes MIN_LIKES]
                                 [--limit LIMIT] [--out OUT]

options:
  -h, --help            show this help message and exit
  --style STYLE         comma list of style tags
  --min-likes MIN_LIKES
  --limit LIMIT
  --out OUT
```

## palette_forge slop

> 反俗套扫描(tailwind 默认/紫域/玻璃拟态)

```
usage: palette_forge.py slop [-h] --palette PALETTE

options:
  -h, --help         show this help message and exit
  --palette PALETTE
```

## palette_forge theme

> 单主题详情(色板+角色)

```
usage: palette_forge.py theme [-h] [--format {css,json}] name

positional arguments:
  name                 主题名(中文或英文)

options:
  -h, --help           show this help message and exit
  --format {css,json}
```

## palette_forge themes

> 主题清单(库内全部已验证主题)

```
usage: palette_forge.py themes [-h] [--json]

options:
  -h, --help  show this help message and exit
  --json
```

## palette_forge tokens

> 设计令牌表(CSS 变量+JSON,含动效令牌)

```
usage: palette_forge.py tokens [-h] [--palette PALETTE] [--theme THEME]
                               [--name NAME] [--brand BRAND] [--dark]
                               [--contrast {standard,high}] [--out OUT]

options:
  -h, --help            show this help message and exit
  --palette PALETTE     色板,逗号分隔 hex
  --theme THEME         主题包名(与 --palette 二选一)
  --name NAME           令牌表名(写入注释头)
  --brand BRAND         品牌名(写入注释)
  --dark                深色为主(令牌明暗互换)
  --contrast {standard,high}
                        对比度旋钮(0.29):standard=WCAG 4.5+APCA Lc
                        60/90;high=7.0+Lc 75/95(AAA 向)
  --out OUT             输出前缀(默认 tokens)
```

## palette_forge typescale

> CJK 字阶(--fluid 流体+排印底座)

```
usage: palette_forge.py typescale [-h] [--base BASE] [--ratio RATIO]
                                  [--floor FLOOR] [--fluid] [--name NAME]
                                  [--out OUT]

options:
  -h, --help     show this help message and exit
  --base BASE    正文字号 px
  --ratio RATIO  等比(1.125-1.5)
  --floor FLOOR  字号硬下限 px
  --fluid        display 级发流体 clamp(375-1440px 线性)
  --name NAME
  --out OUT      输出前缀(默认 typescale)
```

## palette_forge visualize

> 可视化样机(dashboard/编辑器等)

```
usage: palette_forge.py visualize [-h] --palette PALETTE [--name NAME]
                                  [--theme {light,dark}] [--svg SVG]
                                  [--variants VARIANTS] [--shuffle SHUFFLE]
                                  [--out OUT]

options:
  -h, --help            show this help message and exit
  --palette PALETTE
  --name NAME
  --theme {light,dark}
  --svg SVG             对其做重着色(纯黑白保留)
  --variants VARIANTS   同场景 N 次色板排列对比(旋转+反转)
  --shuffle SHUFFLE     --svg 重着色排列数(含对比网格页)
  --out OUT
```

## lint_page.py

> lint_page — HTML 交付前静态审计(色板漂移/字号/渐变/emoji/渲染证据)

```
usage: lint_page.py [-h] [--palette PALETTE] [--floor FLOOR]
                    [--max-grad MAX_GRAD] [--lenient] [--render RENDER]
                    page

positional arguments:
  page

options:
  -h, --help           show this help message and exit
  --palette PALETTE    声明的色板,逗号分隔 hex;缺省时自动读被检 HTML 里的 meta name=aesthete-
                       palette 板声明(引擎产物自带)
  --floor FLOOR        字号下限 px(投影件建议 24-34)
  --max-grad MAX_GRAD  渐变容量(默认 0=禁渐变)
  --lenient            过渡口径:P1 需 >=2 条才红(夜间先跑;默认严:单条 P1 即红)
  --render RENDER      render_probe.js 采集的 evidence.json
```

## make_variants.py

> make_variants — 送审对比页

```
usage: make_variants.py [-h] [--labels LABELS [LABELS ...]] [--cards CARDS]
                        [--out OUT]
                        pages [pages ...]

positional arguments:
  pages                 候选页面(≥2)

options:
  -h, --help            show this help message and exit
  --labels LABELS [LABELS ...]
                        每个候选的名字
  --cards CARDS         元数据 JSON(与 pages 一一对应)
  --out OUT
```

