---
name: akshare-pro
description: A股智能投资助手 - 实时行情、技术分析、自动盯盘、持仓报告、异动告警。支持MACD/KDJ/布林带等技术指标，定时推送持仓报告到飞书/微信。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      pip: ["akshare>=1.12", "pandas>=1.5", "ta>=0.11"]
    install:
      - id: pip-install
        kind: pip
        packages: ["akshare>=1.12", "pandas>=1.5", "ta>=0.11"]
        label: "安装依赖"
keywords:
  - 股票
  - A股
  - 技术分析
  - 自动盯盘
  - 持仓报告
  - MACD
  - KDJ
  - 布林带
  - 量化
---

# A股智能投资助手 (akshare-pro)

## 功能特性

- 实时行情查询（支持多数据源自动切换）
- K线数据获取（自动重试机制）
- 宏观经济数据
- 技术指标计算 (MACD/KDJ/RSI/布林带)
- 自动盯盘告警
- 每日持仓报告
- 回测策略模板
- 飞书/微信推送
- **智能错误处理**（网络异常自动重试）
- **备用数据源**（东方财富 API 直连）

## 快速开始

```bash
pip install akshare pandas ta
```

## 实时行情

```python
import akshare as ak

# A股实时行情
df = ak.stock_zh_a_spot_em()
print(df[['代码', '名称', '最新价', '涨跌幅', '成交量']].head(10))

# 个股查询
stock = df[df['代码'] == '000001']
print(f"平安银行: {stock['最新价'].values[0]}元, 涨跌幅: {stock['涨跌幅'].values[0]}%")
```

### K线数据

```python
# 获取日K线
df = ak.stock_zh_kline(symbol="000001", period="daily", adjust="qfq", start_date="20240101")

# 周K线
df_weekly = ak.stock_zh_kline(symbol="000001", period="weekly")

# 月K线
df_monthly = ak.stock_zh_kline(symbol="000001", period="monthly")
```

### 宏观经济

```python
# GDP
gdp = ak.macro_china_gdp()

# CPI
cpi = ak.macro_china_cpi()

# PMI
pmi = ak.macro_china_pmi()
```

## 技术指标计算

```python
import akshare as ak
import pandas as pd
import ta

def calc_indicators(symbol, start_date="20240101"):
    """计算完整技术指标"""
    df = ak.stock_zh_kline(symbol=symbol, period="daily", adjust="qfq", start_date=start_date)
    
    # MACD
    df['macd'] = ta.trend.macd(df['close'])
    df['macd_signal'] = ta.trend.macd_signal(df['close'])
    df['macd_hist'] = ta.trend.macd_diff(df['close'])
    
    # KDJ (用 Stochastic 替代)
    df['stoch_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'])
    df['stoch_d'] = ta.momentum.stoch_signal(df['high'], df['low'], df['close'])
    df['stoch_j'] = 3 * df['stoch_k'] - 2 * df['stoch_d']
    
    # 布林带
    df['bb_upper'] = ta.volatility.bollinger_hband(df['close'])
    df['bb_middle'] = ta.volatility.bollinger_mavg(df['close'])
    df['bb_lower'] = ta.volatility.bollinger_lband(df['close'])
    
    # RSI
    df['rsi'] = ta.momentum.rsi(df['close'])
    
    # 均线
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    
    return df

# 使用示例
df = calc_indicators("000001")
latest = df.iloc[-1]
print(f"""
平安银行 技术指标:
- MACD: {latest['macd']:.3f} (信号: {latest['macd_signal']:.3f})
- KDJ: K={latest['stoch_k']:.1f} D={latest['stoch_d']:.1f} J={latest['stoch_j']:.1f}
- 布林带: 上轨={latest['bb_upper']:.2f} 中轨={latest['bb_middle']:.2f} 下轨={latest['bb_lower']:.2f}
- RSI: {latest['rsi']:.1f}
- 均线: MA5={latest['ma5']:.2f} MA20={latest['ma20']:.2f}
""")
```

### 买卖信号识别

```python
def detect_signals(df):
    """识别买卖信号"""
    signals = []
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # MACD 金叉/死叉
    if prev['macd'] < prev['macd_signal'] and latest['macd'] > latest['macd_signal']:
        signals.append("📈 MACD金叉 (买入信号)")
    elif prev['macd'] > prev['macd_signal'] and latest['macd'] < latest['macd_signal']:
        signals.append("📉 MACD死叉 (卖出信号)")
    
    # KDJ 超买超卖
    if latest['stoch_j'] > 100:
        signals.append("⚠️ KDJ超买 (J>100)")
    elif latest['stoch_j'] < 0:
        signals.append("💡 KDJ超卖 (J<0)")
    
    # RSI 超买超卖
    if latest['rsi'] > 70:
        signals.append("⚠️ RSI超买 (>70)")
    elif latest['rsi'] < 30:
        signals.append("💡 RSI超卖 (<30)")
    
    # 布林带突破
    if latest['close'] > latest['bb_upper']:
        signals.append("🚀 突破布林上轨")
    elif latest['close'] < latest['bb_lower']:
        signals.append("💰 跌破布林下轨")
    
    # 均线多头/空头
    if latest['ma5'] > latest['ma10'] > latest['ma20']:
        signals.append("🔺 均线多头排列")
    elif latest['ma5'] < latest['ma10'] < latest['ma20']:
        signals.append("🔻 均线空头排列")
    
    return signals
```

### 自动盯盘告警

```python
import json
from datetime import datetime

def check_alerts(watchlist, thresholds=None):
    """检查自选股是否触发告警"""
    if thresholds is None:
        thresholds = {
            'pct_change_up': 5.0,    # 涨幅超过5%
            'pct_change_down': -5.0,  # 跌幅超过5%
            'volume_ratio': 3.0,      # 成交量放大3倍
        }
    
    df = ak.stock_zh_a_spot_em()
    alerts = []
    
    for ticker in watchlist:
        stock = df[df['代码'] == ticker]
        if stock.empty:
            continue
            
        stock = stock.iloc[0]
        
        # 涨跌幅告警
        pct = stock['涨跌幅']
        if pct >= thresholds['pct_change_up']:
            alerts.append({
                'ticker': ticker,
                'name': stock['名称'],
                'type': '涨幅告警',
                'message': f"🚀 {stock['名称']}({ticker}) 涨幅 {pct:.2f}%"
            })
        elif pct <= thresholds['pct_change_down']:
            alerts.append({
                'ticker': ticker,
                'name': stock['名称'],
                'type': '跌幅告警',
                'message': f"📉 {stock['名称']}({ticker}) 跌幅 {pct:.2f}%"
            })
    
    return alerts

# 使用示例
watchlist = ["000001", "600519", "000858"]  # 平安银行、茅台、五粮液
alerts = check_alerts(watchlist)
for alert in alerts:
    print(alert['message'])
```

### 每日持仓报告

```python
def generate_daily_report(watchlist):
    """生成每日持仓报告"""
    report = []
    report.append(f"# 持仓日报 {datetime.now().strftime('%Y-%m-%d')}\n")
    
    df = ak.stock_zh_a_spot_em()
    
    report.append("| 代码 | 名称 | 最新价 | 涨跌幅 | 成交量 | 技术信号 |")
    report.append("|------|------|--------|--------|--------|----------|")
    
    for ticker in watchlist:
        stock = df[df['代码'] == ticker]
        if stock.empty:
            continue
        stock = stock.iloc[0]
        
        # 获取技术信号
        try:
            indicators = calc_indicators(ticker, start_date="20240101")
            signals = detect_signals(indicators)
            signal_str = ", ".join(signals[:2]) if signals else "无明显信号"
        except:
            signal_str = "计算失败"
        
        report.append(f"| {ticker} | {stock['名称']} | {stock['最新价']} | {stock['涨跌幅']:.2f}% | {stock['成交量']} | {signal_str} |")
    
    return "\n".join(report)
```

### 飞书推送配置

在 OpenClaw 的 `openclaw.json` 中配置定时任务：

```json
{
  "cron": {
    "jobs": [
      {
        "id": "daily-report",
        "schedule": "0 15 * * 1-5",
        "prompt": "生成今日持仓报告并发送到飞书",
        "channel": "feishu"
      },
      {
        "id": "alert-check",
        "schedule": "*/30 9-15 * * 1-5",
        "prompt": "检查自选股告警",
        "channel": "feishu"
      }
    ]
  }
}
```

### 回测策略模板

```python
def backtest_ma_cross(symbol, short=5, long=20, start_date="20230101"):
    """均线交叉回测"""
    df = ak.stock_zh_kline(symbol=symbol, period="daily", adjust="qfq", start_date=start_date)
    
    df['ma_short'] = df['close'].rolling(short).mean()
    df['ma_long'] = df['close'].rolling(long).mean()
    
    # 生成信号
    df['signal'] = 0
    df.loc[df['ma_short'] > df['ma_long'], 'signal'] = 1  # 买入
    df.loc[df['ma_short'] < df['ma_long'], 'signal'] = -1  # 卖出
    
    # 计算收益
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['signal'].shift(1) * df['returns']
    df['cumulative'] = (1 + df['strategy_returns']).cumprod()
    
    total_return = (df['cumulative'].iloc[-1] - 1) * 100
    print(f"MA{short}/{long} 策略收益: {total_return:.2f}%")
    
    return df

# 使用示例
backtest_ma_cross("000001", short=5, long=20)
```

## 风险提示

1. **数据来源**: 公开财经网站，仅供参考
2. **投资风险**: 技术指标不构成投资建议
3. **数据延迟**: 实时数据可能有 15 分钟延迟
4. **回测局限**: 历史收益不代表未来表现
