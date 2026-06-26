---
name: china-stock-quant
description: >-
  A-share quantitative analysis toolkit. Use when user wants to analyze Chinese stocks,
  backtest trading strategies, calculate technical indicators (MACD/KDJ/RSI/Bollinger),
  implement ETF day-trading strategies (grid trading, MA crossover, volatility),
  fetch A-share/ETF market data, or perform risk assessment (max drawdown, Sharpe ratio).
  Triggers on: A股分析, 量化交易, ETF做T, 技术指标, 回测, stock analysis, quantitative trading,
  MACD, KDJ, RSI, 布林带, 网格交易, akshare, 选股策略, backtest.
---

# A股量化分析

基于 akshare（免费无需token）的A股量化分析工具包。

## 快速开始

```bash
pip install akshare pandas numpy matplotlib
```

## 工作流

### 1. 获取数据

```python
from scripts.fetch_data import *
# ETF日线
df = fetch_etf_daily("159915", "20250101", "20260301")
# 个股日线
df = fetch_stock_daily("000001", "20250101", "20260301")
# ETF分时（日内做T）
df = fetch_etf_intraday("159915")
# 实时行情
df = fetch_realtime("159915")
```

详见 `references/api-reference.md`

### 2. 计算技术指标

```python
from scripts.technical_indicators import *
# 单指标
df['macd'], df['signal'], df['hist'] = calc_macd(df['close'])
df['k'], df['d'], df['j'] = calc_kdj(df['high'], df['low'], df['close'])
df['rsi'] = calc_rsi(df['close'], period=14)
df['upper'], df['mid'], df['lower'] = calc_bollinger(df['close'])
df['vol_ratio'] = calc_volume_ratio(df['volume'])
# 一键全部
df = add_all_indicators(df)
# 信号检测
signals = detect_signals(df)
```

### 3. 策略回测

```python
from scripts.backtest import *
result = run_backtest(
    df,
    strategy="grid",           # grid / ma_cross / bollinger
    initial_capital=100000,
    grid_num=10,               # 网格数（grid策略）
    ma_short=5, ma_long=20,    # 均线参数（ma_cross策略）
    stop_loss=0.05,            # 止损比例
    take_profit=0.10,          # 止盈比例
)
print(result.summary())
```

### 4. 风险评估

```python
from scripts.backtest import assess_risk
risk = assess_risk(df['close'])
# returns: max_drawdown, sharpe_ratio, annual_volatility, calmar_ratio
```

## 策略库

ETF日内做T策略详解见 `references/strategies.md`，包含：

| 策略 | 适用场景 | 核心逻辑 |
|------|---------|---------|
| 网格交易 | 震荡市 | 价格跌破网格线买入，涨回卖出 |
| 均线交叉 | 趋势市 | 短均线上穿长均线买入，下穿卖出 |
| 布林带回归 | 均值回归 | 触下轨买入，触上轨卖出 |
| 波动率突破 | 突破行情 | ATR放大+价格突破时追入 |

## 风控参数（内置默认值）

```python
RISK_PARAMS = {
    "max_position_pct": 0.25,    # 单只持仓上限
    "stop_loss": 0.05,           # 止损线 5%
    "take_profit": 0.10,         # 止盈线 10%
    "max_daily_turnover": 0.05,  # 日内做T最大换手
    "min_trade_amount": 10000,   # 最低交易金额（元）
    "max_drawdown_limit": 0.15,  # 最大回撤警戒线
}
```

## 资源文件

- `scripts/fetch_data.py` — 数据获取
- `scripts/technical_indicators.py` — 技术指标计算
- `scripts/backtest.py` — 回测引擎+风险评估
- `references/strategies.md` — 策略库详解
- `references/api-reference.md` — akshare接口速查
