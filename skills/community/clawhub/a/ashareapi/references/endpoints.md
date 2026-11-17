# 端点清单（40 个）

- **统一前缀**：`https://api.ashareapi.com/v1`
- **统一信封**：`{ ok, endpoint, tier, elapsed_ms, source, data }` —— 只有这 6 个键
  - ⚠️ **`structured` / `tables` 是【条件字段】，不是每个端点都有**：**只有 `data` 是 Markdown 文本时才附**
    （`market-overview` · `changedist` · `lhb` · `sector` · `sector-valuation` · `bond` · `etf` · `screen` · `macro`）。
    **其余端点没有这两个键** → `body["structured"]` 会 **KeyError**，**一律用 `body.get("structured")`**。
  - ⚠️ **4 个端点信封不同**（都**没有 `data`**）：`/v1/health` = `{ok, uptime_s, data_ready, tiers}` ·
    `/v1/challenge` = `{challenge, difficulty, expires_in, how_to}` · `/v1/usage` = `{ok, day, calls_today, tier, total_calls, total_quota, total_left, daily_quota, per_min}` ·
    `/v1/ip-whitelist` = `{ok, ips, enabled, max_ips}`（`GET`；`POST`/`DELETE` 为 `{ok, ips, enabled}`）
- **参数带 `*` = 必填**
- **实时规格**：`GET https://api.ashareapi.com/openapi.json`（本文件据其生成）

---

## 一、免费端点（无需 Key，5 个数据端点 + 2 个工具端点）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/quote` | `code*` | 实时行情：`last` 现价 / `open/high/low` / `volume`（手）/ `amount`（元）/ `turnover` 换手率% / `date`。**最新一根 = 当日实时** |
| `/v1/kline` | `code*` · `period`(day/week/month/season/year/**m1/m5/m15/m30/m60/m120**) · `count`（默认 30，最大 **1212**；**匿名最多 250**）· `start`/`end`（仅 day 与分钟线，须配对）| OHLCV 历史 K 线。⚠️ **分钟线属付费层**（日/周/月/季/年免费），窗口近 1 个月，不支持 北交所/期货/外汇。复权口径**由服务端固定**（无 `adjust` 参数）：日线及以上前复权（除权除息日不跳空），分钟线不复权 —— **不要再自己复权**（会二次复权）|
| `/v1/minute` | `code*` · `days`（`1` 当日 · `5` 近 5 个交易日，**只有这两档**）| **分时**：盘中每分钟的价格与累计成交量。⚠️ 与 `/v1/kline` 的**分钟 K 线不是一回事**（前者分时、后者 OHLC 蜡烛）。⚠️ **付费端点** |
| `/v1/hot` | `limit`（默认 30，**上限 50**）| 全市场热搜榜（A股/美股/ETF）：关注度排名 + 涨跌幅 |
| `/v1/market-overview` | `type`(summary/trade/interval/technical/margin/**valuation**/**rotation**) | 大盘画像。`valuation` = 中证全指 PE/PB/PS **历史百分位**；`rotation` = 风格轮动（大小盘/成长价值）。⚠️ `type=updown` 是 **T-1 口径**，涨跌家数请用 `/v1/changedist` |
| `/v1/changedist` | 无 | **当期**涨跌家数 / 涨跌停家数 / 停牌 / 成交额 / 区间分布 —— **市场广度推荐入口** |
| `/v1/health` | 无 | `data_ready=true` 表示数据通道可用（不含内部实现细节）|
| `/v1/challenge` | `difficulty` | PoW 挑战（匿名提额用）。解 nonce 后带 `X-PoW: <challenge>.<nonce>`，匿名配额 5 → 15 次/分（**只提每分钟次数，每日条数上限不变**）|

---

## 二、行情与技术（需 Key）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/technical` | `code*` | MA / MACD / KDJ / RSI / BOLL 全家桶 |
| **`/v1/kline-full`** | `code*` · `fq`(qfq/hfq/bfq/nofq，**默认 qfq**) · `start` · `end` | ⭐ **A股全历史日线**（一次拿到**全部日线**，实测约 **2465 根**，2016-08-08 起 —— 而 `/v1/kline` 上限 1212 根）。⚠️ **`fq` 可选且默认 `qfq`**（与 `/v1/kline` 的"服务端固定"不同）⇒ 本端点**可以**自己指定复权口径。⚠️ **日期字段名是 `time`**（不是 `date`！其余 K 线端点用 `date`）；字段 = `time/open/high/low/close/volume/amount`。⚠️ 属付费层 |
| `/v1/chip` | `code*` | 筹码分布与持仓成本（获利盘 / 套牢盘比例）|
| `/v1/orderbook` | `code*` | **五档盘口（order book）**：买一~买五 / 卖一~卖五的**价 + 挂单量（手）**。字段：`b1_p`/`b1_v`~`b5_p`/`b5_v`（买档）、`a1_p`/`a1_v`~`a5_p`/`a5_v`（卖档）。⚠️ **秒级快照（10 秒缓存）· 盘中才有意义**；量单位是**手**（×100 = 股）；**跌停买档全 0 / 涨停卖档全 0**（正常）|
| `/v1/snapshot` | `code*` | **全字段行情画像（35 字段）**：`code/name/sec_type/currency/status` + 价格（`price/prev_close/open/high/low/avg_price/change/change_pct/amplitude/speed`）+ 量（`volume/amount/turnover/outer_vol/inner_vol/volume_ratio`）+ 估值（`pe_ttm/pe_dynamic/pe_static/pb`）+ 市值股本（`float_market_cap/total_market_cap/float_shares/total_shares`）+ 涨跌停（`limit_up/limit_down`）+ 盘口（`bid/ask/bid_ask_diff`）+ `time`。⚠️ **与 quote 分工**：quote 轻（8 字段）免费 / snapshot 全（**35 字段**）付费，**只要现价用 quote 更轻**；✅ **计费=次数**：要估值+市值+股本+涨停价**多项**时，本端点 1 次搞定——比分别调 quote/valuation/orderbook **更省次数**。⚠️ **仅 A 股**（港股/美股字段布局不同，用 quote）——**传其他市场返回空，不返回错数据**|
| `/v1/search` | `q*` | 按名称/代码搜股票、基金、板块 —— **用户只给名称时先搜代码** |
| `/v1/profile` | `code*` | 公司简况：上市日期 / 主营业务 / 所属行业 |

## 三、财务

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/finance` | `code*` · `num`（期数）| 利润表 / 资产负债表 / 现金流量表（多期）。营收 / 净利 / 毛利率 / 负债。⚠️ **`data` 是【表列表】`[[行...], [行...], ...]`**（外层=表，内层=行）→ **先按表索引再按行**：`data[0][0]["..."]` |
| `/v1/dividend` | `code*` · `years` | 分红送转历史：每股分红 / 送股 / 除权日 |
| `/v1/shareholder` | `code*` | 十大股东 / **股东户数（筹码集中度）** / 机构持仓。⚠️ **`data` 是【多段结构】**：`{code, market, tables: [{title, slug, rows}], data: {slug: rows}}`，slug = `top10_holders` / `top10_float_holders` / `holder_count` |

## 四、资金与交易（核心）

| 端点 | 参数 | 返回要点 |
|---|---|---|
| **`/v1/fund`** | `code*` | ⭐ **一接口拿全交易面**：主力资金（当日/5/10/20 日净流入 + 全市场排名）+ 龙虎榜（上榜原因 / 买卖总额 / **营业部明细**）+ 大宗交易 + 融资融券。**问"主力资金/资金流/龙虎榜"优先用它**。⚠️ `data` 是**扁平 dict**（不是多段）：`{date, close, main_net, main_net_5d/10d/20d, main_rank, lhb, lhb_details, block_trades, margin, industry_rank}` |
| `/v1/lhb` | `type`(institution/hotmoney/activeseat) · `date` | 龙虎榜**分榜**：机构榜（机构数 / 机构买入 / 净买）· 游资榜 · 活跃席位榜 |
| `/v1/margin-trade` | `code`（**必填**，支持 `sh600667,sz000651` 批量）· `date` | 融资余额 / 买入 / 偿还 / 融券。未披露日上游会给出原因 |
| `/v1/block-trade` | `code` · `date` | 大宗交易：成交价 / 折溢价 / 量 / 买卖方营业部 |
| `/v1/events` | `code*` | 个股事件总览：**42 类**（大宗 / 龙虎榜 / 回购 / 定增 / 分红 / 业绩 / 解禁 …）|
| `/v1/calendar` | `date` · `limit` | **个股**事件日历（分红派息 / 解禁 / 财报披露排期）。**不是宏观日历**（宏观用 `/v1/macro`）。⚠️ **`data` 是【多段结构】**：`{tables: [{title, slug, rows}], data: {slug: rows}}`，**按事件类型分段保序**；slug 取值 = `financial_report` / `dividend` / `ipo` / `meeting` / `lockup_release` / `rights_issue` |

## 五、板块与产业链

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/sector` | 无 | 行业 / 概念 / 地域板块涨幅榜 + 领涨股 |
| `/v1/sector-valuation` | `code*`（`pt01801780` 形式）| 申万板块 PE/PB/PS/PCF + 股息率 + **历史百分位** |
| `/v1/industry-chain` | `mode`(list/graph/stock) · `topic` · `code` | `list` = **183 个主题** · `graph&topic=X` = 图谱（关联个股 + 节点 + 上中下游）· `stock&code=X` = 该股所属链（主题/节点/位置/**关联度**/业务描述）|

## 六、可转债 / ETF / 新股

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/bond` | `code*`（`sh113052`）| 转债完整条款：溢价率 / 转股价值 / **双低值** / **强赎触发价** / 回售触发价 / 转股价 / 正股 / 到期日 / 信用评级 |
| `/v1/etf` | `code*`（`sh510300`）| ETF 行情 / 规模 / 溢折率 / 资金流 |
| `/v1/ipo` | `days` | 新股发行 / 申购 / 中签 / 上市日历 |

## 七、选股与宏观

| 端点 | 参数 | 返回要点 |
|---|---|---|
| `/v1/screen` | `expr` 或 `preset` · `limit` · `orderby` · `desc` · `market` | **因子选股**。`expr` 多因子交集：`intersect([PE_TTM > 0, PE_TTM < 20, ROETTM > 15])`；`preset` 22 个官方预设（**大小写/下划线不敏感**：`low_pe` = `LowPE`）。常用因子：PE_TTM / PB / PS_TTM / TotalMV / DividendRatioTTM（估值）· ROE / ROETTM / ROIC / GrossIncomeRatioTTM（盈利）· OperatingRevenueGrowRate / NPParentCompanyYOY（成长）· CurrentRatio / DebtAssetsRatio（负债）· NetOperateCashFlowTTM（现金流）|
| `/v1/macro` | `region`(cn/us/jp/eu/hk) · `names` | 宏观：GDP / CPI / PMI / LPR / 国债收益率 / 财政 |
| `/v1/dehydrated` | `mode`(list/detail) · `symbol` · `limit` | 券商研报脱水摘要 |
| `/v1/usage` | 无 | 当前 Key 的今日调用次数 / 剩余总量 / 到期时间 / 限流额度 |

---

## 八、量化回测与因子（需 Key · Standard 起）

> ⭐ 想"用策略跑历史收益"用这里。**先查清单再调用**：有哪 20 条单标的策略 / 9 条组合策略，先调 `/v1/strategies`。

| 端点 | 参数 | 返回要点 |
|---|---|---|
| **`/v1/backtest`** | `mode`(**single** 默认 / portfolio) · `strategy` · `code`（single 必填）· `start` · `end` · `initial_cash`（默认 100 万）· `weighting`(equal/inv_vol) · `include_equity` | ⭐ **量化回测**。`mode=single` **单标的择时·实时算**（毫秒级，传 `code` + `strategy`）；`mode=portfolio` **组合选股·查预计算**（传 `strategy`）。返回 `metrics`（`total_return` / `cagr` / `sharpe` / `max_drawdown` / `ann_vol` / `final_nav`）+ `n_trades` + 可选 `equity` 净值曲线。⚠️ **组合只认预置区间**（省略 `start`/`end` = **全周期**；传其他区间会返回此刻可用的 `available_ranges` 清单，不用猜）。⚠️ 成本已计入：佣金万三（最低 5 元）/ 印花税 0.05% / 滑点千一 + 涨跌停 / 停牌约束 |
| `/v1/backtest-batch` | `codes*` · `strategies` · `start` · `end` · `initial_cash` | **批量回测**（多标的 × 多策略对比矩阵）。返回 `matrix`（每题每策略的 metrics）+ `best` + `skipped`。⚠️ **上限：标的 ≤20 · 策略 ≤10 · 组合 ≤60**（超限直接报错，⛔ 不静默截断）；**单票失败不中断整批** |
| `/v1/strategies` | 无 | **策略清单**：单标的 20 条（`buy_hold` `low_vol` `dca` `vol_target` `ma_stop` `ma_cross` `grid` `mom20` `turtle` `rev5` `breakout` `atr_stop` `macd` `rsi` `boll` `kdj` `wr` `obv` `cci` `sar`）+ 组合 9 条（`buy_hold_equal` `lowvol20` `mom20` `mom20_ex_st` `rev5` `ma_cross` `volume_breakout` `smallcap` `largecap`），各含**参数白名单**（名称/类型/最小/最大/默认）。⚠️ **静态清单，不占重型额度** |
| `/v1/factors` | `category` · `kind` | **因子库**：88 个因子 + 50 个筛选入口 + 22 个预设组合。⚠️ `category` / `kind` **只接受中文枚举值**；要用因子实际选股，用 `/v1/screen` |
| `/v1/playbooks` | `category` · `id` | **方法论库**：13 条「怎么判断市场」流程（含判据 / 阶段 / 实测证据）—— 给 AI 的"判断方法论"，不是数据 |
| `/v1/ip-whitelist` | GET 无 · POST `ips` · DELETE `target_key`（仅客服）| **IP 白名单**（把 Key 锁到固定 IP，外泄也用不了）。`GET` 查 / `POST` 设（覆盖式，最多 50 个精确 IP，⛔ 不支持网段）/ `DELETE` 清空。⚠️ **属 Unlimited 档**；⚠️ **三个方法都要求"当前 IP 在名单内"** —— 换网络被锁死请联系客服 |

---

## 返回形态：`data` 有四种形状（40 端点全量）

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

| 写法 | 说明 |
|---|---|
| `sh600667` | 沪市（sh）· 深市（sz）· 北交所（bj）· 港股（hk）· 美股（us）|
| `600667.SH` | 后缀写法 |
| `600667` | 纯 6 位（按首位推断：5/6→sh · 0/3→sz · 4/8→bj）|
| `pt01801780` | **板块**代码（申万板块，用于 `sector-valuation`）|
| `sh113052` | **可转债**代码 |
| `sh510300` | **ETF** 代码 |

**官方 SDK 会自动归一化三种股票写法**；直接调 HTTP 时建议统一用 `sh600667` 形式。
