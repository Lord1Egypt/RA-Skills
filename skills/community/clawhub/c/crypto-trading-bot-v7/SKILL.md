---
name: crypto-trading-bot
description: >
  加密貨幣交易機器人開發 - 幫你整自動交易Bot，支持Pine Script、Python、CCXT API對接。
  適用於：(1)整TradingView信號Bot (2)CEX/DEX API自動化 (3)套利機器人 (4)止盈止損策略 (5)策略回測 (6)高级风控 (7)多策略框架
---

# Crypto Trading Bot Developer

幫你整加密貨幣自動交易機器人

## 核心功能

### 1. TradingView Pine Script 信号 Bot
- 接收TradingView webhook信號
- 自動執行買賣指令
- 支持多交易所對接

### 2. CEX 自動化交易
- Binance, Bybit, OKX API 對接
- 現貨/合約自動化
- 網格交易策略

### 3. 策略回測
- 多周期回測 (1H/4H/1D)
- 多幣種組合回測
- 核心指標：收益率、最大回撤、勝率、夏普比率、盈虧比
- Excel導出交易記錄和資金曲線

### 4. 高级风控系统 (DynamicRiskManager)
**风控优先级最高，贯穿整个交易流程**

| 功能 | 说明 |
|------|------|
| 波动率过滤 | ATR超过历史高百分位(90%)时暂停开仓 |
| 动态止损 | ATR倍数随波动率动态调整(0.8x~2.0x) |
| 移动止损 | 价格向有利方向移动≥1.0ATR后激活，偏移0.5ATR |
| 仓位计算 | 基于账户权益×1.5%单笔风险 |

### 5. 手续费规则 (BNB折扣)

| 市场 | Maker | Taker | BNB折扣后 |
|------|-------|-------|----------|
| 现货 | 0.1000% | 0.1000% | **0.075%** |
| U本位合约 | 0.0200% | 0.0500% | 0.018%/0.045% |
| 币本位合约 | 0.0000% | 0.0360% | 0.000%/0.036% |

**注意**：高频交易策略需特别注意手续费侵蚀利润！

### 6. 多策略框架 (策略模块更新.txt)
模块化策略系统，支持：

| 模块 | 功能 |
|------|------|
| **MarketStateDetector** | 基于ADX判断趋势/震荡市场 |
| **SupertrendStrategy** | 趋势跟踪策略 |
| **MeanReversionStrategy** | RSI均值回归策略 |
| **StrategySelector** | 根据市场状态自动切换策略 |
| **SignalFusion** | 多策略加权信号融合 |
| **PortfolioAllocator** | 多策略资金分配 |

## 回测引擎版本

| 版本 | 文件 | 说明 |
|------|------|------|
| v1 | backtest_engine.py | 基础RSI+MACD策略 |
| v2 | backtest_engine_v2.py | 多空双向+动态RSI阈值 |
| v3 | backtest_engine_v3.py | 整合高级风控 |
| v4 | backtest_engine_v4.py | 多策略框架+风控 |
| **v5** | **backtest_engine_v5.py** | **稳健基础版 (Supertrend+MTF)** |
| **v6** | **backtest_engine_v6.py** | **含MTF过滤+分批止盈** |
| **v7** | **backtest_engine_v7.py** | **多周期+趋势/震荡自适应+网格** |

## 快速回测命令

```bash
cd /home/user/.openclaw/workspace
source .venv/bin/activate

# v3: 基础多空策略 + 风控
python3 backtest_engine_v3.py

# v4: 多策略框架 + 风控
python3 backtest_engine_v4.py

# v6: MTF过滤 + 分批止盈 (推荐)
python3 backtest_engine_v6.py

# v7: 多周期自适应策略 (最新)
python3 backtest_engine_v7.py
```

## V7策略详情

**V7多周期短线策略** (`scripts/v7_strategy/backtest_engine_v7.py`)

核心特点：
- 多周期分析：日线定方向、4H定区间、1H主信号
- 自适应策略选择：ADX>25用趋势策略，ADX≤25用震荡策略
- 动态风控：杠杆4x、ATR止损、移动止损
- 网格加仓：震荡市场中最多3次加仓
- 分批止盈：布林带中轨平半、对侧全平

适用场景：
- 波动较大的币种 (SOL, AXS, GMT等)
- 趋势和震荡交替的市场

## 策略模块使用

```python
from strategy_modules import (
    MarketStateDetector,    # 市场状态识别
    SupertrendStrategy,     # 趋势策略
    MeanReversionStrategy,  # 均值回归策略
    StrategySelector,       # 策略选择器
    SignalFusion,           # 信号融合
    PortfolioAllocator      # 资金分配
)

# 初始化
risk_mgr = DynamicRiskManager(risk_per_trade=0.015, ...)
market_detector = MarketStateDetector()
supertrend = SupertrendStrategy()
meanrev = MeanReversionStrategy()

# 信号融合模式
fusion = SignalFusion([supertrend, meanrev], weights=[0.6, 0.4])
signal = fusion.generate_signal(high, low, close)

# 策略选择模式
selector = StrategySelector(market_detector, {'Supertrend': supertrend, 'MeanReversion': meanrev})
selected = selector.select_strategy(high, low, close)
```

## 文件结构

```
skills/crypto-trading-bot/
├── SKILL.md
├── scripts/
│   ├── hourly_contrarian_strategy_v2.pine    # Pine Script策略
│   └── strategy_modules.py                      # 多策略框架模块
└── _meta.json

/home/user/.openclaw/workspace/
├── backtest_engine_v3.py                       # 回测引擎v3
├── backtest_engine_v4.py                       # 回测引擎v4 (多策略)
├── 策略模块更新.txt                            # 策略模块源码
├── 风控逻辑.txt                               # 风控模块源码
└── crypto_backtest_v*.xlsx                    # 回测报告
```

## 數據獲取

- Binance公開數據：https://data.binance.vision
- 月度K線：`/data/spot/monthly/klines/{SYMBOL}/{TIMEFRAME}/{SYMBOL}-{TIMEFRAME}-{YYYY-MM}.zip`
- 支持周期：1m~1mo
