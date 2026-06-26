# Crypto Analysis Framework

When analyzing any cryptocurrency (BTC, ETH, TON, LINK, SOL, etc.), follow this structured framework. Each dimension must be checked and reported.

## Framework Dimensions

### 1. Volume Analysis (量能)

- Fetch current 24h volume
- Compare against 7-day volume MA (compute from daily candles)
- Report: volume ratio = current / 7D_MA
- Signal: ratio > 1.2 → bullish (放量), ratio < 0.7 → bearish (缩量), 0.7-1.2 → neutral

### 2. Multi-Timeframe Divergence Detection (多周期背离)

**Check these timeframes**: 15m, 4H, 1D

For each timeframe, compare:
- Price trend direction (higher highs / lower lows)
- RSI trend direction
- MACD histogram direction

**Top Divergence (顶背离)** = Price makes higher high, but RSI/MACD makes lower high → bearish
**Bottom Divergence (底背离)** = Price makes lower low, but RSI/MACD makes higher low → bullish

Report conflicts: e.g., "4H多头趋势 vs 日线顶背离 → 短期方向不明"

### 3. Key Level Analysis (关键位置)

- **Resistance levels**: 24h high, recent swing high, BB upper band, EMA7/EMA25
- **Support levels**: 24h low, recent swing low, BB middle band, EMA25/EMA99
- Report: nearest support and resistance with prices

### 4. Volatility Assessment (波动率)

- Compute 24h volatility: (high - low) / open * 100
- Compare to 7-day average volatility
- Signal: rising volatility → breakout likely, declining → consolidation

### 5. Derivatives Market (合约市场)

- Funding rate: negative → bearish sentiment, positive → bullish
- Open Interest: rising + price up = bullish, rising + price down = bearish
- Report OI in USD

### 6. News & Fundamentals (消息面)

- Check market-intel news feed for relevant catalysts
- Note any ecosystem updates, regulatory news, or macro events

### 7. Consolidation Signal (浓缩信号)

Synthesize into 3-5 actionable focus points:
- Bullish signals summary
- Bearish signals summary
- Key level to watch for breakout/breakdown
- Volume confirmation needed
- Short-term directional bias (1-3 day outlook)

## Data Sources

Use `okx market` CLI for all price/indicator data:
- Ticker: `okx market ticker <INST>-USDT`
- Multi-TF candles: `okx market candles <INST>-USDT --bar 15m/4H/1D`
- RSI: `okx market indicator rsi <INST>-USDT --bar 15m/4Hutc/1Dutc`
- MACD: `okx market indicator macd <INST>-USDT --bar 15m/4Hutc/1Dutc`
- EMA: `okx market indicator ema <INST>-USDT --bar 1Dutc --params 7,25,99`
- BB: `okx market indicator bb <INST>-USDT --bar 1Dutc`
- Funding rate: `okx market funding-rate <INST>-USDT-SWAP`
- OI: `okx market open-interest --instType SWAP --instId <INST>-USDT-SWAP`

Fear & Greed: `curl -s https://api.alternative.me/fng/?limit=1`

## Output Format

Use ASCII-only for WeChat compatibility. Block structure:
```
<COIN> 走势分析 | <DATE> <TIME> (UTC+8)
━━━━━━━━━━━━━━━━━━
📊 即时行情
📈 技术指标 (多周期)
📅 近7日走势
🔻 合约市场
😱 恐慌贪婪指数 (BTC only or market-wide)
🧭 综合研判 + 后续关注重点
```