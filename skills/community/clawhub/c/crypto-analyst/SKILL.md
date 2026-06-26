---
name: crypto-analyst
description: 加密货币综合分析工具，整合OKX、Binance双交易所数据。提供行情查询、技术分析、交易信号、资金流向、仓位管理、DCA计划、风险计算。触发词：分析BTC、行情查询、交易信号、仓位计算、DCA计划、巨鲸追踪、风险评估。
---

# Crypto Analyst v1.1

加密货币综合分析，统一调用 OKX、Binance、AKShare 三大数据源。

## 工作流

```
价格查询 → 技术分析 → 资金流向 → 策略建议 → 仓位管理
```

## 工具速查

| 需求 | 工具 | 数据源 | 备注 |
|------|------|--------|------|
| OKX技术分析/信号 | `okx_analyst.py` | OKX API | 需要API Key |
| Binance实时行情 | `binance_market.py` | Binance公开API | 自动降级至Binance US |
| Binance技术分析 | `technical_analysis.py` | Binance公开API | 同上 |
| 双交易所价格对比 | `cross_exchange.py` | OKX + Binance US | 发现套利机会 |
| 巨鲸追踪 | `whale_tracker.py` | Binance | ≥$10,000才算巨鲸 |
| DCA定投计划 | `dca_calculator.py` | OKX实时价格 | 自动获取BTC价格 |
| 仓位计算 | `position_sizer.py` | 本地计算 | — |
| 市场机会扫描 | `market_scanner.py` | Binance | 过滤<$1M日成交量 |
| 恐惧&贪婪 | `fear_greed.py` | alternative.me | 每日约8:00更新 |
| OKX余额查询 | `balance_check.py` | OKX API | 需要Key+Secret+Passphrase |

## 快速命令

### 日常行情分析
```bash
# OKX技术分析（完整报告）
python3 scripts/okx_analyst.py BTC-USDT

# OKX快速信号
python3 scripts/okx_analyst.py BTC-USDT --signal-only

# Binance实时价格+24h统计
python3 scripts/binance_market.py --symbol BTCUSDT --all

# Binance技术分析
python3 scripts/technical_analysis.py --symbol BTCUSDT --interval 1h
```

### 进阶分析
```bash
# 跨交易所价格对比（发现价差套利机会）
python3 scripts/cross_exchange.py BTC

# 巨鲸追踪（只统计≥$10,000的大单）
python3 scripts/whale_tracker.py --symbol BTCUSDT

# 市场机会扫描（过滤低流动性，日成交>$1M）
python3 scripts/market_scanner.py --gainers --limit 10

# 恐惧&贪婪指数
python3 scripts/fear_greed.py
```

### 策略工具
```bash
# DCA定投计划（自动获取当前BTC价格）
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180

# DCA手动指定价格+情景分析
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180 --current-price 70000 --scenarios

# 仓位计算（2%风控）
python3 scripts/position_sizer.py --balance 10000 --risk 2 --entry 70000 --stop-loss 67000
```

## 标准分析流程

当用户说"分析BTC"或"帮我看看行情"时：

**Step 1 - 价格 & 趋势**
```bash
# OKX 4H周期完整分析
python3 scripts/okx_analyst.py BTC-USDT --timeframe 4H

# Binance 1H作为辅助确认
python3 scripts/binance_market.py --symbol BTCUSDT --klines 1h --limit 50
```

**Step 2 - 资金面**
```bash
# 巨鲸动向（自动过滤<$10,000小额噪声）
python3 scripts/whale_tracker.py --symbol BTCUSDT

# 交易所资金费率（判断多空情绪）
python3 scripts/binance_market.py --symbol BTCUSDT --funding
```

**Step 3 - 市场情绪**
```bash
# 恐惧&贪婪（注意：每天约8:00 UTC更新一次）
python3 scripts/fear_greed.py
```

**Step 4 - 策略输出**
综合以上给出：
1. 当前信号（看涨/看跌/中性）
2. 关键支撑/阻力位
3. 入场区间
4. 止损/止盈建议
5. 仓位大小（风控）
6. 风险提示

## 信号强度说明

| 强度 | 信号 | 建议 |
|:---:|:---:|:---|
| +8以上 | 🟢 强烈看涨 | 积极做多 |
| +5~+7 | 🟡 温和看涨 | 轻仓试多 |
| +2~+4 | 🔵 轻微看涨 | 观望 |
| -1~+1 | ⚪ 中性 | 不操作 |
| -2~-4 | 🟠 轻微看跌 | 轻仓试空 |
| -5以下 | 🔴 强烈看跌 | 不做多 |

## 跨交易所对比

使用 `cross_exchange.py` 检测 OKX vs Binance 价差，超过0.1%提示套利机会。

## 风险控制规则

1. 单笔交易风险 ≤ 账户2%
2. 总持仓 ≤ 账户50%
3. 永远带止损
4. 恐惧&贪婪指数 ≥ 75（极度贪婪）时不做多
5. 巨鲸净卖出 + RSI超买 → 谨慎
6. 极度恐惧（≤25）时 ≠ 立即买入，等企稳

## 配置文件

复制 `.env.example` 为 `.env` 后填入：
```bash
OKX_API_KEY=your-key
OKX_API_SECRET=your-secret
OKX_API_PASSPHRASE=your-passphrase
```

> 注意：`balance_check.py` 需要三个要素（Key + Secret + Passphrase），缺一不可。

## 依赖

```bash
pip install requests pandas numpy python-dotenv akshare
```
