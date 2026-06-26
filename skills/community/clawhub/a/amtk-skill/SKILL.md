---
name: amtk-skill
description: A 股行情数据技能：从 Tushare 抓取数据、查询行情估值、技术分析（均线/RSI/MACD/布林带）
when_to_use: 当用户需要 A 股数据时使用 — 抓取股票数据、查询行情、搜索股票、分析估值、计算技术指标、统计收益率等
argument-hint: "[fetch init | query 000001.SZ | analyze 000001.SZ MACD | ...]"
user-invocable: true
allowed-tools: Bash(uv run *) Bash(uv sync) Read Grep
---

# AMtkSkill — A 股行情数据技能

根据用户意图判断执行哪类操作，调用对应脚本。如果用户意图不明确，先询问。

## 前置条件

项目根目录：`${CLAUDE_SKILL_DIR}`

必须在 `.env` 中配置 `TUSHARE_TOKEN`。

检查依赖：
```!
uv sync
```

## Available scripts

- **`scripts/amtk_fetch.py`** — 从 Tushare 抓取 A 股行情数据存入本地 Parquet/CSV
- **`scripts/amtk_query.py`** — 查询本地数据：搜索股票、查看行情、估值排名、涨跌幅排名
- **`scripts/amtk_analyze.py`** — 技术分析：均线、RSI、MACD、布林带、复权价格、收益统计

每个脚本均支持 `--help` 查看完整用法。

---

# 一、Fetch — 数据抓取

### 首次初始化（全量抓取 + 中断续跑）

```bash
uv run scripts/amtk_fetch.py init
```

可选参数：
```bash
uv run scripts/amtk_fetch.py init --start-date 20250418 --end-date 20260418 --limit 10
```

### 每日增量更新

```bash
uv run scripts/amtk_fetch.py daily --end-date 20260420
```

### 中断续跑

```bash
uv run scripts/amtk_fetch.py resume
```

### 仅拉取股票列表

```bash
uv run scripts/amtk_fetch.py stock-list
uv run scripts/amtk_fetch.py stock-list --list-status L --exchange SSE
```

### 验证数据

```bash
uv run scripts/amtk_fetch.py overview
```

### fetch.py 参数速查

| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `init` | `--start-date`, `--end-date`, `--limit` | 全量抓取，自动 resume |
| `daily` | `--end-date` (必填) | 增量更新 |
| `resume` | 同 init | 中断续跑 |
| `stock-list` | `--list-status`, `--exchange` | 仅拉取股票列表 |
| `overview` | 无 | 数据总览 |

---

# 二、Query — 数据查询

### 数据总览

```bash
uv run scripts/amtk_query.py overview
```

### 搜索股票

```bash
uv run scripts/amtk_query.py stock-info --keyword 银行
uv run scripts/amtk_query.py stock-info --industry 银行 --exchange SSE
```

### 单只股票行情

```bash
uv run scripts/amtk_query.py daily --ts-code 000001.SZ
uv run scripts/amtk_query.py daily --ts-code 000001.SZ --start-date 20260101 --end-date 20260418 --tail 30
```

### 完整数据（行情 + 估值 + 复权因子）

```bash
uv run scripts/amtk_query.py full --ts-code 000001.SZ
```

### 全市场截面

```bash
uv run scripts/amtk_query.py cross-section --date 20260417 --sort-by amount --limit 20
```

### 涨跌幅排名

```bash
uv run scripts/amtk_query.py top-movers --date 20260417 --direction up --limit 10
uv run scripts/amtk_query.py top-movers --date 20260417 --direction down --limit 10
```

### 估值排名

```bash
uv run scripts/amtk_query.py valuation --metric pe --limit 10
uv run scripts/amtk_query.py valuation --metric pb --date 20260417
uv run scripts/amtk_query.py valuation --metric total_mv --limit 10
uv run scripts/amtk_query.py valuation --metric turnover_rate
```

### 行业平均估值

```bash
uv run scripts/amtk_query.py industry
uv run scripts/amtk_query.py industry --date 20260417 --limit 30
```

### query.py 参数速查

| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `overview` | 无 | 各数据集行数/日期范围 |
| `stock-info` | `--keyword`, `--industry`, `--exchange` | 搜索股票 |
| `daily` | `--ts-code` (必填) | 单股 OHLCV |
| `full` | `--ts-code` (必填) | 单股完整数据 |
| `cross-section` | `--date` (必填) | 全市场某日截面 |
| `top-movers` | `--date` (必填), `--direction` | 涨跌幅 TOP N |
| `valuation` | `--metric` (必填: pe/pb/total_mv/turnover_rate) | 估值排名 |
| `industry` | `--date`, `--limit` | 行业平均估值 |

---

# 三、Analyze — 技术分析

### 均线

```bash
uv run scripts/amtk_analyze.py ma --ts-code 000001.SZ
uv run scripts/amtk_analyze.py ma --ts-code 000001.SZ --windows 5,20,60 --start-date 20260101
```

### RSI

```bash
uv run scripts/amtk_analyze.py rsi --ts-code 000001.SZ --period 14
```

### MACD

```bash
uv run scripts/amtk_analyze.py macd --ts-code 000001.SZ
```

### 布林带

```bash
uv run scripts/amtk_analyze.py bollinger --ts-code 000001.SZ
```

### 复权价格

```bash
uv run scripts/amtk_analyze.py adjusted --ts-code 000001.SZ --method forward
uv run scripts/amtk_analyze.py adjusted --ts-code 000001.SZ --method backward
```

### 收益统计

```bash
uv run scripts/amtk_analyze.py stats --ts-code 000001.SZ --start-date 20250418
```

输出：total_return_pct, annualized_return_pct, annualized_volatility_pct, max_drawdown_pct, sharpe_ratio

### 检测分红拆股

```bash
uv run scripts/amtk_analyze.py corporate-actions --ts-code 000001.SZ
```

### 多股票对比

```bash
uv run scripts/amtk_analyze.py compare --ts-codes 000001.SZ,600519.SH,000858.SZ --start-date 20250418
```

### analyze.py 参数速查

| 子命令 | 关键参数 | 说明 |
|--------|----------|------|
| `ma` | `--ts-code`, `--windows` | 均线 (默认 5,10,20,60) |
| `rsi` | `--ts-code`, `--period` | RSI (默认 14) |
| `macd` | `--ts-code`, `--fast`, `--slow`, `--signal` | MACD |
| `bollinger` | `--ts-code`, `--window`, `--num-std` | 布林带 |
| `adjusted` | `--ts-code`, `--method` | 前/后复权价格 |
| `stats` | `--ts-code` | 收益率/波动率/回撤/夏普 |
| `corporate-actions` | `--ts-code` | 分红拆股检测 |
| `compare` | `--ts-codes` (逗号分隔) | 多股票对比 |

---

# 数据表结构

| 数据集 | 字段 |
|--------|------|
| market_daily | ts_code, trade_date, open, high, low, close, vol(手), amount(千元), vwap |
| daily_basic | ts_code, trade_date, turnover_rate(%), pe, pe_ttm, pb, total_mv(万元), circ_mv(万元) |
| adj_factor | ts_code, trade_date, adj_factor |
| stock_basic | ts_code, symbol, name, area, industry, market, exchange, list_status, list_date |

# 指标解读参考

| 指标 | 多头/超买 | 空头/超卖 |
|------|----------|----------|
| RSI | > 70 超买 | < 30 超卖 |
| MACD | macd > signal（金叉） | macd < signal（死叉） |
| 布林带 | 价格触及上轨 | 价格触及下轨 |
| 均线 | 短期 > 长期（多头排列） | 短期 < 长期（空头排列） |

# 通用规则

1. **如果用户未指定日期**：query 和 analyze 默认使用最新交易日
2. **如果没有数据**：提示用户先执行 `uv run scripts/amtk_fetch.py init`
3. **默认使用前复权价格**（analyze）
4. **对结果做简要解读** — 帮用户理解数据含义

# 故障排查

- **token 错误** — 检查 `.env` 中 `TUSHARE_TOKEN`
- **缺少 pyarrow** — 运行 `uv sync`
- **中断后续跑** — `uv run scripts/amtk_fetch.py resume`
- **只想抓少量测试** — `uv run scripts/amtk_fetch.py init --limit 5`
