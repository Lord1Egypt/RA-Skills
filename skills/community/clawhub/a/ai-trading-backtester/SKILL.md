---
name: "AI Trading Strategy Backtester"
description: "AI-powered quantitative trading strategy backtesting assistant. Designs, codes, and evaluates trading strategies across historical market data. Supports A-share (China), Hong Kong, US equity markets. Covers mean reversion, momentum, breakout, pairs trading, and machine learning-based strategies. Built for quantitative analysts and retail traders. Keywords: trading backtest, quantitative strategy, algorithmic trading, Python backtesting, backtrader, vectorbt, trading strategy, momentum, mean reversion, pairs trading, A-share strategy, financial data, technical indicators."
version: "5.0.0"
---

# AI Trading Strategy Backtester

## Overview

An AI-powered quantitative trading strategy design and backtesting assistant that helps you transform trading ideas into fully-coded, backtested strategies. It guides you through strategy design (mean reversion, momentum, breakout, pairs trading, ML-based), implements them in Python (backtrader, vectorbt, pandas), evaluates performance across historical data for A-share, HK, and US markets, and produces risk-adjusted performance reports.

## Triggers

- "backtest my trading strategy"
- "design a momentum strategy for [stock/market]"
- "test mean reversion on [symbol]"
- "pairs trading strategy example"
- "Python backtrader setup guide"
- "vectorbt tutorial"
- "trading strategy optimization"
- "量化回测策略"
- "技术指标择时策略"
- "A股量化策略设计"

## Workflow

### Step 1: Define the Strategy Brief

Collect the trading idea:
- **Strategy type**: Momentum, mean reversion, breakout, pairs trading, ML-based, event-driven
- **Market**: A-share (sh/sz), HK stock (hk), US equity (us)
- **Timeframe**: Intraday (1m/5m/15m), daily, weekly, monthly
- **Assets**: Single stock, ETF, index, portfolio
- **Entry/Exit signals**: Technical indicators, price patterns, fundamental signals, ML predictions
- **Position sizing**: Fixed, Kelly criterion, risk-parity, dynamic
- **Constraints**: Max position size, long-only/short, turnover limit, slippage model

### Step 2: Strategy Design & Code Generation

Based on the brief, generate production-quality Python code:

#### A. Momentum Strategy Template
```python
import pandas as pd
import numpy as np
import backtrader as bt

class MomentumStrategy(bt.Strategy):
    params = (
        ('lookback', 20),       # 回望期
        ('hold_period', 5),    # 持有期
        ('rank_percentile', 0.2),  # 选股分位数
    )

    def __init__(self):
        self.inds = {}
        for d in self.datas:
            self.inds[d] = {}
            self.inds[d]['momentum'] = bt.indicators.RateOfChange(
                d.close, period=self.params.lookback
            )

    def next(self):
        # 按动量排序，取前20%
        rankings = sorted(
            self.datas,
            key=lambda d: self.inds[d]['momentum'][0],
            reverse=True
        )[:int(len(self.datas) * self.params.rank_percentile)]

        # 平仓不在榜单的持仓
        for d in self.datas:
            if d not in rankings and self.getposition(d).size > 0:
                self.close(d)

        # 买入榜单中的标的
        for d in rankings:
            if self.getposition(d).size == 0:
                self.order_target_percent(d, 1.0 / len(rankings))
```

#### B. Mean Reversion Strategy Template
```python
class MeanReversionStrategy(bt.Strategy):
    params = (
        ('bb_period', 20),
        ('bb_dev', 2.0),
        ('rsi_period', 14),
        ('rsi_oversold', 30),
        ('rsi_overbought', 70),
    )

    def __init__(self):
        self.bb = bt.indicators.BollingerBands(
            self.data.close, period=self.params.bb_period,
            devfactor=self.params.bb_dev
        )
        self.rsi = bt.indicators.RSI(
            self.data.close, period=self.params.rsi_period
        )

    def next(self):
        if self.position.size == 0:
            # 价格触及下轨且RSI超卖 → 买入
            if self.data.close < self.bb.lines.bot and \
               self.rsi < self.params.rsi_oversold:
                self.order_target_percent(self.data, 1.0)
        else:
            # 价格触及上轨或RSI超买 → 卖出
            if self.data.close > self.bb.lines.top or \
               self.rsi > self.params.rsi_overbought:
                self.close()
```

#### C. Pairs Trading Strategy
```python
import statsmodels.api as sm

def find_cointegrated_pairs(data_dict):
    """寻找协整配对"""
    n = len(data_dict)
    pairs = []
    symbols = list(data_dict.keys())

    for i in range(n):
        for j in range(i + 1, n):
            try:
                x = data_dict[symbols[i]]
                y = data_dict[symbols[j]]
                # OLS回归
                X = sm.add_constant(x)
                model = sm.OLS(y, X).fit()
                residuals = model.resid
                # ADF检验
                adf_result = sm.tsa.stattools.adfuller(residuals)
                if adf_result[0] < adf_result[4]['1%']:
                    pairs.append((symbols[i], symbols[j], adf_result[0]))
            except:
                continue
    return sorted(pairs, key=lambda x: x[2])

def pairs_trading_signals(spread, z_entry=2.0, z_exit=0.5):
    """配对交易信号"""
    signals = pd.Series(0, index=spread.index)
    z_score = (spread - spread.mean()) / spread.std()

    signals[z_score < -z_entry] = 1    # 做多价差
    signals[z_score > z_entry] = -1     # 做空价差
    signals[abs(z_score) < z_exit] = 0  # 平仓
    return signals
```

### Step 3: Backtest Execution

Guide the user through running the backtest:

```python
import backtrader as bt
import pandas as pd

# 加载数据
data = bt.feeds.GenericCSVData(
    dataname='historical_data.csv',
    dtformat='%Y-%m-%d',
    datetime=0,
    open=1, high=2, low=3, close=4, volume=5,
    openinterest=-1
)

# 运行回测
cerebro = bt.Cerebro()
cerebro.addstrategy(MomentumStrategy)
cerebro.adddata(data)
cerebro.broker.setcash(1000000.0)  # 100万初始资金
cerebro.broker.setcommission(commission=0.001)  # 千一手续费
cerebro.addsizer(bt.sizers.PercentSizer, percents=95)

print(f'初始资金: {cerebro.broker.getvalue():,.2f}')
cerebro.run()
print(f'最终资金: {cerebro.broker.getvalue():,.2f}')
```

### Step 4: Performance Analysis

Generate comprehensive performance metrics:

| Metric | Description | Target |
|--------|-------------|--------|
| Total Return | Cumulative return | > Benchmark |
| Annualized Return | CAGR | > 10% (A-share), > 8% (HK/US) |
| Sharpe Ratio | Risk-adjusted return | > 1.5 |
| Max Drawdown | Peak-to-trough loss | < 20% |
| Win Rate | Percentage of profitable trades | > 50% |
| Profit Factor | Gross profit / Gross loss | > 1.5 |
| Calmar Ratio | Annual return / Max DD | > 1.0 |
| Sortino Ratio | Return / Downside deviation | > 1.0 |

### Step 5: Optimization & Stress Testing

```
A. 参数优化
   - Grid search over key parameters
   - Walk-forward analysis (in-sample / out-of-sample)
   - Avoid overfitting: use Information Coefficient (IC) analysis

B. 压力测试
   - Historical crises: 2008, 2015 A-share crash, COVID-19 (2020)
   - Monte Carlo simulation of equity curves
   - Sensitivity analysis: commission, slippage, spread assumptions

C. 风险分析
   - Position-level VaR (Value at Risk)
   - Factor exposure (momentum, size, volatility)
   - Tail risk: maximum loss scenarios
```

## Input/Output Examples

### Example 1: Strategy Design Request

**Input:**
```
Design a momentum strategy for A-share market.
Criteria:
- Daily timeframe
- Lookback: 20 days
- Hold for 5 days
- Long only
- Top 20% by momentum score
- Max 10 positions
- Trade AAPL, TSLA, NVDA, MSFT
```

**Output:**
```
Strategy Design Summary:

┌─────────────────────────────────────────┐
│ Strategy: Top-Momentum Long-Only        │
│ Market: US Equity (4 stocks)            │
│ Timeframe: Daily                        │
│ Backtest Period: 2020-01-01 to 2025-12-31 │
└─────────────────────────────────────────┘

Key Components:
1. Momentum ranking: ROC(close, period=20)
2. Selection: Top 20% by momentum score (max 10 stocks)
3. Position sizing: Equal weight (10% per position)
4. Hold period: 5 trading days
5. Rebalance: Daily at market open

Expected Performance (illustrative):
- Annualized Return: 18-25% (historical backtest)
- Sharpe Ratio: 0.8-1.2
- Max Drawdown: 30-40%
- Win Rate: 52-56%

Code generated at: strategy_momentum_us.py
```

### Example 2: Performance Report

**Input:**
```
Compare these two strategies: RSI mean reversion vs momentum breakout on CSI 300 (000300)
Period: 2020-2024
Initial capital: 1,000,000 CNY
```

**Output:**
```
Backtest Results: CSI 300 Strategies (2020-2024)

┌──────────────────────┬─────────────────────┬────────────────────┐
│ Metric               │ RSI Mean Reversion  │ Momentum Breakout  │
├──────────────────────┼─────────────────────┼────────────────────┤
│ Total Return         │ +68.3%              │ +124.7%            │
│ Annualized Return    │ +13.2%              │ +17.8%             │
│ Sharpe Ratio         │ 1.12               │ 1.45               │
│ Max Drawdown         │ -22.1%             │ -31.4%             │
│ Win Rate             │ 58.3%              │ 49.2%              │
│ Profit Factor        │ 1.82               │ 1.67               │
│ Calmar Ratio         │ 0.60               │ 0.57               │
│ Avg Holding Days     │ 8.2                │ 4.6                │
│ Total Trades         │ 127                │ 284                │
└──────────────────────┴─────────────────────┴────────────────────┘
Benchmark: CSI 300 Index (+42.1% over same period)

Recommendation:
- Risk-averse investors: RSI Mean Reversion (lower drawdown, higher win rate)
- Return-seeking investors: Momentum Breakout (higher return, more trades)

⚠️ Note: Past performance does not guarantee future results.
A-share markets are subject to significant regulatory and liquidity risks.
```

## Strategy Templates Library

| Strategy Type | Best For | Timeframe | Markets |
|--------------|----------|-----------|---------|
| Momentum | Trending markets | Daily/Weekly | All |
| Mean Reversion | Range-bound markets | Intraday/Daily | All |
| Breakout | Volatile markets | Intraday/Daily | All |
| Pairs Trading | Market-neutral | Daily | US/HK |
| Machine Learning | Alpha discovery | Daily | All |
| Event-Driven | Corporate actions | Daily | A-share/US |

## Best Practices

1. **Always use out-of-sample testing** — split data 70/30 or use walk-forward
2. **Account for transaction costs** — A-share commission + stamp tax ≈ 0.15% per trade
3. **Include slippage** — assume 0.05-0.1% for liquid stocks, higher for illiquid
4. **Diversify across uncorrelated strategies** — don't rely on one strategy
5. **Stress test for A-share specifics** — T+1 trading, limit-up/limit-down, suspension risks
6. **Validate with paper trading** — run live for 1-3 months before real capital
7. **Beware of overfitting** — fewer parameters = more robust strategy

## Risk Disclaimer

This skill provides backtesting tools and historical analysis for educational and research purposes only. Backtested results are not indicative of future performance. Real trading involves significant risks including market volatility, liquidity constraints, regulatory changes, and model risk. Always consult with qualified financial advisors before making investment decisions.
## Appendix G. Alibaba Dianjin Fusion — ai-trading-backtester v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `investment-advisor` (AI投资顾问) & `quant-researcher` (AI量化研究员)  
> **Essence**: 策略回测、参数优化、风险控制、绩效评估  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
策略回测流程：
1. 策略定义：买入条件+卖出条件+止损条件
2. 数据准备：历史K线+成交量+因子数据
3. 回测执行：按时间顺序模拟交易
4. 绩效计算：收益率+夏普比率+最大回撤
5. 参数优化：网格搜索/贝叶斯优化
6. 风险分析：回撤期+胜率+盈亏比
```

---

### G.2 Backtest Metrics (Dianjin method)

**核心指标体系**：

| 指标 | 计算公式 | 优秀标准 | 及格标准 |
|------|---------|---------|---------|
| 年化收益率 | (终值/初值)^(252/交易日)-1 | >20% | >8% |
| 夏普比率 | (年化收益-无风险利率)/年化波动 | >1.5 | >0.5 |
| 最大回撤 | max((历史最高-当前)/历史最高) | <15% | <30% |
| 胜率 | 盈利次数/总次数 | >60% | >45% |
| 盈亏比 | 平均盈利/平均亏损 | >2.0 | >1.5 |
| 索提诺比率 | (年化收益-无风险利率)/下行波动 | >2.0 | >1.0 |

**回测报告模板（Dianjin风格）**：

```
【策略回测报告】均线突破策略（5日+20日）

一、回测参数
- 标的：沪深300指数 (000300.SH)
- 周期：2019-01-01 至 2026-05-31
- 频率：日线
- 初始资金：100万
- 交易成本：单边0.1%（佣金0.03%+印花税0.07%）

二、绩效指标
✅ 年化收益率：18.5%（优秀）
✅ 夏普比率：1.62（优秀）
❌ 最大回撤：-28.3%（不及格，应<15%）
⚠️ 胜率：52.3%（及格）
⚠️ 盈亏比：1.85（及格）

三、分年度表现
| 年份 | 收益率 | 最大回撤 | 夏普比率 |
|------|--------|----------|----------|
| 2019 | +32.5% | -12.3% | 2.1 |
| 2020 | +28.7% | -15.8% | 1.8 |
| 2021 | -8.2% | -22.5% | -0.3 |
| 2022 | -15.3% | -28.3% | -0.8 |
| 2023 | +22.1% | -10.5% | 1.5 |
| 2024 | +12.8% | -8.7% | 1.2 |
| 2025 | +25.6% | -9.2% | 1.9 |

四、问题诊断
❌ 2022年回撤-28.3%（策略在熊市表现差）
❌ 胜率仅52.3%（信号质量不高）
⚠️ 交易成本年化-3.2%（高频交易成本高）

五、改进建议
1. 增加趋势过滤（仅在MA60向上时开仓）
2. 优化止损（当前-8%止损太宽，改为-5%）
3. 降低交易频率（当前年均交易45次，降至20次以下）
```

---

### G.3 Parameter Optimization (Dianjin essence)

**参数优化方法**：

```
方法1：网格搜索（Grid Search）
  - 优点：简单，保证找到全局最优
  - 缺点：计算量大（参数多时指数爆炸）
  - 适用：参数少（<5个），范围小

方法2：贝叶斯优化（Bayesian Optimization）
  - 优点：高效，用高斯过程建模目标函数
  - 缺点：实现复杂，可能陷入局部最优
  - 适用：参数多（>5个），计算资源有限

方法3：遗传算法（Genetic Algorithm）
  - 优点：全局搜索能力强，适合复杂目标
  - 缺点：收敛慢，参数调优难
  - 适用：非线性、多峰目标函数
```

**过拟合风险警示（Dianjin重点）**：

```
⚠️ 过拟合信号：
1. 样本内绩效远优于样本外（差距>50%）
2. 参数极度敏感（微调参数导致绩效剧变）
3. 交易次数过少（<20次，统计不显著）
4. 最大回撤发生在样本末端（未来函数嫌疑）

✅ 防过拟合措施：
1. 样本外测试（保留最近1-2年数据不参训）
2. 滚动窗口验证（Walk-forward，每N个月重新优化）
3. 参数稳定性检验（参数在合理范围内波动，绩效不剧变）
4. 经济逻辑检验（策略要有合理解释，不能纯数据挖掘）
```

---

### G.4 Risk Control & Position Management (Dianjin method)

**仓位管理模型**：

```
固定比例法（最简单）：
  - 单一策略：股票仓位≤30%
  - 组合策略：总仓位≤80%

凯利公式（Kelly Criterion）：
  仓位 = (胜率 × 盈亏比 - 败率) / 盈亏比
  例：胜率55%，盈亏比2.0 → 仓位 = (0.55×2-0.45)/2 = 32.5%

ATR仓位法（波动率调整）：
  仓位 = 账户资金 × 风险系数 / (ATR × 合约乘数)
  例：账户100万，风险系数0.02，ATR=2元，合约乘数100
  → 仓位 = 100万 × 0.02 / (2×100) = 100股（约占总资金2%）
```

---

### G.5 Test Case (Dianjin quality)

**Test Case: 策略回测+优化**

```
Input: "回测均线突破策略（5日+20日）在沪深300的表现，2019-2026"

Expected Output:
1. 回测参数（标的/周期/成本）
2. 绩效指标表（年化收益/夏普/最大回撤/胜率/盈亏比）
3. 分年度表现
4. 问题诊断（回撤过大/胜率过低）
5. 改进建议（增加过滤/优化止损）

Quality Check:
- ✅ 指标计算准确（公式正确）
- ✅ 问题诊断客观（不回避缺陷）
- ✅ 改进建议可行（有实操价值）
- ✅ 风险提示（过拟合风险）
```

---

**End of Dianjin Fusion Content — ai-trading-backtester v5.0.0**
