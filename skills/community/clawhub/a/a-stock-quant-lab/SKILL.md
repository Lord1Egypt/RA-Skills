---
name: a-stock-quant-lab
description: |-
  A 股量化实验室：基于 zvt 框架的数据采集 + 因子研究 + 回测执行一站式。
  覆盖 31 个场景——机构持仓、财报、指数成分、MACD/MA/量能择时。仅限中国 A 股。
license: MIT-0
compatibility: Python 3.12+, uv package manager. Network access to eastmoney / joinquant / baostock / akshare for data fetch.
metadata:
  version: "v6.1"
  blueprint_id: "finance-bp-009"
  compiled_at: "2026-04-20T07:34:47.524525+00:00"
  capability_markets: "cn-astock"
  capability_activities: "data-sourcing, backtesting, factor-research"
  sop_version: "crystal-compilation-v6.1"
  openclaw:
    emoji: "📈"
    skillKey: a-stock-quant-lab
    category: finance
    primaryEnv: python
    requires:
      bins: ["python3", "uv"]
---
# A 股量化实验室 (a-stock-quant-lab)

> 说出"跟机构持仓"或"MACD 回测"——我基于 zvt 直接写代码跑起来，不用你翻文档。 美股数据质量一般，不推荐。

## Pipeline

`data_collection -> data_storage -> factor_computation -> target_selection -> trading_execution -> visualization`

## Top Use Cases (31 total)

### Actor Data Recorder (`UC-101`)
Collects institutional investor holdings and top 10 free float shareholders on a weekly schedule for tracking major player positions
**Triggers**: institutional investor, top holders, actor data

### Financial Statement Recorder (`UC-102`)
Collects fundamental financial data including balance sheets, income statements, and cash flow statements from eastmoney on a weekly basis
**Triggers**: financial statements, balance sheet, income statement

### Index Data Recorder (`UC-103`)
Collects index metadata, index compositions (SZ1000, SZ2000, growth, value indices), and daily index price data
**Triggers**: index data, index composition, SZ1000

For all **31** use cases, see [references/USE_CASES.md](references/USE_CASES.md).

**Execute trigger**: `When user intent matches intent_router.uc_entries[].positive_terms AND user uses action verb (run/execute/跑/执行/backtest/fetch/collect)`

## What I'll Ask You

- Target market: A-share (default), HK, or crypto? (US stocks in ZVT are half-baked — stockus_nasdaq_AAPL exists but coverage is thin)
- Data source / provider: eastmoney (free, no account), joinquant (account+paid), baostock (free, good history), akshare, or qmt (broker)?
- Strategy type: MACD golden-cross, MA crossover, volume breakout, fundamental screen, or custom factor?
- Time range: start_timestamp and end_timestamp for backtest period
- Target entity IDs: specific stocks (stock_sh_600000) or index components (SZ1000)?

## Semantic Locks (Fatal)

| ID | Rule | On Violation |
|---|---|---|
| `SL-01` | Execute sell orders before buy orders in every trading cycle | halt |
| `SL-02` | Trading signals MUST use next-bar execution (no look-ahead) | halt |
| `SL-03` | Entity IDs MUST follow format entity_type_exchange_code | halt |
| `SL-04` | DataFrame index MUST be MultiIndex (entity_id, timestamp) | halt |
| `SL-05` | TradingSignal MUST have EXACTLY ONE of: position_pct, order_money, order_amount | halt |
| `SL-06` | filter_result column semantics: True=BUY, False=SELL, None/NaN=NO ACTION | halt |
| `SL-07` | Transformer MUST run BEFORE Accumulator in factor pipeline | halt |
| `SL-08` | MACD parameters locked: fast=12, slow=26, signal=9 | halt |

Full lock definitions: [references/LOCKS.md](references/LOCKS.md)

## Top Anti-Patterns (47 total)

- **`AP-ZVT-183`**: 除权因子为 inf/NaN 时直接参与乘法导致复权静默失败
- **`AP-ZVT-179`**: 第三方数据接口超限后异常被吞噬，数据静默缺失
- **`AP-ZVT-200`**: Token 失效后数据查询返回空 DataFrame 而非报错

All 47 anti-patterns: [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md)

## Evidence Quality Notice

> [QUALITY NOTICE] This crystal was compiled from blueprint finance-bp-009. Evidence verify ratio = 55.0% and audit fail total = 36. Generated results may have uncaptured requirement gaps. Verify critical decisions against source files (LATEST.yaml / LATEST.jsonl).

## Reference Files

| File | Contents | When to Load |
|---|---|---|
| [references/seed.yaml](references/seed.yaml) | V6+ 全量权威 (source-of-truth) | 有行为/决策争议时必读 |
| [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) | 47 条跨项目反模式 | 开始实现前 |
| [references/WISDOM.md](references/WISDOM.md) | 跨项目精华借鉴 | 架构决策时 |
| [references/CONSTRAINTS.md](references/CONSTRAINTS.md) | domain + fatal 约束 | 规则冲突时 |
| [references/USE_CASES.md](references/USE_CASES.md) | 全量 KUC-* 业务场景 | 需要完整示例时 |
| [references/LOCKS.md](references/LOCKS.md) | SL-* + preconditions + hints | 生成回测/交易代码前 |
| [references/COMPONENTS.md](references/COMPONENTS.md) | AST 组件地图（按 module 拆分）| 查 API 时 |

---

*Compiled by Doramagic crystal-compilation-v6.1 from `finance-bp-009` blueprint at 2026-04-20T07:34:47.524525+00:00.*
*See [human_summary.md](human_summary.md) for non-technical overview.*
