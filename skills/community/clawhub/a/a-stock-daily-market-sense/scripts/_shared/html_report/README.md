# shared/html_report

仓库级 HTML 报告渲染框架。各报告型 skill 把 Markdown 研报 + JSON 证据包套成一份自包含的单页 HTML(图表不依赖外部 CDN)。

设计目标:**新 skill 出 HTML 只写一张"薄清单"**——怎么读自己的数据、画哪几张图——其余(命令行、Markdown→HTML、主题、校验、图表工具、染色/hero 装饰)全部由本包提供。

## 一张薄清单长什么样

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "_shared"))

from html_report import (
    HtmlReportBuilder, ChartHook, RenderJob,
    render_report, PillDecoration, HeroDecoration,
)

def add_arguments(parser):                 # 可选:本 skill 额外的命令行参数
    parser.add_argument("--evidence", default=None)

def build_job(args) -> RenderJob:          # 唯一要写的:读数据 + 选图表
    md = Path(args.input).read_text(encoding="utf-8")
    evidence = load_my_evidence(args.evidence)        # 域:自己的 evidence schema
    charts = extract_my_payload(evidence)             # 域:整形成 JS 好用的 payload
    builder = HtmlReportBuilder(title=args.title or Path(args.input).stem,
                                theme=args.theme, meta_text="…")
    builder.add_decoration(PillDecoration(MY_PILL_RULES))   # 词表是数据
    builder.add_decoration(HeroDecoration(heading_prefix="核心判断"))
    builder.add_chart_hook(ChartHook(name="my-charts", payload=charts, js=MY_CHARTS_JS))
    out = Path(args.output) if args.output else Path(args.input).with_suffix(".html")
    return RenderJob(markdown_text=md, builder=builder, output_path=out,
                     summary={"…": "打印到 stdout 的诊断字段"})

if __name__ == "__main__":
    raise SystemExit(render_report(
        description="Render … to static HTML.",
        build_job=build_job, add_arguments=add_arguments))
```

`render_report` 统一负责:解析 `--input/--output/--title/--theme/--no-validate/--strict`、读 Markdown、跑 `build_job`、以"校验失败转 warning 不阻断"的策略渲染(`--strict` 才硬失败)、写文件、打印 JSON 摘要、把异常收成 `error: …` + 退出码 1。

## 四层结构

| 层 | 模块 | 职责 |
|---|---|---|
| CLI | `cli.py` | `render_report` / `RenderJob`,吃掉每个 skill 重复的 argparse + main 编排 |
| 装饰 | `decorations.py` | `PillDecoration` / `HeroDecoration` / `CollapsibleUpdatesDecoration` / `TimelineDecoration`,数据驱动,机制只一份 |
| 图表 | `chartkit.js` (`window.CK`) + `ChartHook` | 共享 SVG/DOM 工具 + 各 skill 自带的画图 JS |
| 外壳 | `builder.py` `markdown_engine.py` `text_validator.py` `themes/` | HTML 骨架、Markdown→HTML、文本保全校验、CSS 主题 |

## 装饰:换词表不换代码

```python
PillDecoration(rules=[(r"^(成长股|成熟龙头)$", "pill"),
                      (r"^(强|高)$", "pill neg")])          # 表格单元格按正则染成 pill
HeroDecoration(heading_prefix="一句话盘面判断",
               collect_tags=("P",), max_blocks=3,
               stop_at_numbered=True, number_units="%|pct|倍",
               keyword_pattern="上证|创业板|科创50")          # 把摘要标题升格成 hero 卡
CollapsibleUpdatesDecoration()      # ## 更新 YYYY-MM-DD：摘要 → 折叠卡(默认最新展开)
TimelineDecoration()                # 顶部 日期|版本号 表 + 文末 版本变更记录 表 → 可点版本时间轴
```

活报告(同一报告随时间多轮更新)用后两个装饰:更新章节折叠成带日期徽标 + 一句话摘要的卡片(id 为 `upd-<date>`,供其它组件跳转),两张版本表合成一条时间轴(节点弹出该版本主要变更/关键数字,可跳转对应更新卡;时间轴挂上后隐藏顶部两列表,不足 2 个版本不动作)。**添加顺序**:CollapsibleUpdates 在 Hero 之前(hero 收集遇 section/aside/blockquote 停止,不会吞卡),Timeline 在两者之后。带 `.css` 的装饰由 `add_decoration` 自动合并样式。

裸 JS 逃生舱仍在:`builder.add_ui_decoration(js_string)`。

## 结构化 callout 块

`markdown_engine` 认识注册在 `_STRUCTURED_BLOCKS` 的多行块——`==深度调研发现｜徽标A｜徽标B` 与 `==跟踪事项｜ID｜类型｜状态：…`(以 `==` 行收尾),渲染成 `<aside class="<prefix>-card">`(头部徽标 + `标签：值` 行)。卡片 CSS 由使用该块的 skill 随 `extra_css` 提供;行内 `==文字==` 渲染成 `<mark>`。

## 图表工具 `window.CK`

builder 在有 ChartHook 时,自动在 base-UI 脚本之后、各 hook IIFE 之前注入一次 `chartkit.js`,暴露 `window.CK`。hook JS 不再各自重定义 `svgEl`,直接用:

- `CK.svgEl(name, attrs)` / `CK.svgText(x, y, text, anchor, color, size)`
- `CK.fmt.date(v)` / `CK.fmt.num(v, d)` / `CK.fmt.signedPct(v)` / `CK.num(v)`
- `CK.tooltip(card)` / `CK.moveTip(tip, card, e)`
- `CK.card(cls, title, sub)` / `CK.legend([[label, color], …])` / `CK.grid(cls)`
- `CK.metricGrid([{title, value, subtitle, signValue}, …])` / `CK.metricCard(spec)` —— KPI / 指标卡,样式在 theme 里
- `CK.horizontalBarCard({title, subtitle, rows:[{label, value, meta}], maxRows})` —— 通用横向涨跌条,样式在 theme 里
- `CK.findHeading(root, texts[, sel])` / `CK.findNextTable(heading)` / `CK.insertAfter(root, texts, node)`

通用图表类型和 CSS 放在 shared；skill 独有的格式化(价格精度、亿/万亿 除数)、字段映射和"画哪些行"仍留在各自 hook 里,因为这些是领域判断。

### ChartHook JS 协议

每个 hook 的 JS 在专属 IIFE 中执行,渲染器自动注入:

- `__payload` — 当前 hook 的 payload(已经 JSON.parse)
- `window.__chartData` — 整个 envelope `{ hookName: payload, … }`,供跨 hook 取数

## 主题

- `default`:AlphaVault 站点风格(Google Material)——冷白底 + Google 蓝 + 红绿涨跌,默认值。CSS 与 AlphaVault Site 的 `siteCss()` 同源(Google Sans、g-palette、Material 卡片/阴影、4 色 logo 点)
- `claude`:Claude.ai 暖色风格——奶油底 + 黏土橙(clay)强调 + 衬线(serif)标题,编辑器质感
- `print`:黑白衬线、A4 友好,适合导出 PDF 或邮件附件

新增主题:在 `themes/` 下放 `<name>.css`,`list_themes()` 自动发现。

## 同步路径

源码在 `shared/html_report/`。通过 `skill-sync.yaml` 的 `shared.bundles` 同步到目标 skill 的 `scripts/_shared/html_report/`(纯渲染型 skill),或随整个 `shared/` 进 `scripts/_shared/`(同时需要 `db_core` 的 skill)。各 skill 用文件头的 `sys.path` 片段引导导入:

```python
_BUNDLED = Path(__file__).resolve().parent / "_shared"
_DEV = Path(__file__).resolve().parents[2] / "shared"
sys.path.insert(0, str(_BUNDLED if _BUNDLED.exists() else _DEV))   # 装包后用 _shared,开发时回落仓库 shared/
```
