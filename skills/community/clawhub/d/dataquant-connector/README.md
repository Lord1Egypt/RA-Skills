# DataQuant Connector

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/DataQuant-API-4d8df6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48dGV4dCB5PSIuOWVtIiBmb250LXNpemU9IjkwIj7wn6SbPC90ZXh0Pjwvc3ZnPg">
    <img alt="DataQuant" src="https://img.shields.io/badge/DataQuant-API-4d8df6?style=for-the-badge">
  </picture>
  <br><br>
  <b>AI Agent Skill for Quantitative Market Data &amp; Automated Backtesting</b>
  <br>
  <sub>Daily OHLCV for 6,125+ instruments across A-shares, HK, US equities, crypto, indices, and ETFs. One link installs into your AI assistant — zero config, zero code.</sub>
</p>

---

<p align="center">
  <a href="#what-is-dataquant-connector"><b>About</b></a> ·
  <a href="#who-is-this-for"><b>Who It's For</b></a> ·
  <a href="#use-cases"><b>Use Cases</b></a> ·
  <a href="#financial-data-coverage"><b>Coverage</b></a> ·
  <a href="#installation-guide"><b>Install</b></a> ·
  <a href="#automated-backtesting-pipeline"><b>Pipeline</b></a> ·
  <a href="#skill-structure"><b>Structure</b></a> ·
  <a href="#cli-usage"><b>CLI</b></a> ·
  <a href="#rest-api-reference"><b>API</b></a> ·
  <a href="#中文版">中文版</a>
</p>

---

## What Is DataQuant Connector?

**DataQuant Connector** is an AI Agent Skill that equips your assistant with direct access to structured financial market data — daily OHLCV (open, high, low, close, volume, amount) for over 6,125 instruments across six global markets. Built on the [DataQuant](https://app.dataquant.trade/) quantitative data platform, accessible via a simple REST interface.

Designed for quantitative backtesting workflows: describe a strategy in plain language, and your AI handles data retrieval, script generation, execution, and reporting — end to end.

## Who Is This For?

- **AI-assisted quantitative researchers** who design and validate trading strategies through natural-language interaction with an AI agent
- **Developers building AI agents** that need a structured, low-latency financial data source with a simple REST interface
- **Individual traders** who want to backtest ideas without writing data pipelines, web scrapers, or ETL jobs

## Use Cases

All powered by daily OHLCV plus a per-instrument latest snapshot (valuation, size, momentum, 52-week position) — enough for screening without pulling financial statements.

| Use Case | Example Prompt |
|----------|---------------|
| **Rule-based Strategy Backtest** | "Backtest Kweichow Moutai 2020–2025, buy on MA20/MA60 golden cross, sell on death cross" |
| **Event-driven Analysis** | "Buy CSI 300 ETF the day after a PBoC RRR cut and hold for 30 days — run this for all RRR cuts since 2015" [^1] |
| **Multi-asset Portfolio Backtest** | "Equal-weight the top 10 CSI 300 constituents by volume, rebalance monthly, 2020–2025" |

[^1]: Event dates (e.g. RRR cut announcements) are resolved by the AI agent through search tools. DataQuant provides the OHLCV price series for the backtest window.

## Financial Data Coverage

| Market | Instruments | Identifiers |
|--------|-------------|-------------|
| **A-Shares** | ~3,000 | `sh600519` · `sz000001` |
| **HK Stocks** | ~1,000 | `hk00700` · `hk09988` |
| **US Stocks** | ~2,000 | `usAAPL` · `usMSFT` |
| **Cryptocurrency** | ~100 | `BTCUSDT` · `ETHUSDT` |
| **Global Indices** | 15 | `sh000001` · `hkHSI` |
| **ETFs** | 11 | `sh510050` · `sh510300` |

| Metric | Value |
|--------|-------|
| Total Instruments | **6,125+** |
| Update Frequency | **Daily (EOD)** |
| Data Format | OHLCV + latest snapshot (valuation, size, momentum, 52w position) |

**Macroeconomic indicators** — GDP, CPI/PPI, and PMI — are also available via the `/macro` endpoint.

## Installation Guide

### Step 1 — Register &amp; Get Your API Key

Sign up at [app.dataquant.trade](https://app.dataquant.trade/). Copy your API Key from the user dashboard.

### Step 2 — Send the Skill Link to Your AI

Paste the following line into any AI assistant that supports Skill installation:

```
Install the skill at: https://app.dataquant.trade/skill
```

The AI reads the embedded skill definition from the page, creates the directory structure, and writes all support files — fully automated.

### Step 3 — Provide Your Key &amp; Start

```
My DataQuant API Key is dq_xxxxxxxx
```

Your AI is now connected. Describe any strategy:

```
Backtest CSI 300 ETF 2020–2025, Bollinger Band mean-reversion,
buy on lower band touch, sell on middle band convergence
```

## Automated Backtesting Pipeline

<p align="center">
  <kbd>Natural Language Strategy</kbd> &nbsp;→&nbsp;
  <kbd>DataQuant Data Fetch</kbd> &nbsp;→&nbsp;
  <kbd>Backtest Script Generation</kbd> &nbsp;→&nbsp;
  <kbd>Equity Curve Plot</kbd> &nbsp;→&nbsp;
  <kbd>Analysis Report</kbd>
</p>

Every stage is automated. The user provides a strategy description; the AI handles data retrieval, script generation, backtest execution, and final reporting.

## Skill Structure

```
dataquant-connector/
├── SKILL.md                    # Core skill definition
├── skill.json                  # Skill metadata
├── LICENSE
├── README.md
└── scripts/
    └── dataquant.py            # Python CLI for the DataQuant REST API
```

### File Roles

| File | Required |
|------|----------|
| `SKILL.md` | ✅ |
| `skill.json` | ✅ |
| `scripts/dataquant.py` | ✅ |
| `README.md` | — |
| `LICENSE` | — |

API 参数与字段定义以 [app.dataquant.trade/api-docs](https://app.dataquant.trade/api-docs) 为准，本 Skill 不做二次维护。

## CLI Usage

```bash
# Single-instrument daily OHLCV (with adjustment)
python scripts/dataquant.py kline ashare sh600519 \
  --start 2020-01-01 --end 2025-12-31 --adj qfq --api-key KEY

# Batch fetch (up to 50 instruments depending on plan)
python scripts/dataquant.py batch ashare sh600519,sz000858 \
  --start 2025-01-01 --adj bfq --api-key KEY

# Latest snapshot (valuation, size, momentum, 52w)
python scripts/dataquant.py detail ashare sh600519 --api-key KEY
python scripts/dataquant.py detail ashare sh600519,sz000858 --api-key KEY

# Screen by criteria
python scripts/dataquant.py screen ashare \
  --min-pe-ratio 0 --max-pe-ratio 30 --sort change_percent --api-key KEY

# Symbol search
python scripts/dataquant.py search ashare 600519 --api-key KEY

# Quota inspection
python scripts/dataquant.py quota --api-key KEY

# Macroeconomic indicators
python scripts/dataquant.py macro gdp --start 2020 --end 2025 --api-key KEY
```

Or set the key once as an environment variable:

```bash
# Linux / macOS
export DATAQUANT_API_KEY=dq_xxxxxxxx
# Windows (PowerShell)
$env:DATAQUANT_API_KEY = "dq_xxxxxxxx"

python scripts/dataquant.py kline ashare sh600519 --start 2020-01-01
```

## REST API Reference

| | |
|---|---|
| **Base URL** | `https://api.dataquant.trade` |
| **Authentication** | `X-API-Key` header |
| **Response Format** | JSON |

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/{market}/klines/{symbol}?adj=bfq\|qfq\|hfq` | Single-instrument daily OHLCV (bfq default; hfq/qfq forward/backward-adjusted) |
| `GET` | `/{market}/klines?symbols=a,b&adj=...` | Batch OHLCV (comma-separated, same adj support) |
| `GET` | `/{market}/detail/{symbol}?fields=...` | Single-instrument latest snapshot (valuation / size / momentum / 52w) |
| `GET` | `/{market}/detail?symbols=a,b` | Batch latest snapshot (comma-separated) |
| `GET` | `/{market}/screen?min_pe_ratio=...&max_pe_ratio=...` | Filter latest snapshot by valuation / size / momentum |
| `GET` | `/{market}/symbols?search=` | Fuzzy search by name or code |
| `GET` | `/macro?indicator=gdp\|cpi_ppi\|pmi` | Macroeconomic data — GDP, CPI&PPI, PMI (indicator optional; returns all when omitted) |
| `GET` | `/quota` | Current usage and remaining daily quota |

### Markets

```
ashare     A-Shares
hkstock    Hong Kong Stocks
usstock    US Stocks
crypto     Cryptocurrency
indices    Global Indices
etfs       ETFs
```

### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `YYYY-MM-DD` | Start date — inclusive (klines/detail: YYYY-MM-DD; macro: YYYY year only) |
| `end` | `YYYY-MM-DD` | End date — inclusive (klines/detail: YYYY-MM-DD; macro: YYYY year only) |
| `fields` | `o,h,l,c,v,a` | Field selection for klines (short codes or full names, default: `*` for all); detail columns for /detail (e.g. `pe_ratio,pb_ratio,chg_20d`). symbol, date, and adj_factor are always returned regardless of fields |
| `adj` | `bfq\|qfq\|hfq` | Adjustment method — klines only: bfq unadjusted (default), qfq forward-adjusted, hfq backward-adjusted |
| `limit` | `integer` | Max rows per page |
| `offset` | `integer` | Pagination offset |
| `sort` | `string` | Screen sort column (default: `change_percent`), must be in filter whitelist |
| `order` | `asc\|desc` | Screen sort order (default: `desc`) |
| `min_*` / `max_*` | `float` | Screen filter bounds — prefix with column name, e.g. `min_pe_ratio=0`, `max_total_market_cap=1000` |

### OHLCV Fields

| Code | Name | Description |
|------|------|-------------|
| `o` | open | Opening price |
| `h` | high | Session high |
| `l` | low | Session low |
| `c` | close | Closing price |
| `v` | volume | Volume (lots for equities) |
| `a` | amount | Turnover / notional amount |

symbol, date, and adj_factor are always returned in every kline row regardless of the `fields` parameter.
symbol and date are always returned in every detail row.

## Links

- [DataQuant Homepage](https://app.dataquant.trade/)
- [Skill Installation Page](https://app.dataquant.trade/skill)
- [Interactive API Documentation](https://app.dataquant.trade/api-docs)

## License

MIT

---

<br>

# 中文版

---

## DataQuant Connector 是什么？

**DataQuant Connector** 是一个 AI Agent Skill（技能包），为 AI 助手提供结构化金融市场数据的直连通道——覆盖 A 股、港股、美股、加密货币、全球指数、ETF 六大市场，6,125+ 只标的的日线 OHLCV（开高低收量额）。底层对接 [DataQuant](https://app.dataquant.trade/) 量化数据平台。

面向量化回测场景设计：用户用自然语言描述策略，AI 自动完成取数、脚本生成、执行、报告输出全链路。

## 适用人群

- **AI 辅助量化研究者**：通过与 AI 自然语言交互设计、验证交易策略
- **AI Agent 开发者**：需要一个结构化、低延迟金融数据接口来构建量化智能体
- **个人交易者**：想验证交易想法但不想自己写爬虫、ETL 管道、数据清洗链路

## 使用场景

基于日线 OHLCV 与每标的「最新快照」（估值 / 规模 / 动量 / 52 周位置）——足以支撑筛选，无需逐只拉取财务报表。

| 场景 | 示例提示 |
|------|---------|
| **规则型策略回测** | "回测贵州茅台 2020–2025，MA20 上穿 MA60 买入，死叉卖出" |
| **事件驱动分析** | "央行降准后第二天买入沪深 300 ETF 持有 30 天，统计 2015 年以来所有降准事件" [^2] |
| **多标组合回测** | "沪深 300 成份股中成交量前 10 名等权持有，月度再平衡，2020–2025" |

[^2]: 事件日期（如降准公告日）由 AI 通过搜索工具确认，DataQuant 提供回测窗口内的 OHLCV 价格序列。

## 数据覆盖

| 市场 | 标的数 | 标识符示例 |
|------|--------|-----------|
| **A 股** | ~3,000 | `sh600519` · `sz000001` |
| **港股** | ~1,000 | `hk00700` · `hk09988` |
| **美股** | ~2,000 | `usAAPL` · `usMSFT` |
| **加密货币** | ~100 | `BTCUSDT` · `ETHUSDT` |
| **全球指数** | 15 | `sh000001` · `hkHSI` |
| **ETF** | 11 | `sh510050` · `sh510300` |

| 指标 | 数值 |
|------|------|
| 覆盖标的 | **6,125+** |
| 更新频率 | **每日盘后** |
| 数据格式 | OHLCV + 最新快照（估值 / 规模 / 动量 / 52 周位置） |

**宏观经济指标** — GDP、CPI/PPI、PMI — 通过 `/macro` 端点查询。

## 安装指南

### 第一步 —— 注册获取 API Key

前往 [app.dataquant.trade](https://app.dataquant.trade/) 注册，在用户后台复制 API Key。

### 第二步 —— 将 Skill 链接发送给 AI

将下面这行发给你支持 Skill 安装的 AI 助手：

```
安装这个链接里的 skill：https://app.dataquant.trade/skill
```

AI 会自动读取页面内嵌的 Skill 定义，创建目录结构，写入所有支撑文件。

### 第三步 —— 提供 Key，开始使用

```
我的 DataQuant API Key 是 dq_xxxxxxxx
```

配置完成。直接描述策略即可：

```
回测沪深 300 ETF 2020–2025，布林带均值回归，
触碰下轨买入，回归中轨卖出
```

## 自动化回测流水线

<p align="center">
  <kbd>自然语言策略描述</kbd> &nbsp;→&nbsp;
  <kbd>DataQuant 数据获取</kbd> &nbsp;→&nbsp;
  <kbd>回测脚本生成</kbd> &nbsp;→&nbsp;
  <kbd>权益曲线绘制</kbd> &nbsp;→&nbsp;
  <kbd>分析报告输出</kbd>
</p>

全链路自动化。用户提供策略描述，AI 完成数据检索、脚本生成、回测执行和最终报告。

## Skill 目录结构

```
dataquant-connector/
├── SKILL.md                    # 核心 Skill 定义
├── skill.json                  # Skill 元数据
├── LICENSE
├── README.md
└── scripts/
    └── dataquant.py            # DataQuant REST API 的 Python CLI
```

### 文件分工

| 文件 | 必须 |
|------|------|
| `SKILL.md` | ✅ |
| `skill.json` | ✅ |
| `scripts/dataquant.py` | ✅ |
| `README.md` | — |
| `LICENSE` | — |

API 参数与字段定义以 [app.dataquant.trade/api-docs](https://app.dataquant.trade/api-docs) 为准，本 Skill 不做二次维护。

## CLI 使用

```bash
# 单标的日线（支持复权）
python scripts/dataquant.py kline ashare sh600519 \
  --start 2020-01-01 --end 2025-12-31 --adj qfq --api-key KEY

# 批量取数（批量上限取决于套餐）
python scripts/dataquant.py batch ashare sh600519,sz000858 \
  --start 2025-01-01 --adj bfq --api-key KEY

# 最新快照（估值/规模/动量/52周）
python scripts/dataquant.py detail ashare sh600519 --api-key KEY
python scripts/dataquant.py detail ashare sh600519,sz000858 --api-key KEY

# 条件筛选
python scripts/dataquant.py screen ashare \
  --min-pe-ratio 0 --max-pe-ratio 30 --sort change_percent --api-key KEY

# 标的搜索
python scripts/dataquant.py search ashare 600519 --api-key KEY

# 配额查询
python scripts/dataquant.py quota --api-key KEY

# 宏观经济指标
python scripts/dataquant.py macro gdp --start 2020 --end 2025 --api-key KEY
```

也可通过环境变量设置 Key：

```bash
# Linux / macOS
export DATAQUANT_API_KEY=dq_xxxxxxxx
# Windows (PowerShell)
$env:DATAQUANT_API_KEY = "dq_xxxxxxxx"

python scripts/dataquant.py kline ashare sh600519 --start 2020-01-01
```

## REST API 参考

| | |
|---|---|
| **Base URL** | `https://api.dataquant.trade` |
| **认证方式** | `X-API-Key` Header |
| **响应格式** | JSON |

### 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/{market}/klines/{symbol}?adj=bfq\|qfq\|hfq` | 单标的日线 OHLCV（bfq 默认不复权；qfq/hfq 前/后复权） |
| `GET` | `/{market}/klines?symbols=a,b&adj=...` | 批量日线（逗号分隔，同样支持 adj） |
| `GET` | `/{market}/detail/{symbol}?fields=...` | 单标的最新快照（估值 / 规模 / 动量 / 52 周） |
| `GET` | `/{market}/detail?symbols=a,b` | 批量最新快照（逗号分隔） |
| `GET` | `/{market}/screen?min_pe_ratio=...&max_pe_ratio=...` | 按估值 / 规模 / 动量筛选最新快照 |
| `GET` | `/{market}/symbols?search=` | 按名称或代码模糊搜索 |
| `GET` | `/macro?indicator=gdp\|cpi_ppi\|pmi` | 宏观经济数据（GDP / CPI&PPI / PMI，indicator 可选，不传返回全部） |
| `GET` | `/quota` | 查询当日用量与剩余配额 |

### 市场代码

```
ashare     A 股
hkstock    港股
usstock    美股
crypto     加密货币
indices    全球指数
etfs       ETF
```

### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `start` | `YYYY-MM-DD` | 起始日期 — 含当日（K线/快照：YYYY-MM-DD；宏观：YYYY 年份） |
| `end` | `YYYY-MM-DD` | 结束日期 — 含当日（K线/快照：YYYY-MM-DD；宏观：YYYY 年份） |
| `fields` | `o,h,l,c,v,a` | K 线字段选择（短码或全名均可）：单标的默认 `*`(全字段)，批量默认 `close,volume`；detail 快照字段（如 `pe_ratio,pb_ratio,chg_20d`）。kline 行始终含 symbol/date/adj_factor；detail 行始终含 symbol/date |
| `adj` | `bfq\|qfq\|hfq` | 复权方式 — 仅 K 线：bfq 不复权（默认），qfq 前复权，hfq 后复权 |
| `limit` | `integer` | 每页最大返回行数 |
| `offset` | `integer` | 分页偏移 |
| `sort` | `string` | Screen 排序字段（默认 `change_percent`），须在白名单内 |
| `order` | `asc\|desc` | Screen 排序方向（默认 `desc`） |
| `min_*` / `max_*` | `float` | Screen 筛选上下界 — 前缀加列名，如 `min_pe_ratio=0`、`max_total_market_cap=1000` |

### OHLCV 字段

| 代码 | 名称 | 说明 |
|------|------|------|
| `o` | open | 开盘价 |
| `h` | high | 当日最高价 |
| `l` | low | 当日最低价 |
| `c` | close | 收盘价 |
| `v` | volume | 成交量（股/手） |
| `a` | amount | 成交额 |

每行 K 线始终返回 symbol、date、adj_factor，不受 fields 参数影响。
每行 detail 快照始终返回 symbol、date。

## 相关链接

- [DataQuant 主页](https://app.dataquant.trade/)
- [Skill 安装页面](https://app.dataquant.trade/skill)
- [交互式 API 文档](https://app.dataquant.trade/api-docs)

## 许可证

MIT
