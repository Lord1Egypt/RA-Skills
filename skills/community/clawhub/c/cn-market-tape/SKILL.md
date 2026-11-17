---
name: cn-market-tape
description: Use when the user asks for A-share intraday or after-close market tape, theme strength TOP10/BOTTOM10, sector or board money-flow rankings, limit-up pool, institutional survey heat, or a combined read of these signals. Use MX as the primary A-share data layer, preserve the weighted local theme universe for formal theme rankings, and use aggregate fallback sources with rate-limit discipline when MX cannot provide a requested field.
---

# CN Market Tape

统一处理 A 股盘中和盘后盘面数据。默认只抓用户请求的模块，不读取或修改用户自选股之外的账户数据，不把一日榜单、资金流和机构调研混成一个结论。

## Routing

先判断用户要的是盘中快照、收盘数据还是历史数据，再选择模块：

1. `题材强弱`、`题材 TOP10/BOTTOM10`：使用本 skill 的加权题材流程。
2. `板块流入流出`、`主力净流入/净流出`：先尝试 `mx-data` 或等价 MX 查询；MX 不支持、字段为空、只返回“全部A股”市场合计、日期不匹配或接口不可用时，使用聚合的公开资金流备用源。
3. `涨停池`：先尝试 MX 或已有的聚合涨停池接口；不要逐只股票抓取涨停状态。
4. `机构调研`：当前/最近交易日优先运行本 skill 内置的机构调研聚合脚本或 MX 查询；历史请求优先使用公开历史调研热度数据，找不到对应日期或字段时明确声明不支持。

若用户只要求“盘中快照”，不要自动抓股吧、新闻或历史数据；若用户要求“为什么”或“复盘”，再按需要调用 `mx-search`、`cn-stock-move-reason` 和 `macro-news-check`。

## Dependencies

题材强弱的必需依赖：

- `mx-zixuan`：先取一次用户自选股行情，作为快速覆盖层。
- `mx-xuangu`：按代码批量补抓题材映射中未覆盖的 A 股成分。
- `mx-search`：默认只对 TOP3 题材做驱动核查。

其他模块：

- `mx-data`：优先用于板块资金、涨停池、机构调研和指定字段的补充查询。
- `visualize`：用户要求分钟级折线图时，用于渲染带零轴和拐点标注的分时资金图；不可用时退回分钟数据表并说明限制。
- `scripts/institutional_survey_heat.py`：机构调研明细的低频抓取、去重和股票/行业/周度聚合。
- `cn-stock-move-reason`：只有用户需要解释涨停池或个别板块异动时再调用。
- `macro-news-check`：只有用户要求把宏观、跨市场或大盘因素纳入时再调用。

MX 未配置、认证失败、超 quota 或返回空数据时，不要假装已有结果。按 `references/market-tape-source-routing.md` 切换到明确的聚合备用源，并在状态行报告口径变化。

## Module 1: Theme Strength

### Theme universe

题材强弱榜使用本地 A 股题材映射缓存和配置的公共题材 JSON 源。缓存文件为：

- `assets/themes/theme-data.json`
- `assets/themes/theme-label-i18n.json`

正常运行时执行一次映射刷新脚本；两份缓存都有效且未超过 7 天时跳过网络刷新：

```bash
python3 <cn-market-tape>/scripts/refresh_theme_assets_from_public_source.py
```

刷新失败但缓存有效时继续运行，并在状态行写明“题材映射刷新跳过”。缓存缺失或无效且刷新失败时停止题材强弱模块，不得从 MX 行业名临时发明题材池。

只保留 `market == "CN"`、`theme != "未分類"` 的行。每行至少需要 `code`、`theme` 和 `weight`；重复的股票-题材关系按独立权重参与计算。中文标签优先取 `theme-label-i18n.json[theme].zh`。

### Quotes and aggregation

1. 提取去重后的 A 股代码，但保留所有股票-题材关系用于加权。
2. 调用 `mx-zixuan` 一次，读取 `SECURITY_CODE`、`SECURITY_SHORT_NAME`、`NEWEST_PRICE`、`CHG` 和 `dateMsg`。
3. 对缺失代码按最多 50 只一批调用 `mx-xuangu`，批次串行。遇到 `操作过于频繁` 或 HTTP 503，等待 8-15 秒后重试同一批，最多重试 2 次。
4. 合并行情时优先使用 `mx-zixuan`，用 `mx-xuangu` 补齐；若日期不一致，报告混合日期风险。
5. 按下式计算每个题材的加权涨跌幅：

```text
theme_return = sum(theme_weight * stock_chg_pct) / sum(theme_weight)
```

`CHG` 按百分数处理，例如 `10.03` 表示 `+10.03%`。TOP 榜列出 `weight * CHG` 最大的贡献股，BOTTOM 榜列出最小的拖累股。

### Theme interpretation

需要判断持续性、拥挤度、主线、反抽或退潮时，读取 `references/theme-mainline-lifecycle.md`。生命周期只解释榜单质量，不替代加权排名。

默认只检查 TOP3 题材：每个题材选涨幅最高的代表股，结合股吧/讨论发现和 `mx-search` 资讯，区分确认消息、市场思惑、海外映射和个股独立逻辑，并给出“较高/中等/较低”确定度。

## Module 2: Sector Money Flow

### Source priority

先用 MX 查询板块或行业的主力净流入/净流出及数据时间。只有返回结果同时包含目标板块/行业名称、板块级资金字段和目标交易日，才算有效板块结果；如果只返回“全部A股”市场合计、`dataTableDTOList` 为空、字段缺失、日期不匹配或调用失败，切换到一个聚合的公开资金流接口，默认优先使用 `push2.eastmoney.com` 的批量接口，`push2delay.eastmoney.com` 仅作为备用。不要逐板块、逐股票循环抓取。

备用源的字段、请求顺序、超时和错误处理见 `references/market-tape-source-routing.md`。排名榜必须分别获取净流入方向和净流出方向；不能只取按降序返回的第一页，再把末尾几行误称为净流出。若接口声明的总数超过本次返回条数，要记录分页/返回上限风险。金额原始值按元解析后再统一换算为亿元，并保留接口更新时间。同一 host 连续请求超过 3 次后必须加入 8-20 秒随机等待；已出现 HTTP 429/403/5xx、超时、DNS 失败或连接重置时，立即报告 host、endpoint family 和错误，停止继续增加该 host 的请求量。

### Required output

盘中/盘后资金流必须按以下口径输出：

```text
数据时间：YYYY-MM-DD HH:MM；资金口径：主力净流入/净流出；来源：MX 或备用聚合源。

主力净流入 Top10
排名 | 板块 | 主力净流入

主力净流出 Top10
排名 | 板块 | 主力净流出
```

金额必须带单位，优先统一为亿元；同时给出市场宽度或指数快照（如可得）。说明榜单是当前快照还是收盘值，且不要把两个榜单的金额相加：不同板块标签可能重叠，资金流也可能按不同板块口径重复统计。

如果只获得部分板块或只获得净流入方向，明确标注“不完整”，不要补造另一张榜。

### Intraday minute flow and theme/sector chart SOP

When the user asks for `分时流入流出`、`分钟级资金`、`资金折线图`、`资金曲线` or asks to see the intraday turning point of a named sector/theme, follow the full SOP in `references/intraday-flow-chart-sop.md`. The short version is:

1. Disambiguate the object first. `融资融券` can mean the `融资融券` concept board or the market-wide margin-financing/margin-trading account statistics. The former can use minute-level board fund-flow data; the latter is generally an exchange daily summary and must not be presented as a minute chart.
2. Resolve the exact industry/concept board code from an aggregate board list; use `m:90+t:2` for industries and `m:90+t:3` for concepts. Do not guess a code, and do not mistake a constituent-stock response for a board row. In the same run, accept a minute series only when its `data.name` exactly confirms the requested board.
3. Query the current-day minute series from the default public host with `klt=1` and `lmt=240`. Preserve provider timestamps and trading-session gaps exactly; never interpolate the lunch break or missing points. Record the series' latest point separately from the ranking snapshot's update time because the minute endpoint may lag. If the default host returns an endpoint error, switch once to `push2delay.eastmoney.com` under the routing rules; do not keep retrying the failed host.
4. Interpret `f51` as timestamp, `f52` as cumulative main net inflow, `f53`/`f54` as small/medium-order net flow, and `f55`/`f56` as large/super-large-order net flow. Parse yuan first, then convert to亿元. Check that `f52` approximately reconciles to `f55 + f56` before charting.
5. For one board, plot cumulative `f52` with a visible zero line, y-axis unit, date/time, source, cumulative label, lunch gap, low/high, zero crossings, and latest point. For multiple themes/boards, use one shared time axis; use 分面图 when scales differ and do not normalize away the yuan/亿元 meaning. The chart is supplemental to the latest snapshot table.
6. Only when the user explicitly asks for “每分钟变化/增量” calculate adjacent-point differences of `f52`; render and label that series separately from the cumulative curve.

The default chart read should state whether the tape is persistent outflow, early outflow then recovery, early inflow then distribution, or two-way high-level divergence. A positive latest point after a deep intraday drawdown is a recovery path, not automatically a full-day inflow trend. If the endpoint is empty, stale, non-JSON, rate-limited, timed out, or otherwise unstable, report the host/endpoint family and stop increasing request volume; return the validated snapshot table or state that the chart is unavailable.

### Intraday snapshot comparison

同一交易日内再次查询资金流时，自动读取本次会话中的上一次结果；若会话中没有，则读取运行时快照缓存。缓存只保存聚合榜单、交易日、数据时间、来源、资金口径和单位，不保存原始响应或账户数据。默认缓存位置为用户级 Codex 运行时目录，不得写入本仓库。

只有当交易日、资金口径、来源、单位、板块/行业宇宙和数据时间范围一致时才做数值比较。MX 切换到备用源、榜单口径变化或日期不一致时，仍输出当前表，但在表头写明“上次快照不可比”，不能把不同口径的数字相减。分时图比较优先使用相同时间点；只能取得各自最新点时，明确写出时间不一致和接口滞后。

首次查询时保存当前快照，并在表头写 `上次快照：无`。再次查询时，仍然只输出两张表，但列改为：

```text
主力净流入 Top10（当前 vs 上次）
当前排名 | 板块 | 当前净流入 | 上次排名 | 上次净流入 | 变动额

主力净流出 Top10（当前 vs 上次）
当前排名 | 板块 | 当前净流出 | 上次排名 | 上次净流出 | 变动额
```

当前或上次未进入对方 Top10 的板块使用 `—`，并标注 `新入榜` 或 `出榜`；`—` 不等于零，不据此计算虚假的变动额。表格之后只补一行数据状态，例如 `上次快照：10:32；当前：11:18；可比；来源：MX。` 查询成功后再写入当前快照，失败时不得覆盖上一次快照。

## Module 3: Limit-up Pool

优先查询当天聚合涨停池，校验交易日期 `qdate` 与当前请求日期。输出至少包括：

- 涨停总数、有效普通涨停数、跌停数（接口提供时）。
- 最高连板数，以及 2 板及以上的数量（接口提供时）。
- 炸板数、封板率、封单金额或成交额（接口提供时）。
- 连板梯队和行业/题材分布。
- 用户点名或与当前主线有关的重点股票，可列名称、代码、连板数、首次/最后封板时间和炸板次数。

区分“涨停池统计”和“涨停个股原因”。只有用户要求原因时，才对重点股票调用 `cn-stock-move-reason`；不要把聚合池扩展成逐只新闻抓取。

若盘中接口返回的是动态池，写明统计时间；盘后以收盘快照为准。日期字段缺失或不是目标交易日时，标记数据日期风险。

## Module 4: Institutional Survey

当前或最近交易日：使用本 skill 内置的 `scripts/institutional_survey_heat.py` 或 MX 查询调研记录，按既有机构调研口径输出股票、行业和周度热度。

历史请求：

1. 优先使用公开历史调研热度数据或对应的历史 JSON 快照。
2. 校验目标日期/日期区间、`RECEIVE_START_DATE` 和数据生成时间。
3. 若历史源没有对应日期、字段或完整窗口，直接写“尚不支持该时间/数据”，不得用当前快照冒充历史数据。

## Combined workflow

1. 先列出本次需要的模块和数据时间，避免无关抓取。
2. 题材模块先刷新/读取映射，再用 MX 批量取行情。
3. 资金流、涨停池、机构调研优先使用 MX；需要备用源时按引用文件串行访问并随机等待。
4. 每个模块返回后先校验日期、字段完整性和数据来源，再合并结论。
5. 盘中报告标记 `盘中快照`，盘后报告标记 `收盘快照`；历史报告标记数据窗口。
6. 若某一来源失败，报告失败的 host/endpoint family、错误类型和切换后的来源；不要重复轰击已不稳定的接口。

## Default output order

用户未指定顺序时，按以下顺序输出：

1. 数据状态和时间。
2. 市场宽度/指数简表（可得时）。
3. `题材强弱 TOP10/BOTTOM10`。
4. `主力净流入 Top10` 和 `主力净流出 Top10`。
5. `涨停池`。
6. `机构调研`。
7. 只在用户要求时补充 TOP3 题材驱动、消息、技术或操作风险。

题材表默认列：`排名 | 题材 | 加权涨跌幅 | 主要贡献/拖累`。

资金表默认列：`排名 | 板块 | 主力净流入/净流出`。

始终用中文回答。说明每个数字是实时、延迟、盘后还是历史数据。默认不写输出文件，不提交 API key、cookie、账户标识、完整自选股列表、原始响应或运行缓存。

## Safety

- `mx-zixuan` 只查询，不添加、删除或修改自选股。
- 不把用户的个人持仓、自选股、私有调研资料或账户数据写入本仓库。
- 不把不同源、不同时间、不同统计窗口的数字直接拼接成一个精确结论。
- 输出仅用于市场研究，不构成投资建议。
