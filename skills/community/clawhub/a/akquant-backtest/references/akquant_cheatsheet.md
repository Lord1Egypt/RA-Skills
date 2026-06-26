# AKQuant 指标速查

## 技术指标

### 趋势指标

#### SMA(period) - 简单移动平均线
```python
sma = aq.SMA(period=20)
sma.update(price)
value = sma.value  # 当前均线值
```

#### EMA(period) - 指数移动平均线
```python
ema = aq.EMA(period=12)
ema.update(price)
value = ema.value
```

#### MACD(fast_period, slow_period, signal_period)
```python
macd = aq.MACD(fast_period=12, slow_period=26, signal_period=9)
macd.update(price)
dif, dea, macd_bar = macd.value  # 返回三个值
```

### 震荡指标

#### RSI(period) - 相对强弱指数
```python
rsi = aq.RSI(period=14)
rsi.update(price)
value = rsi.value  # 0-100
```

### 波动指标

#### BollingerBands(period, multiplier) - 布林带
```python
bb = aq.BollingerBands(period=20, multiplier=2)
bb.update(price)
upper, middle, lower = bb.value  # 上轨、中轨、下轨
```

#### ATR(period) - 平均真实波幅
```python
atr = aq.ATR(period=14)
atr.update(high, low, close)
value = atr.value
```

## AKShare 数据接口

### 股票日线数据
```python
import akshare as ak

df = ak.stock_zh_a_hist(
    symbol="000001",      # 股票代码
    period="daily",       # 周期: daily/weekly/monthly
    start_date="20240101",
    end_date="20241231",
    adjust="qfq"          # 复权: qfq(前复权)/hfq(后复权)
)
```

### 指数数据
```python
# 上证指数
df = ak.index_zh_a_hist(symbol="000001", period="daily")

# 个股实时行情
df = ak.stock_zh_a_spot_em()
```

## 回测配置

### BacktestConfig
```python
config = aq.BacktestConfig(
    initial_capital=100000,    # 初始资金
    commission_rate=0.0003,    # 手续费率
    slippage=0.001,            # 滑点
)
```

## 常用策略模板

### 双均线策略
```python
class DoubleMAStrategy:
    def __init__(self, fast=10, slow=30):
        self.fast_ma = aq.SMA(fast)
        self.slow_ma = aq.SMA(slow)
        
    def on_bar(self, bar):
        self.fast_ma.update(bar['close'])
        self.slow_ma.update(bar['close'])
        
        if self.fast_ma.value > self.slow_ma.value:
            return 'BUY'
        elif self.fast_ma.value < self.slow_ma.value:
            return 'SELL'
        return 'HOLD'
```

### RSI策略
```python
class RsiStrategy:
    def __init__(self, period=14, overbought=70, oversold=30):
        self.rsi = aq.RSI(period)
        self.overbought = overbought
        self.oversold = oversold
        
    def on_bar(self, bar):
        self.rsi.update(bar['close'])
        
        if self.rsi.value < self.oversold:
            return 'BUY'  # 超卖买入
        elif self.rsi.value > self.overbought:
            return 'SELL'  # 超买卖出
        return 'HOLD'
```

## 股票代码参考

| 代码 | 名称 |
|------|------|
| 000001 | 平安银行 |
| 000002 | 万科A |
| 600000 | 浦发银行 |
| 600519 | 贵州茅台 |
| 000858 | 五粮液 |
| 002594 | 比亚迪 |
| 300750 | 宁德时代 |
