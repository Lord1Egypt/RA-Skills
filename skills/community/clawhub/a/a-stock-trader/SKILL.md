---
name: a-stock-trader
description: "A股模拟交易系统 - 数据爬取、存储、策略回测、模拟交易 / A-Share Paper Trading System - Data Fetch, Storage, Backtest, Simulation"
metadata:
  version: 1.0.1
  author: OpenClaw Agent
---

# A股模拟交易系统 / A-Share Paper Trading System

这是一个完整的A股模拟交易系统，包含数据获取、存储、策略回测和模拟交易功能。

This is a complete A-share paper trading system with data fetching, storage, strategy backtest and simulation.

## 功能模块 / Function Modules

### 1. 数据爬取 / Data Fetching
- 实时行情数据（10分钟级别）/ Real-time data (10-min level)
- 历史K线数据（日/周/月）/ Historical K-line (daily/weekly/monthly)
- 个股基本面数据 / Stock fundamentals
- 大盘指数数据 / Market index data
- 数据源：东方财富网、新浪财经 / Data source: East Money, Sina Finance

### 2. 数据存储 / Data Storage
- SQLite 数据库 / SQLite database
- 表结构：日线数据、财务数据、持仓记录、交易记录 / Tables: daily_data, financials, positions, trades
- 数据路径：`~/.openclaw/workspace/a-stock/` / Data path

### 3. 模拟交易 / Paper Trading
- 纸上交易（不真实下单）/ Paper trading (no real orders)
- 持仓管理 / Position management
- 资金管理（初始100万）/ Capital management (initial 1M)
- 收益计算 / PnL calculation

### 4. 策略模板 / Strategy Templates

#### 4.1 均线策略 (MA) / Moving Average Strategy
- 金叉买入，死叉卖出 / Buy on golden cross, sell on death cross
- 参数：MA5, MA10, MA20 / Parameters

#### 4.2 动量策略 (Momentum) / Momentum Strategy
- 追涨杀跌 / Trend following
- 涨幅>5%买入，回撤>3%卖出 / Buy when +5%, sell when -3%

#### 4.3 突破策略 (Breakout) / Breakout Strategy
- 20日高点突破买入 / Buy on 20-day high breakout
- 跌破5日低点卖出 / Sell on 5-day low break

#### 4.4 网格策略 (Grid) / Grid Strategy
- 震荡行情网格交易 / Grid trading in ranging market
- 设定价格区间和网格数量 / Set price range and grid count

## 使用示例 / Usage Examples

### 获取数据 / Fetch Data
```bash
python scripts/fetch_daily.py --stock 600519 --days 250
```

### 运行回测 / Run Backtest
```bash
python scripts/backtest.py --strategy ma --stock 600519
```

### 模拟交易 / Paper Trade
```bash
python scripts/simulate.py --strategy momentum --stock 600519
```

### 查看持仓 / Show Portfolio
```bash
python scripts/simulate.py --show
```

## 数据结构 / Data Schema

### daily_data (日线数据 / Daily Data)
| 字段/Field | 类型/Type | 说明/Description |
|------------|-----------|-----------------|
| date | TEXT | 日期 / Date |
| code | TEXT | 股票代码 / Stock code |
| open | REAL | 开盘价 / Open |
| high | REAL | 最高价 / High |
| low | REAL | 最低价 / Low |
| close | REAL | 收盘价 / Close |
| volume | REAL | 成交量 / Volume |
| amount | REAL | 成交额 / Amount |

### positions (持仓 / Positions)
| 字段/Field | 类型/Type | 说明/Description |
|------------|-----------|-----------------|
| code | TEXT | 股票代码 / Stock code |
| name | TEXT | 股票名称 / Stock name |
| shares | INTEGER | 股数 / Shares |
| cost | REAL | 成本价 / Cost |
| buy_date | TEXT | 买入日期 / Buy date |

### trades (交易记录 / Trade Records)
| 字段/Field | 类型/Type | 说明/Description |
|------------|-----------|-----------------|
| date | TEXT | 交易日期 / Date |
| code | TEXT | 股票代码 / Stock code |
| type | TEXT | buy/sell |
| price | REAL | 价格 / Price |
| shares | INTEGER | 股数 / Shares |
| pnl | REAL | 盈亏 / PnL |

## 定时任务 / Scheduled Tasks

系统会自动：/ System will automatically:
- 每天收盘后获取当日数据 / Fetch daily data after market close
- 每周运行策略回测 / Run weekly backtest
- 每月生成交易报告 / Generate monthly report

## 注意事项 / Notes

1. 本系统仅供学习研究，不构成投资建议 / For learning only, not investment advice
2. 模拟交易不涉及真实资金 / No real money involved
3. 历史业绩不代表未来表现 / Past performance doesn't guarantee future results
