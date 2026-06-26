# Indicators Guide

Quick reference for the most effective technical indicators in Freqtrade strategy development.

## RSI (Relative Strength Index)

**Period:** 14 (standard)

**Formula:** RSI = 100 - (100 / (1 + RS)), where RS = avg gain / avg loss

**Interpretation:**
- < 30 = Oversold (potential buy)
- > 70 = Overbought (potential sell)
- 30–70 = Neutral

**Usage:** Entry filter for oversold conditions; exit filter for overbought conditions.

**In Freqtrade:**
```python
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
```

---

## CCI (Commodity Channel Index)

**Period:** 20 (standard)

**Formula:** CCI = (Typical Price - SMA) / (0.015 × Mean Deviation)

**Interpretation:**
- < -100 = Deep oversold; strong momentum reversal signal
- -100 to +100 = Neutral
- > +100 = Deep overbought

**Usage:** Momentum confirmation for entry signals; very selective filter.

**In Freqtrade:**
```python
dataframe['cci'] = ta.CCI(dataframe, timeperiod=20)
```

---

## Bollinger Bands

**Period:** 20; Std Dev: 2.0

**Formula:** 
- Middle Band = SMA(20)
- Upper Band = Middle + (2 × StdDev)
- Lower Band = Middle - (2 × StdDev)

**Interpretation:**
- Price near lower band = Oversold; reversal likely
- Price near upper band = Overbought; pullback likely
- Bands widening = Volatility increasing
- Bands narrowing = Consolidation

**Usage:** Identify overbought/oversold zones; confirm breakouts.

**In Freqtrade:**
```python
dataframe['bb_upperband'], dataframe['bb_middleband'], \
    dataframe['bb_lowerband'] = ta.BBANDS(dataframe, timeperiod=20)
```

---

## EMA (Exponential Moving Average)

**Period:** 9, 21, 50 (customize per timeframe)

**Formula:** EMA = (Close - EMA_prev) × (2 / (n + 1)) + EMA_prev

**Interpretation:**
- Price above EMA = Uptrend
- Price below EMA = Downtrend
- EMA slope shows trend strength

**Usage:** Trend filter; avoid counter-trend entries.

**In Freqtrade:**
```python
dataframe['ema_9'] = ta.EMA(dataframe, timeperiod=9)
dataframe['ema_21'] = ta.EMA(dataframe, timeperiod=21)
```

---

## MACD (Moving Average Convergence Divergence)

**Default:** Fast=12, Slow=26, Signal=9

**Formula:**
- MACD Line = EMA(12) - EMA(26)
- Signal Line = EMA(9) of MACD
- Histogram = MACD - Signal

**Interpretation:**
- MACD > Signal & both > 0 = Strong uptrend
- MACD < Signal & both < 0 = Strong downtrend
- Crossovers = Trend changes

**Usage:** Trend confirmation; identify momentum shifts.

**In Freqtrade:**
```python
macd, signal, hist = ta.MACD(dataframe)
dataframe['macd'] = macd
dataframe['macd_signal'] = signal
```

---

## MFI (Money Flow Index)

**Period:** 14

**Formula:** MFI = 100 - (100 / (1 + Money Flow Ratio))

**Interpretation:**
- < 20 = Oversold with volume; strong buy setup
- > 80 = Overbought with volume; strong sell setup

**Usage:** Confirm entry signals with volume weight; avoid low-volume trades.

**In Freqtrade:**
```python
dataframe['mfi'] = ta.MFI(dataframe, timeperiod=14)
```

---

## Volume SMA (Volume Simple Moving Average)

**Period:** 20 (standard)

**Usage:** Filter entries by volume confirmation; ignore trades on low volume.

**In Freqtrade:**
```python
dataframe['volume_sma'] = ta.SMA(dataframe['volume'], timeperiod=20)
# Entry only if: dataframe['volume'] > dataframe['volume_sma']
```

---

## Pro Tips

1. **Avoid indicator overload** — 3–5 indicators per strategy is optimal; too many = conflicts
2. **Match timeframe to purpose** — Fast timeframes (5m) need faster indicators; slow timeframes (1h) can use longer periods
3. **Combine momentum + trend** — Use MACD or CCI for momentum, EMA for trend, volume for confirmation
4. **Backtest indicator periods** — The standard periods are a starting point; optimize for your data
5. **Check latest Freqtrade docs** — For accurate TA-Lib wrapper syntax
