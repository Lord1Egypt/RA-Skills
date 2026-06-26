---
name: climate-esg-investing
description: |-
  使用Fama-French因子模型进行气候ESG投资分析，支持月度股价数据下载、因子相关性计算、OLS回归诊断及显著性筛选，帮助用户构建因子组合和风险评估。
license: Proprietary. See LICENSE.txt in project root.
compatibility: Designed for Doramagic-host ecosystem (Claude Code / openclaw / Cursor). Requires Python 3.12+ with uv package manager.
metadata:
  version: "v6.1"
  blueprint_id: "finance-bp-105"
  compiled_at: "2026-04-22T13:00:49.775031+00:00"
  capability_markets: "global"
  capability_activities: "macro-data"
  sop_version: "crystal-compilation-v6.1"
---
# ESG 气候投资 (climate-esg-investing)

> 使用Fama-French因子模型进行气候ESG投资分析，支持月度股价数据下载、因子相关性计算、OLS回归诊断及显著性筛选，帮助用户构建因子组合和风险评估。

## Pipeline

`data_collection -> data_storage -> factor_computation -> target_selection -> trading_execution -> visualization`

## Top Use Cases (9 total)

### Sector Stock Count and Significant Factor Regression Analyzer (`UC-101`)
Identifies how many stocks from an index fall into each sector and screens for stocks with statistically significant factor regression results based o
**Triggers**: sector composition, significant regression, p-value screening

### Factor Correlation Calculator (`UC-102`)
Computes correlations between different factors over time to understand factor relationship dynamics and potential multicollinearity issues
**Triggers**: factor correlation, correlation matrix, factor relationships

### OLS Regression with Diagnostic Statistics (`UC-103`)
Performs ordinary least squares regression on factor data with comprehensive diagnostic tests including Durbin-Watson, Jarque-Bera, and Breusch-Pagan
**Triggers**: OLS regression, diagnostic tests, statistical tests

For all **9** use cases, see [references/USE_CASES.md](references/USE_CASES.md).

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

## Top Anti-Patterns (14 total)

- **`AP-MACRO-DATA-001`**: SEC EDGAR Rate Limit Violation
- **`AP-MACRO-DATA-002`**: Temporal Knowledge Graph Look-Ahead Bias
- **`AP-MACRO-DATA-003`**: Technical Indicator Look-Ahead Bias via Missing Shift

All 14 anti-patterns: [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md)

## Evidence Quality Notice

> [QUALITY NOTICE] This crystal was compiled from blueprint finance-bp-105. Evidence verify ratio = 3.3% and audit fail total = 20. Generated results may have uncaptured requirement gaps. Verify critical decisions against source files (LATEST.yaml / LATEST.jsonl).

## Reference Files

| File | Contents | When to Load |
|---|---|---|
| [references/seed.yaml](references/seed.yaml) | V6+ 全量权威 (source-of-truth) | 有行为/决策争议时必读 |
| [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) | 14 条跨项目反模式 | 开始实现前 |
| [references/WISDOM.md](references/WISDOM.md) | 跨项目精华借鉴 | 架构决策时 |
| [references/CONSTRAINTS.md](references/CONSTRAINTS.md) | domain + fatal 约束 | 规则冲突时 |
| [references/USE_CASES.md](references/USE_CASES.md) | 全量 KUC-* 业务场景 | 需要完整示例时 |
| [references/LOCKS.md](references/LOCKS.md) | SL-* + preconditions + hints | 生成回测/交易代码前 |
| [references/COMPONENTS.md](references/COMPONENTS.md) | AST 组件地图（按 module 拆分）| 查 API 时 |

---

*Compiled by Doramagic crystal-compilation-v6.1 from `finance-bp-105` blueprint at 2026-04-22T13:00:49.775031+00:00.*
*See [human_summary.md](human_summary.md) for non-technical overview.*
