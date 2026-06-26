# Technical Indicators Reference

> Knowledge base for signal interpretation. Agent policy (`AGENTS.md`) references this document for analysis.

---

## 1. Trend Indicators

### MA (Moving Average)

**Purpose**: Smooth price fluctuations, reveal trend direction.

**Formula**: `MA(N) = (C1 + C2 + ... + CN) / N`

| Period | Meaning | Application |
|--------|---------|-------------|
| MA5 | Weekly average (ultra-short) | Immediate trend, frequent crossovers |
| MA10 | 2-week average (short) | Short-term support/resistance |
| MA20 | Monthly average (medium-short) | Swing trading core reference |
| MA50 | 2-month average (medium) | Medium-term trend boundary |
| MA200 | Long-term average | Bull/Bear divider, institutional focus |

**Signals**:
| Pattern | Signal | Meaning |
|---------|--------|---------|
| Golden Cross (short MA crosses above long MA) | Buy | Short-term momentum > long-term |
| Death Cross (short MA crosses below long MA) | Sell | Short-term momentum < long-term |
| Bullish Alignment (MA5 > MA10 > MA20 > MA50) | Strong Uptrend | All timeframes agree |
| Bearish Alignment (MA5 < MA10 < MA20 < MA50) | Strong Downtrend | All timeframes agree |
| MA Convergence | Pending Breakout | Wait for direction confirmation |

---

### EMA (Exponential Moving Average)

**Purpose**: More weight on recent prices, faster response than MA.

**Formula**: `EMA(t) = α × Price(t) + (1-α) × EMA(t-1)`, where `α = 2/(N+1)`

**Key Periods**:
- **EMA12**: Short-term momentum, MACD fast line basis
- **EMA26**: Medium-term momentum, MACD slow line basis

**vs MA**: EMA reacts faster to sudden moves, better for volatile crypto markets.

---

### DMI (Directional Movement Index)

**Purpose**: Measure trend strength AND direction.

**Components**:
- **+DI**: Upward momentum strength
- **-DI**: Downward momentum strength
- **ADX**: Trend strength (direction-agnostic)

**Parameter**: Period = 14

**ADX Interpretation**:
| ADX Value | Market State | Trading Strategy |
|-----------|--------------|------------------|
| < 20 | No trend / Ranging | Range trade, avoid trend strategies |
| 20-25 | Trend forming | Prepare entry, await confirmation |
| 25-40 | Trend confirmed | Trade with trend, hold position |
| 40-50 | Strong trend | Add to position, watch for extremes |
| > 50 | Extreme trend | Prepare exit, reversal possible |

**Direction**: `+DI > -DI && ADX > 25` = Long | `-DI > +DI && ADX > 25` = Short

---

## 2. Momentum Indicators

### RSI (Relative Strength Index) ★ Core Indicator

**Purpose**: Measure overbought/oversold conditions and momentum.

**Formula**: `RSI = 100 - (100 / (1 + RS))`, where `RS = Avg Gain / Avg Loss`

**Parameter**: Period = 14

**Zone Analysis**:
| RSI Range | State | Action |
|-----------|-------|--------|
| > 80 | Extreme Overbought | Strong short signal, high reversal probability |
| 70-80 | Overbought | Watch for short, await confirmation |
| 50-70 | Bullish Zone | Uptrend, hold longs |
| 30-50 | Bearish Zone | Downtrend, hold shorts |
| 20-30 | Oversold | Watch for long, await confirmation |
| < 20 | Extreme Oversold | Strong long signal, high bounce probability |

**Divergence (Most Important Reversal Signal)**:
| Type | Pattern | Meaning |
|------|---------|---------|
| Bearish Divergence | Price new high, RSI no new high | Upward momentum exhausted, prepare short |
| Bullish Divergence | Price new low, RSI no new low | Downward momentum exhausted, prepare long |
| Hidden Divergence | Price pullback but RSI holds | Trend continuation signal |

**Trend Context**:
- **Uptrend**: RSI 40-50 = support zone (add to longs)
- **Downtrend**: RSI 50-60 = resistance zone (add to shorts)

---

### MACD (Moving Average Convergence Divergence)

**Purpose**: Track momentum changes via EMA differential.

**Formula**:
```
DIF (Fast Line) = EMA12 - EMA26
DEA (Signal Line) = 9-period EMA of DIF
Histogram = (DIF - DEA) × 2
```

**Signal Categories**:

**1. Crossovers**:
| Pattern | Location | Meaning |
|---------|----------|---------|
| Golden Cross (DIF above DEA) | Above zero | Strong trend continuation |
| Golden Cross (DIF above DEA) | Below zero | Possible reversal start |
| Death Cross (DIF below DEA) | Below zero | Weak trend continuation |
| Death Cross (DIF below DEA) | Above zero | Possible pullback start |

**2. Zero Line**:
- DIF/DEA above zero = Bull market, prioritize longs
- DIF/DEA below zero = Bear market, prioritize shorts
- Zero line cross = Major trend transition

**3. Histogram**:
| Pattern | Meaning |
|---------|---------|
| Red bars expanding | Bullish momentum increasing |
| Red bars shrinking | Bullish momentum weakening, watch for reversal |
| Green bars expanding | Bearish momentum increasing |
| Green bars shrinking | Bearish momentum weakening, watch for bounce |

---

### KDJ (Stochastic Oscillator)

**Purpose**: Measure price position relative to range, fast overbought/oversold detection.

**Formula**:
```
RSV = (Close - N-day Low) / (N-day High - N-day Low) × 100
K = 2/3 × Previous K + 1/3 × RSV
D = 2/3 × Previous D + 1/3 × K
J = 3K - 2D
```

**Parameters**: N=9, M1=3, M2=3

**Signals**:
| Condition | State | Action |
|-----------|-------|--------|
| K, D > 80 | Overbought | Watch for short, J > 100 = extreme |
| K, D < 20 | Oversold | Watch for long, J < 0 = extreme |
| K crosses above D | Golden Cross | Buy signal (more valid at low levels) |
| K crosses below D | Death Cross | Sell signal (more valid at high levels) |

**J-line Extremes**: J > 100 or J < 0 = Short-term extreme, high reversal probability.

---

## 3. Volatility Indicators

### Bollinger Bands

**Purpose**: Dynamic support/resistance based on standard deviation.

**Formula**:
```
Middle = MA(20)
Upper = MA(20) + 2 × StdDev
Lower = MA(20) - 2 × StdDev
%B = (Price - Lower) / (Upper - Lower)
```

**Price Position**:
| Position | State | Action |
|----------|-------|--------|
| Touch upper band | Overbought | Watch for pullback |
| Touch lower band | Oversold | Watch for bounce |
| Walking upper band | Strong uptrend | Don't rush to short |
| Walking lower band | Strong downtrend | Don't rush to long |

**Bandwidth**:
| Pattern | Meaning | Action |
|---------|---------|--------|
| Squeeze (narrow bands) | Low volatility, pending breakout | Wait for direction |
| Expansion (wide bands) | Trend started | Trade with trend |

**%B Values**:
- %B > 1 = Price above upper band, extreme overbought
- %B < 0 = Price below lower band, extreme oversold
- %B = 0.5 = Price at middle band

---

### ATR (Average True Range)

**Purpose**: Measure volatility for stop-loss/take-profit distance.

**Formula**:
```
TR = Max(High-Low, |High-PrevClose|, |Low-PrevClose|)
ATR = 14-period MA of TR
```

**Applications**:
| Use Case | Formula | Notes |
|----------|---------|-------|
| Stop Loss | Entry ± 1.5-2 × ATR | Avoid normal volatility stop-outs |
| Take Profit | Entry ± 2-3 × ATR | Reasonable risk/reward |
| Position Size | Risk Amount / ATR | Reduce size when volatility high |

**Volatility Assessment**:
- ATR% = ATR / Price × 100
- ATR% < 3% = Low volatility, can increase leverage
- ATR% > 5% = High volatility, reduce leverage and size

---

## 4. Volume Indicators

### OBV (On-Balance Volume)

**Purpose**: Track money flow via cumulative volume weighted by price direction.

**Rules**:
- Close > Previous Close: OBV += Today's Volume
- Close < Previous Close: OBV -= Today's Volume
- Close = Previous Close: OBV unchanged

**Signals**:
| Pattern | Meaning |
|---------|---------|
| Price up + OBV up | Healthy uptrend, sustainable |
| Price up + OBV down (divergence) | Weak uptrend, reversal warning |
| Price down + OBV down | Normal pullback, not panic |
| Price down + OBV up (divergence) | Possible bottom accumulation |

---

## 5. Price Structure Indicators

### Fibonacci Retracement

**Purpose**: Identify potential support/resistance based on Fibonacci ratios.

**Key Levels**:
| Ratio | Meaning | Significance |
|-------|---------|--------------|
| 0.236 | Shallow retracement | Strong trends often stop here |
| 0.382 | Golden retracement | Common support/resistance ★ |
| 0.500 | Mid retracement | Psychological level |
| 0.618 | Deep retracement | Most important level ★★★ |
| 0.786 | Extreme retracement | Trend may be invalidated |

**Extension Levels (for take-profit)**:
- 1.272: First target
- 1.618: Second target (golden extension)
- 2.618: Extreme target

**Application Rules**:
1. Uptrend pullback to 0.382-0.618 zone = High probability long entry
2. Downtrend bounce to 0.382-0.618 zone = High probability short entry
3. Retracement beyond 0.786 = Original trend likely ended

---

### Support/Resistance

**Pivot Points Calculation**:
```
P (Pivot) = (High + Low + Close) / 3
R1 = 2P - Low     S1 = 2P - High
R2 = P + (High - Low)    S2 = P - (High - Low)
R3 = High + 2(P - Low)   S3 = Low - 2(High - P)
```

**Swing High/Low Identification**:
- Swing High: Highest point with 3-5 lower bars on each side
- Swing Low: Lowest point with 3-5 higher bars on each side
- Multiple tests without break = Strong level

---

## 6. Derivatives Data Interpretation

### Funding Rate

| Pattern | Meaning | Implication |
|---------|---------|-------------|
| Consistently positive | More longs than shorts | Market bullish, but crowded long |
| Consistently negative | More shorts than longs | Market bearish, but crowded short |
| Extreme positive (> 0.1%) | Over-leveraged longs | High probability of long squeeze |
| Extreme negative (< -0.1%) | Over-leveraged shorts | High probability of short squeeze |

### Open Interest

| Pattern | Meaning | Implication |
|---------|---------|-------------|
| OI rising + Price rising | New longs entering | Uptrend confirmed |
| OI rising + Price falling | New shorts entering | Downtrend confirmed |
| OI falling + Price rising | Shorts covering | Uptrend may be weak |
| OI falling + Price falling | Longs liquidating | Downtrend may be weak |

### Liquidation Data

| Pattern | Meaning | Implication |
|---------|---------|-------------|
| Heavy long liquidations (side='sell') | Market crashed longs | Possible bottom forming |
| Heavy short liquidations (side='buy') | Market squeezed shorts | Possible top forming |
| Dense liquidations | Extreme move | Trend may reverse or accelerate |
| Sparse liquidations | Normal volatility | Trend likely continues |
