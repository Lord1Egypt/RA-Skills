---
name: china-technical-analysis
description: Compute and analyze technical indicators (MACD, KDJ, RSI, Moving Averages, Bollinger Bands) for Chinese futures markets. Generate buy/sell signals and chart descriptions based on data from china-commodity-quotes.
emoji: 📉
metadata:
  openclaw:
    requires:
      bins:
        - curl
    envVars: []
    dependencies:
      skills:
        - china-commodity-quotes
---

# China Technical Analysis — 中国期货技术分析

Compute technical indicators and generate trading signals for Chinese commodity futures, financial index futures, crude oil, and shipping index markets.

**Use this skill when:**
- User asks for MACD, KDJ, RSI, 金叉死叉, or any technical indicator analysis
- User wants buy/sell signals for a specific futures contract
- User asks to "看下XX的走势" or "分析一下XX的技术面"
- User wants to know if a contract is overbought/oversold
- User wants channel, support/resistance levels

## Quick Start

### Recommended Flow

1. **Fetch quote data** → Use `china-commodity-quotes` to get price data for the target contract
2. **Calculate indicators** → Use formulas below to compute MACD, MA, RSI, Bollinger Bands, KDJ
3. **Generate signal** → Combine indicators and output buy/sell/neutral recommendation
4. **Present result** → Format with clear buy/sell signals and chart description

### Data Sources

Through `china-commodity-quotes`, you can get:
- `open`, `high`, `low`, `close` (daily or intraday)
- `volume` and `open_interest`
- Historical bar data via Sina Finance API

**For multi-day historical data (best for indicators):**
```
https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_=new%20Date().getTime()/InnerFuturesNewService.getDailyKLine?symbol=<CONTRACT_CODE>&datalen=<DAYS>
```

Example (curl):
```bash
curl -s "https://stock2.finance.sina.com.cn/futures/api/jsonp.php/InnerFuturesNewService.getDailyKLine?symbol=IF0&datalen=60"
```

**For minute-level data:**
```
https://stock2.finance.sina.com.cn/futures/api/jsonp.php/InnerFuturesNewService.getMinLine?symbol=<CONTRACT_CODE>&type=<M1|M5|M15|M30|M60>
```

## Technical Indicator Formulas

### 1. Moving Averages (MA — 均线系统)

**Simple Moving Average (SMA):**
```
SMA(n) = (C1 + C2 + ... + Cn) / n
```
Where C = closing price, n = period

**Common periods for Chinese futures:**
- MA5 (5-day) — short-term trend
- MA10 (10-day) — short-term support/resistance
- MA20 (MA20) — mid-term trend
- MA60 (60-day) — long-term trend
- MA120 (120-day) — major trend line

**Golden Cross (金叉) — Buy Signal:**
Short-term MA crosses ABOVE long-term MA (e.g., MA5 上穿 MA20)

**Death Cross (死叉) — Sell Signal:**
Short-term MA crosses BELOW long-term MA (e.g., MA5 下穿 MA20)

### 2. MACD (指数平滑异同移动平均线)

**Step-by-step calculation:**

```
Step 1: EMA12 = EMA(C, 12)    — Fast EMA
Step 2: EMA26 = EMA(C, 26)    — Slow EMA
Step 3: DIF = EMA12 - EMA26    — Difference
Step 4: DEA = EMA(DIF, 9)      — Signal line (9-day EMA of DIF)
Step 5: MACD bar = 2 × (DIF - DEA)   — Histogram
```

**EMA calculation (recursive):**
```
EMA(today) = (C × K) + (EMA(yesterday) × (1 - K))
Where K = 2 / (N + 1)
```

**Signals:**
| Signal | Condition | Interpretation |
|:-------|:----------|:--------------|
| Golden cross | DIF crosses above DEA | Bullish 🟢 |
| Death cross | DIF crosses below DEA | Bearish 🔴 |
| Zero crossing (up) | DIF crosses above 0 | Trend turning bullish |
| Zero crossing (down) | DIF crosses below 0 | Trend turning bearish |
| Divergence (bullish) | Price lower low, MACD higher low | Reversal up ⬆️ |
| Divergence (bearish) | Price higher high, MACD lower high | Reversal down ⬇️ |

### 3. RSI (相对强弱指标)

```
RSI(n) = 100 - [100 / (1 + RS)]
RS = AvgGain(n) / AvgLoss(n)
```

Where:
- `AvgGain(n)` = average of up-moves over n periods
- `AvgLoss(n)` = average of down-moves over n periods
- Default period: n = 14

**Interpretation:**
| RSI Range | Signal |
|:---------|:-------|
| > 80 | Overbought (超买) — potential sell ⚠️ |
| 70 - 80 | Strongly bullish, nearing overbought |
| 30 - 70 | Normal range |
| 20 - 30 | Strongly bearish, nearing oversold |
| < 20 | Oversold (超卖) — potential buy ⚠️ |

### 4. Bollinger Bands (布林带)

```
Middle Band = SMA(n)
Upper Band  = Middle Band + (k × StdDev(n))
Lower Band  = Middle Band - (k × StdDev(n))
```

Where:
- n = 20 (default period)
- k = 2 (default multiplier)
- StdDev = standard deviation of closing prices

**Interpretation:**
| Pattern | Meaning |
|:--------|:--------|
| Price touches upper band | Overbought; potential resistance |
| Price touches lower band | Oversold; potential support |
| Price breaks above upper band | Strong momentum; trend continuation |
| Price breaks below lower band | Strong momentum; trend continuation |
| Bands squeeze (narrowing) | Low volatility; impending breakout |
| Bands expand (widening) | High volatility |

### 5. KDJ (随机指标 — Chinese Traders' Favorite)

KDJ is a derivative of the Stochastic Oscillator, widely used by Chinese futures traders.

```
Step 1: RSV = (C - L9) / (H9 - L9) × 100
   Where C = today's close, L9 = lowest low of 9 periods, H9 = highest high of 9 periods

Step 2: K = (2/3 × K(yesterday)) + (1/3 × RSV)
Step 3: D = (2/3 × D(yesterday)) + (1/3 × K(today))
Step 4: J = (3 × K) - (2 × D)
```

**Interpretation:**
| Value | Meaning |
|:------|:--------|
| K > D | Uptrend |
| K < D | Downtrend |
| K/D/J > 80 | Overbought |
| K/D/J < 20 | Oversold |
| Golden cross (K ↑ D) | Buy signal (especially < 20) |
| Death cross (K ↓ D) | Sell signal (especially > 80) |
| J > 100 | Top warning 🔴 |
| J < 0 | Bottom warning 🟢 |

## Signal Generation Logic

### Composite Signal Scoring

Assign weights to get a combined signal:

| Indicator | Buy Signal | Sell Signal | Weight |
|:----------|:-----------|:------------|:------:|
| MACD | DIF ↑ DEA, DIF > 0 | DIF ↓ DEA, DIF < 0 | 30% |
| RSI | RSI < 30 → oversold | RSI > 70 → overbought | 20% |
| MA | Price > MA5 > MA10 > MA20 | Price < MA5 < MA10 < MA20 | 25% |
| Bollinger | Price at/below lower band | Price at/above upper band | 10% |
| KDJ | K ↑ D < 20 | K ↓ D > 80 | 15% |

**Overall:**
- Score ≥ 60 → **Buy 🟢**
- Score ≤ -60 → **Sell 🔴**
- Otherwise → **Neutral ⚪**

### Support & Resistance

**Support levels (支撑位):**
- Previous lows
- MA20, MA60
- Lower Bollinger Band
- Fibonacci retracement levels (0.382, 0.5, 0.618)

**Resistance levels (压力位):**
- Previous highs
- MA20 (acting as resistance in downtrend)
- Upper Bollinger Band
- Fibonacci retracement levels

## Scripts

### `scripts/indicators.py`
Core technical indicator calculation engine:
- `sma(data, period)` — Simple Moving Average
- `ema(data, period)` — Exponential Moving Average
- `macd(data)` — MACD (DIF, DEA, histogram)
- `rsi(data, period=14)` — RSI
- `bollinger(data, period=20, k=2)` — Bollinger Bands
- `kdj(data)` — KDJ indicator
- `golden_death_cross(short_ma, long_ma)` — Detect 金叉/死叉
- `composite_signal(data)` — Combine all indicators → final signal

## Example Output

```
📉 沪深300 (IF2606) 技术分析

📊 均线系统
  MA5:  3850.2  |  MA10: 3820.5  |  MA20: 3790.8
  ⚡ 金叉确认: MA5 上穿 MA10 ✅

📊 MACD (12,26,9)
  DIF: +8.50  |  DEA: +5.20  |  柱: +6.60
  🟢 MACD金叉，DIF在零轴上方

📊 RSI(14): 62.5
  ⚪ 正常区间，偏强

📊 布林带 (20,2)
  上轨: 3920.0  |  中轨: 3790.8  |  下轨: 3661.6
  价格接近中轨，布林带略微扩张

📊 KDJ(9,3,3)
  K: 68.2  |  D: 62.5  |  J: 79.6
  ⚠️ J值接近80，注意超买风险

━━━━━━━━━━━━━━━━━━━━━
🟢 BUY 信号 (评分: +65/100)
  主要支撑: 3790 (MA20)
  主要压力: 3850 (前高) / 3920 (布林上轨)

💡 建议: 短线偏多，注意J值高位回调风险
  止损参考: 3780 (-0.5%)
```

## Important Notes

- Technical analysis provides **probability-based signals**, not guarantees
- Always combine with fundamentals and market news
- Chinese futures markets have unique characteristics (夜盘, limit up/down rules)
- KDJ is particularly popular among Chinese retail traders; MACD + MA combo is preferred by institutions
- The script `scripts/indicators.py` can be called directly for batch analysis
