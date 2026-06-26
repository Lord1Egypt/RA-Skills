---
name: daily-stock-analyzer
description: |-
  基于 Qlib 的 A 股自选股智能分析系统，集成 LLM Agent ReAct 推理引擎和技术指标择时模块（MA 多头排列、乖离率阈值严进策略），自动生成每日 buy/hold/sell 指令并推送至微信。触发场景：(1) 用户要查询自选股当天的 AI 交易信号和涨跌预测；(2) 用户要获取符合 MA 多头排列且乖离率低于 5% 的可买入股票列表；(3) 用户要在收盘后自动接收个股的买卖建议和持仓诊断报告。
license: Proprietary. See LICENSE.txt in project root.
compatibility: Designed for Doramagic-host ecosystem (Claude Code / openclaw / Cursor). Requires Python 3.12+ with uv package manager.
metadata:
  version: "v6.1"
  blueprint_id: "finance-bp-004"
  compiled_at: "2026-04-22T11:38:26.686045+00:00"
  capability_markets: "unspecified"
  capability_activities: "finance-analytics"
  sop_version: "crystal-compilation-v6.1"
---
# daily-stock-analyzer

> I help you build quant strategies on A-share with ZVT — from data fetch to backtest, one flow. Just tell me what you want; I'll write the code, you don't have to dig docs. (Heads up: ZVT natively supports A-share, HK, and crypto. US stocks — stockus_nasdaq_AAPL — are half-baked; don't bother for serious work.)

## Pipeline

`data_collection -> data_storage -> factor_computation -> target_selection -> trading_execution -> visualization`

## Top Use Cases (9 total)

### A股自选股智能分析系统主调度 (`UC-101`)
协调各模块完成股票分析流程，实现低并发的线程池调度，全局异常处理确保单股失败不影响整体分析任务
**Triggers**: 股票分析, 调度, 线程池

### RESTful API 后端服务 (`UC-102`)
提供RESTful API服务支持CORS跨域访问，同时托管前端静态文件用于生产环境部署
**Triggers**: API服务, 后端, FastAPI

### LLM Agent ReAct执行循环 (`UC-103`)
提供LLM Agent的ReAct执行循环，支持可插拔的进度回调、消息历史和结果处理，实现工具调用与LLM推理的迭代执行
**Triggers**: LLM Agent, ReAct, 工具调用

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

## Evidence Quality Notice

> [QUALITY NOTICE] This crystal was compiled from blueprint finance-bp-004. Evidence verify ratio = 52.9% and audit fail total = 25. Generated results may have uncaptured requirement gaps. Verify critical decisions against source files (LATEST.yaml / LATEST.jsonl).

## Reference Files

| File | Contents | When to Load |
|---|---|---|
| [references/seed.yaml](references/seed.yaml) | V6+ 全量权威 (source-of-truth) | 有行为/决策争议时必读 |
| [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) | 0 条跨项目反模式 | 开始实现前 |
| [references/WISDOM.md](references/WISDOM.md) | 跨项目精华借鉴 | 架构决策时 |
| [references/CONSTRAINTS.md](references/CONSTRAINTS.md) | domain + fatal 约束 | 规则冲突时 |
| [references/USE_CASES.md](references/USE_CASES.md) | 全量 KUC-* 业务场景 | 需要完整示例时 |
| [references/LOCKS.md](references/LOCKS.md) | SL-* + preconditions + hints | 生成回测/交易代码前 |
| [references/COMPONENTS.md](references/COMPONENTS.md) | AST 组件地图（按 module 拆分）| 查 API 时 |

---

*Compiled by Doramagic crystal-compilation-v6.1 from `finance-bp-004` blueprint at 2026-04-22T11:38:26.686045+00:00.*
*See [human_summary.md](human_summary.md) for non-technical overview.*
