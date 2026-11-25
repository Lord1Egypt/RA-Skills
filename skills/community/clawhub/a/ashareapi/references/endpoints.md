# 端点清单（102 个）

- **统一前缀**：`https://api.ashareapi.com/v1`
- **统一信封**：`{ ok, endpoint, tier, elapsed_ms, source, data }` —— 只有这 6 个键
  - ⚠️ **`structured` / `tables` 是【条件字段】，不是每个端点都有**：**只有 `data` 是 Markdown 文本时才附**
    （`market-overview` · `changedist` · `lhb` · `sector` · `sector-valuation` · `bond` · `etf` · `screen` · `macro`）。
    **其余端点没有这两个键** → `body["structured"]` 会 **KeyError**，**一律用 `body.get("structured")`**。
  - ⚠️ **4 个端点信封不同**（都**没有 `data`**）：`/v1/health` = `{ok, uptime_s, data_ready, tiers}` ·
    `/v1/challenge` = `{challenge, difficulty, expires_in, how_to}` · `/v1/usage` = `{ok, day, calls_today, tier, total_calls, total_quota, total_left, daily_quota, per_min}` ·
    `/v1/ip-whitelist` = `{ok, ips, enabled, max_ips}`（`GET`；`POST`/`DELETE` 为 `{ok, ips, enabled}`）
- **参数带 `*` = 必填**
- **实时规格**：`GET https://api.ashareapi.com/openapi.json`

---

## 一、免费端点（无需 Key，7 个数据端点 + 1 个文档检索 + 2 个工具端点，共 10 个）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/quote` | `code*`（支持逗号批量；**匿名单次最多 5 只标的**）| **实时行情快照**（轻量 8 字段）。⚠️ `data` 是**数组**：默认 **30 条日线**、**降序**（`data[0]` 最新，取现价用 `data[0]`）。字段：`last` / `open/high/low` / `volume`（手）/ `amount`（元）/ `turnover` 换手率% / `date`。⚠️ **免费 / 匿名档 5 分钟刷新，付费档实时**（盘中约每分钟）。⚠️ **不含估值 / 市值** —— 要这些用 `/v1/snapshot`（35 字段，pro 档，仅 A 股）。⚠️ 支持 **A 股 / 港股 / 美股**；美股三大指数：道指 `usDJI` · 纳指 `usIXIC` · 标普500 **`usINX`**（⛔ 不是 `usSPX`） |
| `/v1/kline` | `code*`（支持逗号批量；**匿名单次最多 5 只标的**）· `period`(day/week/month/season/year/**m1/m5/m15/m30/m60/m120**) · `count`（默认 30，最大 **1212**；**匿名最多 250**）· `start`/`end`（仅 day 与分钟线，须配对）| OHLCV 历史 K 线 —— **字段恒定 8 列**：`date` / `open` / `last`(收盘) / `high` / `low` / `volume`(手) / `amount`(元) / `turnover`(换手%)。⚠️ **收盘价字段名是 `last` 不是 `close`**；**返回按日期降序**（最新在 `data[0]`，别当升序算涨跌幅）。⚠️ **分钟线属付费层**（`standard` 起；日/周/月/季/年免费 —— 免费档 5 分钟刷新、付费实时），窗口近 **1 个月**（整段超出 → 422）；北交所/期货/外汇无分钟线，美股指数仅 `day`，期货外汇仅 day/week/month。⚠️ 复权口径**由服务端固定**（无 `fq` 参数）：日线及以上前复权（除权除息日不跳空），分钟线不复权 —— **不要再自己复权**（会二次复权）。⭐ 要原始价/后复权用 `/v1/kline-batch` 或 `/v1/kline-full`。⚠️ `start`/`end` 仅 day 与分钟线（须配对），周/月/季/年线用 `count`；**港股/美股不支持日期范围**。⚠️ `000001` 按深市处理（平安银行），指数请显式 `sh000001` |
| `/v1/hot` | `limit`（默认 30，**上限 50**）· `type`（`stock` 热搜股票 / `wx` 全市场热度带 pv / `news` 热门文章 / `sector` 热门板块 / `etf` 热搜 ETF —— ⚠️ 5 类字段各不相同）| 热度榜（默认热搜股票）|
| `/v1/market-overview` | `type`(summary/trade/interval/technical/margin/**valuation**/**rotation**) | 大盘画像。`valuation` = 中证全指 PE/PB/PS **历史百分位**；`rotation` = 风格轮动（大小盘/成长价值）。⚠️ `type=updown` 是 **T-1 口径**，涨跌家数请用 `/v1/changedist` |
| `/v1/changedist` | 无 | **当期**涨跌家数 / 涨跌停家数 / 停牌 / 成交额 / 区间分布 —— **市场广度推荐入口**。⚠️ **`data` 是排版好的 Markdown 文本（给人看）**，程序化读取请用**顶层 `structured`**（每个指标一项）；多分组时用顶层 `tables`。⛔ **`structured` 在响应顶层，不在 `data` 里** —— 读 `data.structured` 会拿到空，不是没数据 |
| `/v1/wiki` | `q` 关键词 · `slug` 取单篇 · `lang`(zh/en) | ⭐ **产品文档检索**：字段单位 / 口径 / 常见误用 / 跨市场差异。⚠️ **不确定某字段含义或单位时先查这里，别猜**。**渐进加载**：不带参 = **目录**（小）；`q=` = **摘要**（含片段，**不含全文**）；`slug=` = **该篇全文**。免费但**计入用量与限流** |
| `/v1/models` | 无 | OpenAI / Anthropic 兼容的模型清单（**免费、无需 Key**）。返回真实可用的 `deepseek-flash` / `gpt-5.6-luna` / `claude-*`，另含 `ashare/scanner@deepseek-flash`（选股员，专业版 ¥99+）。聊天仍需 `apiKey = ct-xxx:sk-yyy`（BYOK） |
| `/v1/trade-calendar` | `date` · `start`/`end` · `year` · `trading_only` · `limit`/`offset` | **A 股交易日历**：逐个日期给出是否开市，以及是否为本周 / 本月 / 本季 / 本年的**最后一个交易日**（结算日、到期日、调仓日用）。⚠️ 与 `/v1/calendar`（个股事件日历）不同：本端点**只讲市场开不开市**。查询三选一：不传 = 当月 · `date=` 单日 · `start`+`end` 或 `year=` 区间。`trading_only=true` 只返回开市日（整年约 242 行）。⚠️ `limit` 默认按范围自动补足（年/区间给满 400 行上限），翻页用 `offset`。⚠️ `data` 是排版表格，**程序取数用顶层 `structured`**。⚠️ **免费**（无需 Key） |
| `/v1/health` | 无 | `data_ready=true` 表示数据通道可用 |
| `/v1/challenge` | `difficulty` | PoW 挑战（匿名提额用）。解 nonce 后带 `X-PoW: <challenge>.<nonce>`，匿名配额 5 → 15 次/分（**只提每分钟次数，每日条数上限不变**）|

---

## 二、行情与技术（需 Key）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/technical` | `code*` · `date`（交易日，默认最新；非交易日自动回退，以返回的 `date` 为准）| 技术指标全家桶：MA / EMA / MACD / KDJ / RSI / BOLL / BIAS / WR / DMI / OBV / VR / BBI / TRIX / DPO / PSY / ENE / CCI 等**共 55 项**。⚠️ **只有日线口径**（周期参数不生效 ⇒ 不提供）。⚠️ 代码可传 `sh600667` 或裸 6 位；**A 股（含北交所）/ 港股 / 美股**均支持。⭐ **多只请用 `/v1/technical-batch`**（500 只 1.2 秒，逐只状态） |
| **`/v1/kline-full`** | `code*` · `fq`(qfq/hfq/bfq/nofq，**默认 qfq**) · `start` · `end` | ⭐ **A股全历史日线**（一次拿到**全部日线**，约 **2,500 根**，2016-08-08 起 —— 而 `/v1/kline` 上限 1212 根）。⚠️ **`fq` 可选且默认 `qfq`**（与 `/v1/kline` 的"服务端固定"不同）⇒ 本端点**可以**自己指定复权口径。⚠️ **日期字段名是 `time`**（不是 `date`！其余 K 线端点用 `date`）；字段 = `time/open/high/low/close/volume/amount`。⚠️ 属付费层 |
| **`/v1/market-kline`** | `date*`（YYYY-MM-DD）· `limit` · `offset` · `codes` | ⭐ **全市场单日 K 线**：**一次**返回全市场（**5000+ 只 A 股**）某交易日的日线 —— 替代逐只调用（省 5000+ 次请求）。字段：`code`/`time`/`open`/`high`/`low`/`close`/`volume`/`amount`（**不复权原始价**）。⚠️ **`volume` 单位是「股」**（不是手）—— 与 `/v1/kline`、`/v1/kline-batch` 的「手」相差 100 倍；`amount` 单位元。⚠️ **仅 `pro`（专业版 ¥99）/ `unlimited`（机构版 ¥199）** —— `standard` 及以下**不可用**；⚠️ **1 次调用 = 折算 500 次额度**；日额度 `pro` 200 / `unlimited` 1000。⚠️ 范围 = **仅 A 股股票**（5,572 只 · 2016-08-08 起），⛔ 不含 ETF / 转债 / 指数 / 板块 / 港美股；最新到**前一交易日**（当日盘中不可用）。体积约 **785 KB / 日**。⭐ 传 `codes` 时逐只回报 `requested` / `returned` / `missing`（`reason` = `not_covered` 不在覆盖范围 / `no_data` 当日无行情）；用 `limit` 分页时未出现 ≠ 没数据（会标 `partial:true`） |
| `/v1/minute` | `code*` · `days`（`1` 当日 · `5` 近 5 个交易日，**只有这两档**）| **分时**：盘中每分钟一价 + 累计成交量。⚠️ 与 `/v1/kline` 的**分钟 K 线不是一回事**（前者分时、后者 OHLC 蜡烛）。⚠️ **含 15:00 后的盘后固定价格交易**（15:05—15:30），`kline` 不含；**末点 15:30 的 `amount` 是当日累计值** ⇒ ⛔ 别拿末点比 `kline` / `snapshot`（它们等于 `15:00` 那一点）。⚠️ `days` **只有 1 / 5 两档**（传 2/3/4 不报错但一律返回整 5 日）。⚠️ **standard（¥29.9）起** |
| `/v1/chip` | `code*` · `date` | 筹码分布与持仓成本（套牢盘 / 获利盘比例，判断抛压）。`date` 回看历史（**仅近 1 年**，实测 2025-10-24 起；更早返回空 ⇒ `ok:false` 且**不扣次数**）。⚠️ 非交易日 / 未来日期**自动回退**到最近交易日，以返回行 `date` 为准。⚠️ **支持沪深 A 股与 ETF**（实测 `sh510300` 有值，口径与个股相同）；**港股 / 美股不支持** |
| `/v1/orderbook` | `code*` | **五档盘口（order book）**：买一~买五 / 卖一~卖五的**价 + 挂单量（手）**。字段：`b1_p`/`b1_v`~`b5_p`/`b5_v`（买档）、`a1_p`/`a1_v`~`a5_p`/`a5_v`（卖档）。⚠️ **秒级快照（10 秒缓存）· 盘中才有意义**；量单位是**手**（×100 = 股）；**跌停买档全 0 / 涨停卖档全 0**（正常）|
| `/v1/snapshot` | `code*` | **全字段行情画像（35 字段）**：`code/name/sec_type/currency/status` + 价格（`price/prev_close/open/high/low/avg_price/change/change_pct/amplitude/speed`）+ 量（`volume/amount/turnover/outer_vol/inner_vol/volume_ratio`）+ 估值（`pe_ttm/pe_dynamic/pe_static/pb`）+ 市值股本（`float_market_cap/total_market_cap/float_shares/total_shares`）+ 涨跌停（`limit_up/limit_down`）+ 盘口（`bid/ask/bid_ask_diff`）+ `time`。⚠️ **单位**：`volume` 手 · `amount` **万元** · 市值 亿元 · 股本 股 · 比率/涨幅 百分数。⚠️ **`amount` 精度 = 1 万元**（该字段本身即整数万元，不做换算）⇒ 与按元计的 `/v1/kline` `amount` 有 0~9,999 元取整差，**要精确到元请用日线 `amount`**。⚠️ **交易范围 = 15:00 收盘**（不含盘后固定价格交易）；与 `/v1/minute` 末点 15:30 不可直接比。⚠️ **仅 A 股**（港股/美股用 `/v1/quote`，传了返空不返错数据）。✅ **计费 = 次数**：要估值+市值+股本+涨停价多项时，1 次搞定比分别调 quote/valuation/orderbook **更省次数** |
| `/v1/search` | `q*` | 按名称 / 代码搜股票、基金、板块 —— **用户只给名称时先搜代码**。⚠️ **覆盖 A 股 / 港股 / 美股**：`hk00700` / `usAAPL` 都能搜到；⚠️ **港股代码是 5 位**（`hk00700`），与 A 股 6 位不同 |
| `/v1/profile` | `code*` | 公司简况：上市日期 / 主营业务 / 所属行业 / 官网 / 注册资本 / 董事长 / 联系方式。⚠️ **ETF / 指数请改用 `/v1/etf?kind=详情` 或 `/v1/quote`** —— 本端点对 ETF 只有 `code`/`name`/`listedDate` 有值，`business`/`industry`/`sector`/`chairman` **本来就没有**（不是取数失败）；ETF 的 64 个字段在 `/v1/etf?kind=详情` |
| `/v1/index-list` | `limit`（1~500）· `offset` · `date`（留空=最新）| **指数清单**（1,223 个，含港股指数）—— 中证 `cs*` 系列只在这里能取到（拿它们的 K 线/行情会返回空）|

## 三、财务

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/finance` | `code*` · `num`（返回期数，默认 4，降序）| 利润表 / 资产负债表 / 现金流量表（多期，**最近 N 期、降序**）。⚠️ **多只请用 `/v1/finance-batch`**（本端点只查一只）。⚠️ 支持港股（`hk00700`），但**按 A 股列名硬解析会错**。⚠️⚠️ **银行 / 保险 / 券商没有 `TotalAssets`**，也没有流动/非流动拆分 —— 用 `EnterpriseType` 判行业，⛔ 别用 `TotalCurrentAssets + TotalNonCurrentAssets` 推总资产。⚠️ **`data` 是【表列表】`[[行...], [行...], ...]`**（外层=表，内层=行）→ **先按表索引再按行**：`data[0][0]["..."]` |
| `/v1/dividend` | `code*` · `years`（年数，默认 3）| 分红送转历史：每股分红 / 送股 / 除权日 |
| `/v1/shareholder` | `code*` | 十大股东 / **股东户数（筹码集中度）** / 机构持仓。⚠️ **`data` 是【多段结构】**：`{code, market, tables: [{title, slug, rows}], data: {slug: rows}}`。⚠️ **A 股与港股段语义不同（都 3 段但完全不同）**：A 股 = `top10_holders` / `top10_float_holders` / `holder_count`；港股 = `shareholders` 持股股东 / `holder_distribution` 股东分布 / `institutional_holdings` 机构持仓 ⇒ **按 `market` + `slug` 取，⛔ 别按序号** |

## 四、资金与交易（核心）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| **`/v1/fund`** | `code*` | ⭐ **一接口拿全交易面**：主力资金（当日 / 5 / 10 / 20 日净流入 + 全市场排名）+ 龙虎榜（上榜原因 / 买卖总额 / **营业部明细**）+ 大宗交易 + 融资融券。**问「主力资金 / 资金流 / 龙虎榜」优先用它**。⚠️ **仅 A 股**（港股个股资金流用 `/v1/fund-flow`）。⚠️ `data` 是**扁平 dict**（不是多段）：`{date, close, main_net, main_net_5d/10d/20d, main_rank, lhb, lhb_details, block_trades, margin, industry_rank}` |
| **`/v1/fund-batch`** | `codes*`（**逗号分隔**，如 `sh600519,sz000001,sz300750`）| ⭐ **一次拿多只的资金流**（主力资金 + 龙虎榜 + 大宗 + 两融），每只一条 —— 扫一个行业或自选池不必逐一调 `/v1/fund`。`data` = 数组，每项 `{code, ok, data}`（或 `error`）⇒ **逐只标明成功与否**，另给 `requested`/`returned`/`failed`。⚠️ **仅 `pro`（专业版 ¥99）/ `unlimited`（机构版 ¥199）**；上限 `pro` **200** 只 / `unlimited` **1000** 只；**计费按实际返回只数**（失败不计）。⚠️ **标的范围**：仅 **A 股**（`sh`/`sz`/`bj`）；**港股只有主力净流入一项**，**美股无资金流**（该只标 `ok:false`） |
| `/v1/lhb` | `type`(institution/hotmoney/activeseat) · `date` | **龙虎榜 6 种榜**：`all` 全市场总榜（净买 / 买卖额）· `institution` 机构榜（机构数 / 机构买入 / 净买）· `activeseat` 活跃席位（席位买入额 + 关联个股）· `winbuy` 高胜率买入（净买额 / 胜率 / 席位明细）· `winseat` 高胜率席位（席位胜率 + 关联个股）· `hotmoney` 游资榜。⚠️ **`hotmoney` 暂无数据** ⇒ 改用 `all` / `activeseat` / `winbuy`。⚠️ 收盘后发布（一般 18:00 后）；`date` 留空 = 最近交易日 |
| `/v1/margin-trade` | `code`（**必填**，支持 `sh600667,sz000651` 批量）· `date` | 融资余额 / 买入 / 偿还 / 融券（金额元）。`code` 支持逗号批量；缺 `code` 会明确报错。⚠️ **ETF 不在两融名单** —— 如 `sh510300` 无论当日还是历史日都恒回 `NOT_DISCLOSED`（文案写「尚未披露」，实为标的不属于两融），⛔ 别当数据延迟去重试 |
| `/v1/block-trade` | `code` · `date` | 大宗交易：成交价 / 折溢价 / 量 / 买卖方营业部 |
| `/v1/events` | `code*` | 个股事件总览：**42 类**（大宗 / 龙虎榜 / 回购 / 定增 / 分红 / 业绩 / 解禁 …）|
| `/v1/calendar` | `date` · `limit` | **个股**事件日历（分红派息 / 解禁 / 财报披露 / 会议 / 增发 / 新股）。**不是宏观日历**（宏观用 `/v1/macro`），也**不是财报披露日**（那个用 `/v1/disclosure`）。⚠️ **`data` 是【多段结构】**：`{tables: [{title, slug, rows}], data: {slug: rows}}`，按事件类型分段保序；slug = `financial_report` / `dividend` / `ipo` / `meeting` / `lockup_release` / `rights_issue`。⚠️ **支持港股**（`hk00700` 实测 151 条事件，密度远高于 A 股），同样按 slug 取段 |

## 五、板块与产业链

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/sector` | 无 | 行业 / 概念 / 地域板块涨幅榜 + 领涨股。用户问『哪些板块在涨 / 板块轮动 / 行业热度』时用 |
| `/v1/sector-valuation` | `code*`（`pt01801780` 形式）| 申万板块 PE/PB/PS/PCF + 股息率 + **历史百分位** |
| `/v1/industry-chain` | `mode`(list/graph/stock) · `topic` · `code` | `list` = **183 个主题** · `graph&topic=X` = 图谱（关联个股 + 节点 + 上中下游）· `stock&code=X` = 该股所属链（主题/节点/位置/**关联度**/业务描述）|

## 六、可转债 / ETF / 新股

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/bond` | `code*`（`sh113052`）| 转债完整条款：溢价率 / 转股价值 / **双低值** / **强赎触发价** / 回售触发价 / 转股价 / 正股 / 到期日 / 信用评级 |
| `/v1/etf` | `code*`（`sh510300`）· `kind` · `start` · `end` · `date`（仅 kind=概览/持仓：历史快照日，留空=最新）| ETF 数据。`kind` = **概览**（默认，行情/规模/溢折率/资金流）/ 详情 / 持仓 / **净值**（须传 `start`+`end`，4 位单位净值）/ 公司 / 持有人 / 财务。⚠️ **`code` 单次只接受 1 只** —— 传逗号会 422，多只请分别请求（各自计次）。⚠️ 传个股代码返回 `ok:false` 且**不扣次数**。⚠️ `data` 是排版好的文本，**字段请取 `structured`（首表）或 `tables`（全部表）** |
| `/v1/ipo` | `days`（查询天数，默认 15）| 新股发行 / 申购 / 中签 / 上市日历。⚠️ **三市场覆盖**：A 股 / **港股** / 美股 |

## 七、选股与宏观

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/screen` | `mode` · `filters` · `preset` · `sort` · `board` · `metric` · `pool` · `strategy` · `event` · `limit` · `offset` · `date` · `start` · `end` · `asset` · `list` · `slim` | **选股：五分模式**。`mode` = `filter`(默认)/`pool`/`rank`/`strategy`/`event`；`filters` 逗号分隔＝AND（`pe_ttm:0..20,roe_ttm:>=15`，区间含两端，支持 `>=` `<=` `>` `<` `=`）；`sort=roe_ttm` 降序、`-` 前缀升序；`board` = `hs300`/`zz500`/`zz1000`/`sse50`/`sz_component`（不传＝全市场）；`metric` = `overall`（默认）/`capital`/`fundamental`/`risk`/`technical`（仅 rank 模式）；**94 个筛选字段 / 108 主题池 / 98 策略 / 42 事件 / 22 预设**，全部用 `list=fields\|pools\|strategies\|events\|presets\|metrics\|boards` 自发现（⛔ 别猜，猜错 422）；`limit` 在 filter 模式**无上限**（9999 = 全市场），其余模式单页 ≤200；`offset` 翻页；`date` 历史截面；`asset=etf` 切 ETF 池；`slim=true` 省约 42% 体积（旧参数 `expr` / `orderby` / `desc` / `market` **仍兼容**）|
| `/v1/macro` | `region`(cn/us/jp/eu/hk) · `names` · `limit`（每个指标最多返回最近 N 条，默认 12；取多年历史建议 60）| 宏观：GDP / CPI / PMI / LPR / 国债收益率 / 财政。⚠️ **`data` 是 Markdown 文本（给模型读），`structured` 是同内容的行列表（程序取数用后者）**；多分组时用顶层 `tables`。💡 不确定指标短名 ⇒ `names` 留空取全套清单，或只传 `region` 拉该地区全部指标 |
| `/v1/dehydrated` | `mode`(list/detail) · `symbol` · `limit`（默认 10）| 券商研报脱水摘要 |
| `/v1/usage` | 无 | 当前 Key 的今日调用次数 / 剩余总量（买断档）/ 到期时间（订阅档）/ 限流额度。⚠️ `by_endpoint` = 今日**各端点**实际消耗（按消耗降序取前 8）—— 撞 429 时先看这项，能定位是哪个端点吃掉额度。⚠️ **批量端点按返回只数扣额度**（故一次 `codes=` 带 450 只 = 450 次）。⚠️ 只反映**今天**（次日 0 点归零），不含上线前历史 |

---

## 八、量化回测与因子（需 Key · 专业版）

> ⭐ 想"用策略跑历史收益"用这里。**先查清单再调用**：有哪 20 条单标的策略 / 9 条组合策略，先调 `/v1/strategies`。

| 端点 | 参数 | 返回要点 |
|---|---|---|
| **`/v1/backtest`** | `mode`(**single** 默认 / portfolio) · `strategy` · `code`（single 必填）· `start` · `end` · `initial_cash`（默认 100 万）· `weighting`(`equal` 默认等权 / `inv_vol` 波动率倒数 —— **机构版**能力) · `include_equity` | ⭐ **量化回测**。`mode=single` **单标的择时·实时算**（毫秒级，传 `code` + `strategy`）；`mode=portfolio` **组合选股·查预计算**（传 `strategy`）。返回 `metrics`（`total_return` / `cagr` / `sharpe` / `max_drawdown` / `ann_vol` / `final_nav`）+ `n_trades` + 可选 `equity` 净值曲线。⚠️ **只有 4 个预置区间**（全周期 / 近 4 年 / 近 2 年 / 前半段），省略 `start`/`end` = **全周期**；传其他区间会回 `available_ranges` 清单（不用猜）。⚠️ 成本已计入：佣金万三（最低 5 元）/ 印花税 0.05% / 滑点千一 + 涨跌停 / 停牌约束 |
| `/v1/backtest-batch` | `codes*` · `strategies` · `start` · `end` · `initial_cash` | **批量回测**（多标的 × 多策略对比矩阵）。返回 `matrix`（每题每策略的 metrics）+ `best` + `skipped`。⚠️ **上限：标的 ≤20 · 策略 ≤10 · 组合 ≤60**（超限直接报错，⛔ 不会只跑一部分）；**单票失败不中断整批**。⚠️ **专业版（¥99）起**；日额度 `pro` 20 / `unlimited`（机构版）100 |
| `/v1/strategies` | 无 | **策略清单**：单标的 20 条（`buy_hold` `low_vol` `dca` `vol_target` `ma_stop` `ma_cross` `grid` `mom20` `turtle` `rev5` `breakout` `atr_stop` `macd` `rsi` `boll` `kdj` `wr` `obv` `cci` `sar`）+ 组合 9 条（`buy_hold_equal` `lowvol20` `mom20` `mom20_ex_st` `rev5` `ma_cross` `volume_breakout` `smallcap` `largecap`），各含**参数白名单**（名称/类型/最小/最大/默认）。⭐ 每条带 **`performance` 实测表现**（沪深300 + 中证500 共 800 只 · 2019 年至今，**含佣金/印花税/滑点**），`verdict` = `effective` / `neutral` / `weak` / `avoid`（**实测亏损的也列出**，便于避开）。⚠️ 历史实测不代表未来。⚠️ **静态清单，不占重型额度**；门槛 `standard`（¥29.9） |
| `/v1/factors` | `category` · `kind` | **因子库 / 筛选能力字典**：**87 个因子**（估值 6 / 行情 2 / 盈利 34 / 资产负债 32 / 现金流 13，各带代码 / 中文名 / 单位 / 说明）+ **50 个非因子筛选入口**（排行 18 / 标签 21 / 事件 11，含排雷类如 `risk_st` / `risk_delisting` / `fin_unhealthy_growth` / `shareunlock_next_90`）+ **22 个预设** + **14 个策略模板** + 8 条使用规则 + 12 条易错写法。⚠️ `category` / `kind` **只接受中文枚举值**。⭐ 因子代码可直接用于 `/v1/screen?filters=`（大小写不敏感，标准写法小写下划线）；⛔ 不支持 `OR` / `between` / `in`。⚠️ **最常见错误**：`PE_TTM > 0` 必须前置（亏损股 PE 为负会被当低 PE 选入）。⭐ 支持历史截面（`/v1/screen?date=` 实测 2016-08-08 起）。⚠️ **静态清单**，门槛 `standard`（¥29.9） |
| `/v1/playbooks` | `category` · `id` | **方法论库**：25 条「怎么判断市场」流程（12 类玩法），每条含 `question` 问题 / `signals` 判据（算式 + 数据 + 阈值）/ `stages` 阶段与应对 / `avoids` 能避开什么亏损 / `evidence` 实测证据（未跑过的标「待实测」）。⚠️ 是**判断流程**不是数据；要数值用 `/v1/factors` |
| `/v1/ip-whitelist` | GET 无 · POST `ips` · DELETE `target_key` | **IP 白名单**（把 Key 锁到固定 IP，即使外泄也无法使用）。`GET` 查 / `POST` 设（覆盖式，最多 50 个精确 IP，⛔ 不支持网段）/ `DELETE` 清空指定 Key 的名单。⚠️ **属机构版（¥199）**；⚠️ **三个方法都要求"当前 IP 在名单内"** —— 换网络被锁死请联系客服 |

---

## 九、短线打板（需 Key · 标准版起；集合竞价 `auction` 需专业版）

> ⭐ 看「今天钱在哪些题材、梯队怎么排、谁被监管盯上」。`review` 的 `board`+`ladder` **共用一次取数**。

| 端点 | 参数 | 返回要点 |
|---|---|---|
| **`/v1/auction`** | `code*` · `mode`(stock 默认 / stock-history / volume) · `date` | **集合竞价**（9:15–9:25）。`mode=stock` **当日竞价分时**（分钟级 tick：`time` / `price` / `stage` 行情源标记位〔语义未公开，勿依赖；分可撤单/不可撤单段请用 `time`：09:15–09:20 / 09:20–09:25〕/ `volume` 累计量）；`stock-history` **历史竞价分时**（**秒级**，需 `date`）；`volume` **当日竞价量 / 净额**（`bid_volume` 手 · `bid_amount` 元）。含**「竞价触及涨停」判定** |
| **`/v1/limit-up`** | `mode`(limit 默认) · `date` | **打板**：`limit` = 当日**全部涨停**个股（含各连板高度，**一次全量无需翻页**）+ 涨停原因 + 资金面；`auction` = **竞价涨停**（09:25 定盘即封，判据 `limit_time <= 09:25`；竞价摸过但定盘前被砸开的**不算**）。字段：`code` / `name` / `streak` 连板数 / `limit_time`(Unix 秒) / `reason` / `seal_amount` 封单额(元) / `seal_amount_max` / `main_net` / `main_buy`·`main_sell` / `amount` / `concepts` / `float_cap` / `turnover` 换手% / `board_code`·`board_limit_count` / `pct`。⚠️ `date` 空 = 实时；给日期 = 该交易日历史（须**真实交易日**，否则空）；条数在顶层 `count` |
| **`/v1/review`** | `mode`(board 默认 / ladder) · `date` | **短线复盘（涨停结构）**：`board`（默认）**板块主线** = 当日涨停最集中的题材（`board_code` / `board_name` / `limit_count` / `amount` 成交额(元) / `stocks` 成分股）；`ladder` **连板梯队** = 按连板高度分组（`streak` / `limit_time` / 所属板块 / `market_cap` / `board_amount` / `tips` 如「7天4板」/ `max_streak` / `limit_days` / `is_repack` 反包）。⚠️ `date` 空 = 实时；给日期须**真实交易日**，否则空。⚠️ **天梯约 16:30 才汇总完成**（涨停池收盘即有），此前查当日 `ladder` 可能不全 |
| **`/v1/abnormal`** | `mode`(`deviation` 默认 偏离值热门榜-今日 / `deviation_hist` 同上-历史〔需 `date`〕/ `deviation_plan` 今日+明日两组〔`group` 区分〕/ `abnormal` 异动频率〔需 `date`，每日全量常见 500+ 条〕/ `watch` 异动盯盘名单-今日 / `watch_hist` 同上-历史) · `date` · `limit`(默认 600，1–2000) | **监管异动 / 偏离值**：触发「严重异动」「10 日 100% 偏离」、异动盯盘名单、**严重异动提醒** —— 短线风控关键信号。`deviation` 偏离值热门榜（今日实时，含 `reason` 规则 / `pct` / `turnover` / `board_desc` 连板 / `concepts` / `window`）；`deviation_hist` 历史（需 `date`）· `deviation_plan` 今日+明日两组（`group` 区分）· `abnormal` 异动频率。⚠️ `mode` 取值以 `/openapi.json` 为准 |

## 十、资讯与公告（需 Key · 标准版起）

> ⭐ 分工：**`news` = 时效**（最新消息面）· **`notice` = 历史**（可回溯约 16 年）。二者都是**不传 `id` = 列表**、**传 `id` = 详情**。

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/news` | `code` · `id` · `limit`(默认 50) · `type` | **个股 / 指数 / ETF / 板块 / 转债资讯**（A 股 / 港股 / 美股）。不传 `id` ⇒ 列表（**`code` 必填**，标题 + 来源 + 时间）；传 `id` ⇒ ⭐ **该条完整正文**（**干净 Markdown**，已清洗 HTML / 图片占位 / 无效内链，保留股票关联如 `茅台(sh600519)`；时间 `YYYY-MM-DD HH:MM:SS`）—— **可直接喂大模型**，无需再处理。⚠️ 列表**只有最新 N 条**（无翻页、无历史）⇒ 要历史用 `/v1/notice`；⚠️ 列表里的 `url` 指向**动态页、抓不到正文** ⇒ 要正文**必须**用 `id` |
| `/v1/notice` | `code` · `id` · `type` · `limit`(默认 50) · `offset`(默认 0) | **上市公司公告**。不传 `id` ⇒ 列表（`code` 必填，`type` / `limit` / `offset` **可翻页**，可回溯约 **16 年**（茅台最早一条到 2010 年））；传 `id` ⇒ 详情。⚠️ **详情两种形态**（多数公告给正文）：多数（短公告）⇒ `text` = **正文纯文本**、`url` 为空 —— **直接读 `text`**；少数（长报告 100+ 页）⇒ `text` 空、`url` = **PDF 链接** ⇒ 判据 = **先看 `text` 有没有值**，空则取 `url`（PDF 原文，用你的 PDF 阅读 / 解析工具打开）。💡 要财务数字（营收/净利）用 `/v1/finance` |

---

## 十一、期货与外汇（需 Key · 机构版）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/futures` | `code`（55 个期货 + 10 个现货商品）| 单合约快照：最新价 / 买一卖一 / 开高低 / 结算价与昨收 / 成交量额 / **持仓量 + 当日增减** / **到期日** / 52 周高低 / VWAP。⚠️ **两类标的字段不同**（按代码判断，别硬编码列数）：期货 `fu*` / `r_hd*` = **24 列**；现货商品 `hf_*`（伦敦金/银/铂、布伦特原油、LME 金属）= **16 列**，`volume` 恒 0 **且没有历史 K 线**（该市场不支持）。最新价字段是 **`lastPrice`**。⚠️ 清单 = **55 个期货 + 10 个现货**（贵金属 / 能源化工 / 基本金属 / 农产品 / 股指 / 利率 / 外汇期货）；⛔ **不覆盖内盘商品期货**、国内股指期货（IF/IC/IM/IH）、国债期货。⚠️ `isDelayed` 是延迟状态标记，**照实返回**。⚠️ `fu6*` 是 **CME 外汇期货**（有基差、有到期日），⛔ 不是即期汇率。⚠️ **机构版（¥199）专属** |
| `/v1/forex` | `code`（10 个货币对）| **10 个主流外汇现货实时报价**：USDCNY / CNH / EURUSD / GBPUSD / USDJPY / USDHKD / EURCNY / HKDCNY / CNYJPY / 美元指数。⚠️ **14 列**，最新价字段是 **`price`**（不是 `lastPrice`，与 `/v1/futures` 不同）：`code name price change askPrice bidPrice changePct high low marketStatus open prevClose symbol updateTime`。⚠️ **无成交量、无持仓量** ⇒ ⛔ 不能算量比、不能说「放量」。⚠️ `marketStatus` 是**拼接字符串**（如 `2026-11-02 09:38:49\|USDCNY_open_交易中`），⛔ 别当枚举解析；`updateTime` 是纯数字 `YYYYMMDDHHMMSS`。⚠️ **`fu6*` 是 CME 期货合约、不是即期汇率** —— 结汇 / 做账只能用本端点；**不覆盖澳元 / 瑞郎 / 加元 / 纽元即期**（那几个只有期货，走 `/v1/futures`）。⚠️ 代码必须在清单内，否则 422 并返回 10 个可用代码。⚠️ **机构版（¥199）专属** |

⚠️ **`fu6E`（CME 欧元期货）≠ `fxEURUSD`（即期汇率）**：前者含基差、有到期日；做结汇看 `fx*`。

---

## 返回形态：`data` 有四种形状（102 端点全量）

**程序化处理前必须先判形状** —— `data` **不是**永远同一个类型，写死 `data[0]["x"]` 会在 `finance` / `calendar` 上炸。

| 形状 | 长这样 | 哪些端点 | 怎么读 |
|---|---|---|---|
| **① 对象数组** | `[{"col": val}, ...]` | 多数：`quote` `kline` **`kline-full`** `hot` `technical` `chip` `orderbook` `snapshot` `profile` `dividend` `margin-trade` `ipo` | `for row in data: row["field"]` |
| **② 表列表** | `[[行...], [行...]]`（外层=表，内层=行）| `finance`（利润表 / 资产负债表 / 现金流量表）| `data[表号][行号]["字段"]` —— **先按表索引** |
| **③ 多段结构** | `{"tables": [{"title","slug","rows"}], "data": {"<slug>": rows}}` | `shareholder`（另带 `code`/`market`）· `calendar` | `data["tables"]` 保序分段；`data["data"]["<slug>"]` 便捷索引 |
| **④ Markdown 字符串** | `"\| 列 \| 列 \|\n..."` | 9 个（见信封说明）+ `events` · `dehydrated` | 优先读同响应的 `structured` / `tables`（**若存在**）；不存在才正则解析 |

**特殊 dict（不属于上面四类）**：`fund` = 扁平 `{date, close, main_net, main_net_5d/10d/20d, main_rank, lhb, lhb_details, block_trades, margin, industry_rank}` ·
`industry-chain?mode=list` = `{mode, topics}` ·
**量化组**（`backtest` · `backtest-batch` · `strategies` · `factors` · `playbooks`）= **各自一个 dict**（如 `backtest` → `{mode, strategy, universe, weighting, range, metrics, n_trades, …}`；`backtest-batch` → `{matrix, best, skipped}`；`strategies` → `{single, portfolio}`）—— ⛔ 不要把 `data[0]` 当行取。

**空结果的三种表现**（都**不是**故障，`ok:true`）：`data = []`（如 `block-trade` 当天无成交）· `data` 是含"数据为空"的 Markdown（`events`）· 多段结构里 `tables = []`。

**推荐写法（四种形状通吃）**：

```python
def rows_of(body):
    d = body.get("data")
    if isinstance(d, dict) and "tables" in d:      # ③ 多段结构
        return [r for t in d["tables"] for r in (t.get("rows") or [])]
    if isinstance(d, list) and d and isinstance(d[0], list):   # ② 表列表
        return d[0]                                 # 或按表号取
    return body.get("structured") or d              # ① / ④（④ 优先用 structured）
```

---

## 代码格式（`code` 参数）

| 市场 / 类型 | 写法 | 例 |
|---|---|---|
| 沪市 | `sh` + 6 位 | `sh600667` |
| 深市 | `sz` + 6 位 | `sz000001` |
| 北交所 | `bj` + 6 位 | `bj830799` |
| 港股 | `hk` + **5 位** | `hk00700` |
| 美股 | `us` + 代码（大写） | `usAAPL`；三大指数 `usDJI` / `usIXIC` / `usINX`（标普 500 是 `usINX`，**不是** `usSPX`） |
| ETF | 同 A 股前缀 + 6 位 | `sh510300` / `sz159915` |
| 可转债 | 同 A 股前缀 + 6 位 | `sh113052` |
| 指数 | `sh` / `sz` / `hk` 前缀 | `sh000001` 上证 · `sz399001` 深证成指 · `hkHSI` 恒生（⚠️ `cs*` 中证指数只出现在 `/v1/index-list` 清单里，取 K 线/行情会返回空） |
| 板块（申万） | `pt` + 8 位 | `pt01801780`（用于 `/v1/sector-valuation`） |
| 期货（55 个合约） | `fu` + 品种 | `fuGC` COMEX 黄金 · `fuCL` 原油 · `fuES` 标普期货 |
| 现货商品（10 个） | `hf_` + 品种 | `hf_XAU` 伦敦金（**无历史 K 线**） |
| 外汇（10 个货币对） | `fx` + 货币对 | `fxUSDCNY` · `fxEURUSD` · `fxDINIW` 美元指数 |

**简写规则（只对 A 股生效）**：

- 后缀写法：`600667.SH` / `000001.SZ` / `830799.BJ` → 自动转成 `sh600667` / `sz000001` / `bj830799`
- 纯 6 位：`600667` → 按首位推断（**5/6 → sh** · **0/3 → sz** · **4/8 → bj**）
- ⛔ **港股 / 美股 / 期货 / 外汇必须带前缀** —— `00700.HK`、`GC`、`USDCNY` 这类写法不支持

官方 SDK 会自动补市场前缀；直接调 HTTP 时建议统一用 `sh600667` 形式。

---

---

## 十二、其余端点

> 参数名与必填标记（`*`）以下方表格为准；字段语义与返回样例见 <https://ashareapi.com/endpoints/>。

### L2 大单与资金（12 个）

| 端点 | 参数（`*` = 必填）| 说明 |
|---|---|---|
| `/v1/bigorder` | code* | **单股大单资金分时**：每 1 分钟一点，`net` = 该分钟**大单净额（元）**（正 = 净买入，负 = 净卖出）。`data` 为行数组（`time` / `net`），标的级信息在顶层 `meta`：`day` 数据日期 / `max` 当日最大单分钟净买入 / `min` 最大单分钟净卖出 / `points` 点数。⭐ 累加 `net` 看大单是否持续净流入；找大额净卖出的那一分钟看砸盘。⚠️ **仅当日**（非交易日 / 盘前回最近一个交易日全天，以 `meta.day` 为准）；盘中 `points` 随交易时段增长（09:30–15:00 约 242 点）。⚠️ 是**大单口径**（按成交金额聚合），不是逐笔委托、也不是十档盘口 |
| `/v1/bigorder-flow` | code*、money、limit、offset | **逐笔大单成交**（成交额 ≥ 阈值），四方向：`direction` 1 被动卖 / 2 主动买 / 3 被动买 / 4 主动卖；行字段 `time` `direction_cn` `volume`(手) `amount`(元) `avg_price`；`money` 取 0~4 = **30万 / 50万 / 100万 / 300万 / 1000万**；`meta` 有 `money_threshold` / `total` / `returned` / `deduped` / `truncated` / 四方向 `summary`（⚠️ 截断时仅统计本次返回的样本）。单次最多约 200 笔，要全量用 `bigorder-flow-full` |
| `/v1/bigorder-flow-full` | code*、money、max_rows | **全天逐笔大单成交**：当日**每一笔**≥阈值的大单一次给全，不受 `/v1/bigorder-flow` 的 200 笔限制（flow = 盯盘看最新一段；本端点 = 复盘做统计）。行字段与 `bigorder-flow` 完全一致（`time` / `direction` / `direction_cn` / `volume` 手 / `amount` 元 / `avg_price`）。`meta`：`total` / `returned` / `raw_returned` / `deduped` / `pages` / `complete`（是否已拿全）/ `summary`（`summary_scope=all_rows`，拿全时即当日全量合计）。⭐ **要算「今天主力净流入多少」、按方向统计金额必须用它** —— 用 200 笔样本会算错 |
| `/v1/bigorder-history` | code*、limit | **单股逐日大单净额**：往回最多 **100 个交易日**，每天一个 `net`（元，正 = 净买入）。`data` 行（`date` / `net`）**倒序**；顶层 `code` / `days` / `upstream_days` / `unit`。⭐ 补 `/v1/bigorder`（只有今天）的「往回看」：判断是持续吸筹还是今天冲一下。⚠️ **固定返回 100 个交易日**，`limit` 只在本地截断（省流量不省调用）。⚠️ `net` 是**大单口径**，⛔ 不是主力净额 / 龙虎榜 / 逐笔。⚠️ 非交易日返回截至最近交易日的 100 天，以 `data[0].date` 为准 |
| `/v1/bigorder-queue` | code*、vol、tur、limit | **大单挂单明细**：当日委托量或委托金额超阈值的挂单逐笔列出。行：`time` / `order_id` / `price` / `volume`(手) / `amount`(元) / `side`(1 买 / 2 卖) / `side_cn` / `is_limit_up`(1 = 涨停价挂单) / `is_cancel`(1 = 已撤)。`meta`：`vol_threshold` / `tur_threshold` / `total` / `returned` / `truncated` + 本次样本撤单汇总 `cancel_count` / `cancel_ratio`(0–1) / `cancel_volume` / `cancel_amount`（`cancel_stats_scope="returned_rows"`，**仅统计本次返回的样本**）。⭐ 看**封单是真的还是演的**：大额买单挂上又撤 = 假封单；配合 `bigorder-flow` 分清「挂单没成交」和「真的成交」。⚠️ **仅当日**，单次最多约 200 笔 |
| `/v1/bigorder-rank` | sort、limit、offset、date | **全市场主力资金榜**（约 5,568 只）。`sort` 8 种：`net_in` 主力净流入（默认）/ `net_out` / `buy` / `sell` / `gain` 涨幅 / `loss` 跌幅 / `turnover` 换手 / `mcap` 市值。行字段含 `main_buy` `main_sell`（负数）`main_net` `turnover_rate` `amount` `market_cap` `concept` |
| `/v1/bigorder-split` | code*、date | **分钟级主力四分解**：`main_buy`(含 `active_buy` 主动买 / `passive_buy` 被动买) · `main_sell`(负数，含 `active_sell` / `passive_sell`) · `trades` 笔数 · `net`；顶层 `summary` 全天汇总 + `buy_avg_price` / `sell_avg_price` 加权均价 |
| `/v1/fund-flow` | code*、start、end | **个股资金流向**（主力/散户买卖与净额、均价、收盘价）。⭐ **沪深支持历史区间**：传 `start`+`end`（单代码）逐日返回；不传则只返回最新一行。**港股不支持历史区间**；**美股没有资金流数据**（返 `data:[]`，美股用 `/v1/fund-short`）。⚠️ 与 `/v1/fund` 不同：`/v1/fund` 是综合口径（龙虎榜+大宗+两融，仅 A 股）。⚠️ 金额单位是**元** |
| `/v1/fund-short` | code*、date | **卖空数据**（`ShortShares` / `ShortAmount` / `ShortRatio`），仅**港股 / 美股**（A 股用 `/v1/margin-trade`）。⚠️ **请传 `date`**：不传且当日数据未发布时，返回里**只有标识字段**、没有卖空数值 |
| `/v1/fund-south` | codes*、date | **港股通南下资金持仓**（持股数 / 比例 / 市值），**季度**口径、仅港股。⚠️ 不是逐日资金流 —— 要逐日净流入用 `/v1/fund-flow`。`codes` 支持逗号多只；`date` 可指定季度末 |
| `/v1/market-mood` | date | **今天短线情绪冷不冷**：破板率 + 最近 9 个交易日赚钱效应。顶层 `date` / `requested_date` / `is_fallback` / `break_count` 破板家数 / `break_rate` 破板率%（= 破板家数 ÷（破板 + 涨停）× 100）；`data` 9 行（**新→旧**）：`date` / `success_rate` 成功率% / `profit_rate` 盈利概率%（**可为负**）。⭐ `success_rate` 连降 = 情绪转冷；`profit_rate` 由负转正 = 赚钱效应回来。⚠️ 9 日序列**固定为最近 9 个交易日**、不随 `date` 变化，`date` 只影响破板率；盘中会变，缓存 5 分钟。⚠️ **机构版（¥199）专属** |
| `/v1/northbound` | date、limit | **外资（北向）在 A 股各板块的持仓**：按季度公布（实测 20 个板块）。行 `plate_code` / `plate_name` / `raw`；顶层 `date` / `requested_date` / `is_fallback` / `total_net` 区间净额(元，**可为负**) / `total_hold` 总持仓(元) / `available_dates`（7 个季度末）。🔴 **必须传季度末**：留空自动取最近季度末，传非季度末日**返回空（不是故障）**。⚠️ 这是**板块维度**（20 行 = 20 个板块），不是个股；与 `/v1/fund-south`（港股通南下）是两回事。⚠️ **机构版（¥199）专属** |

### 批量端点（10 个）

| 端点 | 参数（`*` = 必填）| 说明 |
|---|---|---|
| `/v1/chip-batch` | codes*、date | **一次拿多只的筹码分布**（获利盘比例 / 平均成本 / 90% 与 70% 集中度），**逐只标明成功与否**（`data[]` 每项 `{code, ok, data}`，另给 `requested` / `returned` / `failed`）。实测 200 只约 3.9 秒。⚠️ 与 `/v1/chip` 传逗号的区别：后者返回 N×8N 对角矩阵、无效代码的整组列会消失。**上限：专业版 200 只 / 机构版 300+** |
| `/v1/finance-batch` | codes*、periods（默认 4，最多 12）、type、fields | 一次拿多只的三大报表，**逐只标明成功与否**（`data[]` 每项 `{code, ok, data}`）。实测 **10 只 × 4 期 4.2 秒**。`type` 只取一张表（`income` / `balance` / `cashflow`，省略=三张全取）；`fields` = `all`（默认 186 列）/ `core`（69 列，载荷约 1/3）|
| `/v1/kline-batch` | codes*、period、count（默认 30）、start、end、fq | **一次拿多只的 K 线**（多只 × 同一段时间）：`data` 每项 `{code, ok, data:[...]}` —— **取几只回几个条目**，另给 `requested` / `returned` / `failed`。实测 200 只 × 30 根 = 6,000 行 **3.39 秒**。每根 8 列 `date`/`open`/`last`/`high`/`low`/`volume`/`amount`/`turnover`（与 `/v1/kline` 一致）；⚠️ **代码在外层 `data[i].code`**，行内没有 code 列。⚠️ **`fq` 可自己指定**（`qfq`/`hfq`/`nofq`）⇒ 拿后复权/原始价的途径之一。⚠️ 上限：**专业版 200 只 / 机构版 1000 只**，且 标的数 × `count` ≤ **60,000**；计费按实际返回只数（失败不计）。⚠️ `volume` 单位「手」（与 `kline-full`/`market-kline` 的「股」差 100 倍） |
| `/v1/profile-batch` | codes* | **一次拿多只公司的简况**，`data` 每项 `{code, ok, data}`（或 `error`）—— **取几只回几个条目**，另给 `requested` / `returned` / `failed`。实测 **100 只 6.8 秒**。⚠️ 与 `/v1/profile` 的区别：后者 `code` 虽支持逗号但返回**扁平行、无逐只状态**，无效代码**不报错直接丢弃**。⚠️ 上限：**专业版 100 只 / 机构版 150 只**，计费按实际返回只数。⚠️ **仅 A 股** |
| `/v1/quote-batch` | codes*、period、count、start、end | **一次拿多只的行情**，`data` 每项 `{code, ok, data}`（或 `error`）—— **取几只回几个条目**，另给 `requested` / `returned` / `failed`。实测 **沪深300 全 300 只 4.16 秒**（循环单只约 3.5 分钟）。⚠️ 与 `/v1/quote` 的区别：后者返回**扁平行、不带逐只状态**（缺了哪只要自己算）。⚠️ 上限：**专业版 200 只 / 机构版 1000 只**，计费按实际返回只数。⚠️ `period` 默认 `day`、`count` 默认 **1** |
| `/v1/scanner` | q* | 把自然语言条件交给**选股员**，返回候选池 + 引用 + 工具轨迹（`x_tool_trace`）。⚠️ **BYOK**：必须带 `X-LLM-Key`（模型 Key）+ 本服务 API Key，模型 token 由客户自付。⚠️ **额度独立**：专业版 2,000 次（生命周期）/ 机构版 10,000 次每月，不占数据 API 总池。⚠️ 只有 `ok:true` 且**结果非空**才扣次数（失败 / 空结果退回） |
| `/v1/scanner/snapshots` | limit | 返回**当前 Key** 的最近选股快照（含前向收益汇总）。**只读、不扣 scanner 次数** |
| `/v1/shareholder-batch` | codes* | **一次拿多只的股东研究**，`data` 每项 `{code, ok, data}` —— `data` 内结构与 `/v1/shareholder` **完全一致**（`market` + `tables` + `data{slug}`），切换不用改解析；另给 `requested` / `returned` / `failed`。实测 **200 只 4.1 秒 / 300 只 5.6 秒**。⚠️ 与单只端点的区别：后者 `code` 传逗号返回**一大坨 markdown、无逐只状态**，无效代码**不报错直接消失**。⚠️ 上限：**专业版 200 只 / 机构版 300 只**，按实际返回只数计费。⚠️ **支持沪深 A 股 + 港股**（可混传）；北交所/ETF/指数/美股会标 `ok:false` |
| `/v1/snapshot-batch` | codes* | **一次拿多只的完整画像**（35+ 字段），`data` 每项 `{code, ok, data}`，另给 `requested` / `returned` / `failed`。实测 **300 只 0.40 秒**（比 `/v1/quote-batch` 快 10 倍）。⚠️ 上限：**专业版 200 只 / 机构版 250 只**，按实际返回只数计费。⚠️ **仅 A 股**（`sh`/`sz`/`bj`）；港股/美股会标 `ok:false` 并提示改用 `/v1/quote`（⛔ 不返错数据）。⚠️ **单位**：`volume` 手 · `amount` **万元** · 市值 亿元 · 股本 股 |
| `/v1/technical-batch` | codes*、date | **一次拿多只的 55 项技术指标**，`data` 每项 `{code, ok, data}` —— 行内结构与 `/v1/technical` **单行完全一致**，另给 `requested` / `returned` / `failed`。实测 **500 只 1.2 秒 / 1000 只 1.8 秒**（循环单只约 8 分钟）。⚠️ 上限：**专业版 500 只 / 机构版 1000 只**，按实际返回只数计费。⚠️ `date` 对所有代码同时生效，非交易日回退（以返回行 `date` 为准）。⚠️ **只有日线口径**。⚠️ A 股（含北交所）/ 港股 / 美股**可混传** |

### 打板 / 情绪 / 风控（7 个）

| 端点 | 参数（`*` = 必填）| 说明 |
|---|---|---|
| `/v1/broken-board` | date、limit | **某日涨停被砸开（炸板）的票** + 概念标签。⭐ 与 `/v1/limit-up` 互补：涨停池是**封住的**，本端点是**没封住的** —— 两者一比就是当天封板质量。`date` 留空 = 最近工作日（周末回退上周五），节假日请显式传；`is_fallback=true` 表示没拿到你指定的那天，以顶层 `date` 为准。⚠️ **机构版（¥199）专属** |
| `/v1/limit-reason` | code*、date、limit | **「这只票为什么涨停」**：每次涨停的**完整原因文案** + 板块 + 当日地位。行（**新→旧**）：`date` / `dragon_rank`（日内龙几，空 = 非龙头）/ `plates` / `reason` / `concept`。⭐ 与 `/v1/limit-up` 分工：涨停池给**今天全市场**，本端点给**单只的历史**。⚠️ 返回该股历次涨停**全部记录**，`date` 不用于筛选。⚠️ `code` 必须 A 股。⚠️ **机构版（¥199）专属** |
| `/v1/new-high` | date、limit | **哪些题材今天在创百日新高**：按题材汇总家数（实测 18 个题材）。行字段 `theme` / `plate_code` / `raw`；顶层 `date` / `requested_date` / `is_fallback`。⚠️ 不保证历史：`is_fallback=true` 表示没拿到你指定的日期，以 `date` 为准。⭐ 与 `/v1/sector`（板块涨幅榜）对照，看是「涨得多」还是「创新高多」。⚠️ **机构版（¥199）专属** |
| `/v1/score` | codes*、date | **股票评分**（仅 A 股）：`basic` 基本面 / `technical` 技术 / `composite` 综合 / `fund` 资金 / `risk` 风险，**均为 0~100**（越高越好），每维带 `chg_week` / `chg_month` / `chg_quarter`。⚠️ **`chg_quarter` 不是 0**：评分**每季度重置** ⇒ 季度变动 = 本季累计（通常等于 `value`）；要「季度环比」请自己减上季末。⚠️ `codes` 支持逗号多只。⚠️ `date` 查历史，**最早只到 2026-04 下旬**（更早为空，不是故障） |
| `/v1/stocks` | market、industry、limit、offset | **一次拿全 A 股约 5,576 只**：`code`（`sh600519`）/ `name` / `market`（sh/sz/bj）/ `listedDate` / `industry` / `sector` / `issuePrice` / `regCapital`；返回 `total`（符合条件总数）/ `returned` / `data`。⚠️ 某字段为 `'-'` = 该标的本就没有这项（如个别次新股未归档），**不是取数失败**。⚠️ 口径是**当前在册**（已退市不在内，新股自动补入）。⚠️ 全量约 **1 MB** ⇒ 日常带 `limit` 分页，或只在初始化时全量拉一次 |
| `/v1/suspension` | market | **当日停复牌清单**：哪些票停牌、哪些复牌、停牌原因。⚠️ **三市场**：`market=沪深`（默认）/ `港股` / `美股`（也接受 `hs` / `hk` / `us`）。⚠️ `suspendDate` 是**完整日期**（`2026-10-13`），不是截断到月。⚠️ **选股后过滤停牌股用这个**：`/v1/screen` 的筛选**不剔除停牌**，拿到候选请与本清单交叉核对 |
| `/v1/tail-chase` | limit、sort | **尾盘资金在抢哪些票**（全市场约 292 只）。行：`code` / `name` / `fund_tag`（如「基金」，空 = 无）/ `theme` 题材 / `change_pct` / **`chase_amount` 抢筹金额（元）** / `masked` / `raw`。⚠️ **前 4 行的代码与名称被隐藏**（`600***` / `****`），金额仍完整；`masked=true` 的行**不要当标的用**。⭐ 已按 `sort` 重排（默认 `chase_amount` 降序），第一条即当日抢筹最大。⚠️ 覆盖**最近交易日**（不支持按日期回看）。⚠️ **机构版（¥199）专属** |

### 资讯 / 研报 / 评级（7 个）

| 端点 | 参数（`*` = 必填）| 说明 |
|---|---|---|
| `/v1/analyst` | snapshot_id*、focus、horizon | **复盘分析师**：输入 `snapshot_id`，读取该快照的 picks 与 T+1 / T+5 / T+20 评估，输出收益 / 基准 / 超额 / 命中率、赢家输家、数据缺口与复盘报告。⚠️ **BYOK 可选**：带 `X-LLM-Key` 用模型润色，不带则返回确定性复盘。⚠️ **只读**（不改快照 / 评估，不选股、不预测） |
| `/v1/consensus` | codes* | **卖方一致预期**：目标价 + 未来年度/季度预测（EPS / 营收 / 净利润 / 预测 PE·PB·PS）。⚠️ **单次 ≤15 只，超过会丢数据**（20 只只回 6 只）。⚠️ 字段按市场不同：**A 股有 `targetPrice`**、**港股没有目标价**；⚠️ `institutionCnt`（机构覆盖数）**恒为 null**（该字段无有效值）|
| `/v1/disclosure` | codes* | **业绩预约披露日**：`disclosureDate` 披露日 / `reportEndDate` 报告期 / `disclosureDesc` 说明。**三市场**：A 股 / 港股 / 美股。⚠️ 与 `/v1/calendar`（分红 / 解禁 / 会议等）**不是一回事**，本端点只覆盖财报披露日。⚠️ **港股 `disclosureDate` 常为空**，日期写在 `disclosureDesc` 文案里（如「将于 2026-11-18 发布财报」） |
| `/v1/evidence` | q*、scope、limit | **一次查询、多源取证**：同时检索**交易所公告**（沪深官方一手）与**财经资讯**，合并成一张表并去重转载。行：`source`（`cninfo` 公告源 / `eastmoney` 资讯源）/ `kind`（`notice` / `news` / `report`）/ `title` / `url` / `date` / `code` / `name` / `media` / `authority`（1.0 官方 · 0.5 门户）/ `relevance`（1.0 命中实体 · 0.6 仅摘要 · 0.3 未确认）/ `relevance_where`（`title` / `name` / `snippet` / `unknown`）/ `snippet`（**资讯才有**；公告正文在 PDF 里）/ `also_on`（同消息的其它转载）。⭐ **每行带证据三件套**：`cit_endpoint` / `cit_params` / `cit_field_path` / `cit_value_hash`（16 位）/ `cit_hash_alg`（`sha256-v1`）/ `cit_retrieved_at`。⭐ **指纹可自证**：重取后找 `date`+`title` 都同的一行，算 `sha256(endpoint \| 按 key 排序的 k=v 用 & 连 \| field_path \| JSON(标题) \| 日期)` 取前 16 位应相等。顶层 `meta`：`trace` / `counts` / `counts_kind` / `related`。⭐ 排序 = `relevance` → `authority` → `date`（同级公告在资讯前）。⭐ `scope=report` 可一并要研报（单独算名额、**不额外计费**，无摘要）。⚠️ 公告返 **PDF 链接**、资讯返原文链接、研报返详情页；结果缓存 5 分钟；`scope` 默认 `notice,news` |
| `/v1/flash` | limit、index | **全市场财经快讯**（不需要代码；按个股消息用 `/v1/news`）。行字段 `id` / `time` / `title` / `content` / `source` / `url`。⚠️ `limit` **上限 200**；翻页用 `index`（从 0 起，步长=上次 `limit`，如 `limit=20&index=20` 是第二页），只能往回翻、没有日期参数。⚠️ 缓存 **1 分钟**：同一分钟内多次请求返回同一批，不重复消耗 |
| `/v1/rating` | codes* | **卖方机构评级**：目标价（均值 / 最高 / 最低）+ 评级分布（买入 / 增持 / 中性 / 减持 / 卖出 + 覆盖机构数）+ **评级月度趋势**。⚠️ **只支持港股 / 美股**（`hk00700` / `usAAPL`）；**A 股没有卖方评级，请用 `/v1/consensus`**。⚠️ `codes` 支持逗号多只，每只一段（按 `#### <代码>` 分段，正文在 `tables`） |
| `/v1/report` | code、id、limit、offset | **卖方研报**：不传 `id` ⇒ 列表（标题 + 机构 + 评级 + 类型 + 时间）；传 `id` ⇒ ⭐ **研报全文**（Markdown，含财务点评）。**A 股 / 港股**都覆盖。⚠️ **列表 `limit` 上限 20**（传更大 **422**），翻页用 `offset`；「共 N 条」是历史总数。⚠️ **条数不精确**（实测 `limit=3` 回 4 条），⛔ 别按条数做严格校验。⚠️ **没有时间范围参数**，按时间找只能翻页。⚠️ `tzpj` 是投资评级（买入 / 增持 / 中性 / 减持 / 卖出），**可能为空**。⚠️ 与 `/v1/dehydrated`（要点摘要）互补 |

### 自选 / 指数 / 其它（6 个）

| 端点 | 参数（`*` = 必填）| 说明 |
|---|---|---|
| `/v1/buyback` | code*、start、end | **公司自己买自己**（与 `/v1/shareholder` 谁持有不同）。⚠️ **返回结构按市场不同，不能同一套列名解析**：A 股 ⇒ 回购事件概要（`code` / `name` / `market`）；港股 ⇒ 逐日明细（`date` / `BuybackMoney` / `BuybackPrice` / `BuybackShares` / `BuybackCumMoney` / `closePrice`）|
| `/v1/index-constituent` | code* | **指数成分股全量清单**（一次给全，不受条数上限）：`sh000300` 返回 300 只。⚠️ **一次只查 1 个指数**（逗号多只返回空）。⚠️ **字段按市场不同**：A 股指数据 `code` / `name` / `IndexName`；**港股指数用中文键** `代码` / `名称` / `涨跌幅` / `成交额`。⚠️ **只有成分与名称，没有权重**（权重要用 `/v1/etf?kind=持仓`）|
| `/v1/lhb-agency` | date、sort、limit | **全市场机构榜**：某交易日机构席位参与过的**所有个股**一次拿完（实测单日 51 只）。行字段（金额**元**）：`net_buy` 机构净买入（**负值 = 净卖出**）/ `join_num` 参与机构家数 / `change_pct` / `turnover` 成交额 / `amplitude` / `turnover_rate` / `float_cap` / `market_cap` / `fengkou_plates`（板块代码，**不含板块名称**）。顶层 `date` / `requested_date` / `is_fallback` / `total` / `returned` / `sort` / `unit`。`sort=net_buy` 看机构今天真金白银买了谁。⚠️ 不保证历史：`is_fallback=true` 即以 `date` 为准。⚠️ **机构版（¥199）专属** |
| `/v1/lhb-seats` | code*、date | **某只票某次上榜的营业部席位明细**（最多约 10 个）：`name`（营业部）/ `total_buy` / `total_sell` / `net`（净买 = 买 − 卖）/ `is_youzi`（游资标记）/ `log_id`；顶层 `meta` 含 `code` / `name` / `date` / `qjzf`（区间涨幅%）/ `rows`。⭐ 比机构榜更具体：能看出是沪股通专用、某营业部还是游资。⚠️ 盘后数据：`date` 留空 = 最近一次上榜日。⚠️ **机构版（¥199）专属** |
| `/v1/watchlist` | action、code、codes、list、name、note、tags | 按 API Key 隔离的自选股：`action=list` 查 / `add` 加 / `remove` 删 / `export` 导出 CSV。⚠️ **CRUD 不扣数据次数**。`code` 单只；批量用 `codes=600519,000001,300750`，**逐只返回结果**（单只失败不影响整批）。⚠️ 档位限额（列表数 / 每列表只数）：体验版 **1 / 20** · 标准版 **3 / 100** · 专业版 **10 / 500** · 机构版 **50 / 2000** |
| `/v1/watchlist/quotes` | list | 一次查询自选股最新行情。⚠️ **正常扣 1 次数据额度**（与 CRUD 不同） |

### Agent / 对话接口（7 个）

| 端点 | 参数（`*` = 必填）| 说明 |
|---|---|---|
| `/v1/agent-ask` | q*、scope、max_results、recency | **开箱即用问答**：服务端取数后生成一段带 `[ref_N]` 内联引用的答案，你不用自己编排。与 `/v1/agent-search` 的区别：那个返回**结构化候选 + 证据**，不生成答案。🔑 **BYOK**：请求头 `X-LLM-Provider`（`deepseek` / `openai` / `moonshot`）+ `X-LLM-Key` + 可选 `X-LLM-Model`；Key **只在本次请求的内存里用，不保存、不写日志**。⚠️ **不带头也能用**：只返回证据、不生成答案（`answer: null` + `degraded: "no_llm_key"`），证据与裁决照常返回。响应：`answer` + `citations[]`（来源 / 取值 / `value_hash`）+ `verification`（逐条结论的核验记录）+ `citation_check`（**机械校验有无编造引用**）+ `usage`（你的 token 用量） |
| `/v1/agent-research` | q*、depth（`fast` / `standard` / `deep`）| **异步研究**：POST 提交 → 拿 `task_id` → 轮询 `/v1/agent-research/{task_id}`（⭐ **查询不扣额度**）。`depth`：`fast` 30–90s / **`standard` 默认** 2–5min / `deep` 5–15min（预算 = 工具调用次数 5/12/25）。BYOK 可选，不带头只取证不给报告。⚠️ 你的 key **不会被保存** ⇒ **服务器重启会中断未完成任务**（状态 `interrupted`，需重提） |
| `/v1/agent-research/{task_id}` | task_id* | **查研究任务**：`status` = `queued` → `running` → `done` / `failed` / `interrupted`；`progress[]` 记录取数过程；`done` 时给 `report`（`answer` + `citations` + `verification` + `citation_check` + `usage`）。只能查自己提交的；查询不扣额度 |
| `/v1/agent-search` | q*、scope（`ashare` / `notice,news,report` / `web` / `wechat` / `a2b` / `xhs` / `local`；不传=自动选）、depth（当前只支持 `fast`）、max_results、clarify、claim、replay、authority_min（默认 0=不过滤；`0.6` 只要官方一手）、recency（`7d` / `24h`；超出窗口不丢弃，只在 verification 里标 `unverified`）| **自然语言 → 带证据链的结构化候选**，供你自己编排；**不生成答案**。每行带 `evidence`：`endpoint` / `params` / `field_path` / `value` / `value_hash`（16 位）/ `hash_alg` —— 拿 `endpoint`+`params` 重取并按同一记录重算 sha256，应得同一 `value_hash`（可自行复算校验）。顶层另有 `interpreted`（标的 + 意图 + `intent_source`）。⚠️ **只有两个通道**：`ashare`（资金流 / 行情价格）与 `notice,news,report`（公告 / 资讯 / 研报，每行带 `kind` / 标题 / 媒体） |
| `/v1/chat/completions` | 无 | OpenAI Chat Completions 协议（OpenAI SDK / Cherry Studio / ChatBox / OpenWebUI 等）。`base_url = https://api.ashareapi.com/v1`；`apiKey = ct-xxx:sk-yyy`（前半本产品 Key，后半你的模型 Key）。`model` 支持 `ashare/deepseek-flash` / `gpt-5.6-luna` / `claude-*` 等；`stream=true` 走 SSE。⭐ 选股员：`model=ashare/scanner@deepseek-flash`（专业版 ¥99+），响应带 `x_citations` 与 `x_tool_trace`。⚠️ 首版**忽略 `tools`**；要 Anthropic 协议用 `/v1/messages` |
| `/v1/messages` | 无 | Anthropic Messages 协议接入点（Claude Code / Anthropic SDK · BYOK）。`x-api-key` 写成 `ct-xxx:sk-ant-yyy`（前半本产品的 Key，后半你的 Anthropic Key）；`max_tokens` 必填；支持 **SSE 流式**（`stream=false` 返完整 message）。⚠️ 首版**不支持 `tools`** —— 普通聊天可用，Claude Code 的文件/终端工具不在支持范围。⚠️ 要 DeepSeek / OpenAI 模型请用 `/v1/chat/completions` |
| `/v1/responses` | 无 | OpenAI 新一代 Responses 协议（Codex / openai SDK 2.x · BYOK）。`input` 支持字符串或消息数组；`instructions` **由服务端丢弃**（不可覆盖）；`apiKey = ct-xxx:sk-yyy`；`stream=true` 发 **9 个标准 SSE 事件**，`false` 返完整 JSON。⭐ 选股员：`model=ashare/scanner@deepseek-flash`（专业版 ¥99+），响应带 `x_tool_trace`。⚠️ 首版**不实现** `previous_response_id`，上下文请放 `input` |