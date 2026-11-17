# Technical Indicator Calculation Formulas

## Moving Averages (MA)
- MA5 = (Close_t + Close_t-1 + Close_t-2 + Close_t-3 + Close_t-4) / 5
- MA10 = Sum of last 10 closing prices / 10
- MA20 = Sum of last 20 closing prices / 20

## Relative Strength Index (RSI) - Wilder's Smoothing
1. Calculate changes: Δ = Close_t - Close_t-1
2. Separate gains and losses:
   - Gain = Δ if Δ > 0 else 0
   - Loss = -Δ if Δ < 0 else 0
3. Calculate average gain and loss over period (typically 14):
   - Average Gain = (Previous Average Gain × 13 + Current Gain) / 14
   - Average Loss = (Previous Average Loss × 13 + Current Loss) / 14
4. RS = Average Gain / Average Loss
5. RSI = 100 - (100 / (1 + RS))

## Moving Average Convergence Divergence (MACD)
- EMA12 = Exponential Moving Average of Close with period 12
- EMA26 = Exponential Moving Average of Close with period 26
- DIF = EMA12 - EMA26
- DEA = EMA9 of DIF (Exponential Moving Average of DIF with period 9)
- MACD Histogram = DIF - DEA

*Note: Some platforms (like Chinese trading software) multiply MACD values by 2 for display. Always verify the calculation convention being used.*

## Bollinger Bands
- Middle Band = MA20 (20-period Simple Moving Average)
- Standard Deviation = sqrt( Σ(Close_i - MA20)^2 / 20 ) for i from t-19 to t
- Upper Band = Middle Band + (2 × Standard Deviation)
- Lower Band = Middle Band - (2 × Standard Deviation)

## Volume Indicators (Optional)
- Volume Ratio = Current Volume / 5-day Average Volume
- Price-Volume Trend (PVT) = Previous PVT + Volume × ((Close_t - Close_t-1) / Close_t-1)

## Calculation Notes
1. Always use 前复权 (forward-adjusted) prices to account for dividends and splits.
2. Ensure sufficient warm-up period: calculate indicators starting from at least 50-100 days before the analysis period to stabilize EMA calculations.
3. For weekly aggregates: use Friday's close as week close, Monday's open as week open (adjust for holidays).
4. Volume is typically reported in 万手 (10,000 shares) in Chinese markets; convert to shares by multiplying by 10,000 when needed.