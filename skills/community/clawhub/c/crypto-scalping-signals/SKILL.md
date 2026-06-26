# Crypto Scalping Signals

AI-powered crypto futures scalping with 10+ battle-researched strategies.

## What This Skill Does

Gives your agent real-time crypto scalping capabilities:
- **Signal generation** using 10+ proven strategies
- **Risk management** with position sizing, daily loss limits, leverage control
- **Market structure analysis** — break of structure, liquidity sweeps, kill zones
- **Order flow insights** — CVD delta divergence, volume profile, absorption
- **Exchange optimization** — MEXC, Binance, low-fee futures

## Strategies Included

1. **Liquidity Sweep Reversal** — Wait for stop hunts at equal highs/lows, enter the reversal (65-70% WR)
2. **Break of Structure Continuation** — Filter real BoS from fake with body/volume analysis
3. **VWAP Pullback** — Enter on VWAP retest with RSI/BB confirmation
4. **Bollinger Bands + RSI** — Mean reversion at BB extremes with RSI divergence
5. **Double RSI (7/21)** — Momentum filter, 64.7% WR on M5
6. **Stochastic RSI (5,3,3)** — MEXC zero-fee optimized, 65-70% WR
7. **ATR Squeeze Breakout** — TTM Squeeze detection for volatility expansion
8. **Order Flow Delta Divergence** — CVD exhaustion at key levels (62-65% WR)
9. **Kill Zone Scalping** — Session-based entries during London/NY windows
10. **1MS Method** — Market Structure → Momentum → Sentiment triple filter

## Commands

When you need a trading signal or analysis, use these prompts:

- `scan for setups` — Check current market for any strategy matches
- `analyze [SYMBOL]` — Deep analysis of a specific pair (e.g., `analyze SOL/USDT`)
- `liquidity sweep check` — Find equal highs/lows on watched pairs
- `kill zone status` — Check if we're in a high-volume trading window
- `risk calculator [amount] [leverage]` — Calculate position size and risk

## Configuration

Set these in your agent's TOOLS.md or environment:

```
### Trading Setup
- Exchange: MEXC (or other low-fee futures)
- Pairs: BTC, ETH, SOL, AVAX, SUI, NEAR, FET, RENDER, WIF, PEPE, LINK, UNI, AAVE, DOGE, XRP, ADA
- Format: BTC/USDT:USDT
- Leverage: 2-3x (start conservative)
- Risk: 1-2% per trade, 4% daily max
- Timeframe: 1m primary, 5m confirmation
- Scan interval: 30 seconds
```

## Risk Management Rules

This skill enforces strict risk management:
- **Max risk per trade:** 2% of account
- **Daily loss limit:** 4% of account (hard stop)
- **Leverage cap:** 3x until proven profitable
- **Max concurrent trades:** 3
- **Commission awareness:** Account for 0.08% round-trip minimum
- **Skip rule:** If fee > 50% of expected profit, skip the trade
- **Kill zone filter:** Only trade during London (07-09 UTC) or NY (13-15 UTC) windows

## Data Sources

- Real-time prices: Exchange WebSocket APIs
- Indicators: ccxt library (EMA, RSI, BB, VWAP, ATR, Stochastic RSI)
- Sentiment: Fear & Greed Index, funding rates, long/short ratios
- Volume: Deal flow, CVD delta, volume profile

## Strategy Details

### Liquidity Sweep Reversal (Primary Strategy)
1. Mark equal highs/lows (within 0.1% tolerance) — these are liquidity magnets
2. Wait for price to sweep beyond with a wick
3. Confirm rejection: candle closes back beyond the level
4. Enter on retest with RSI extreme confirmation
5. SL beyond wick extreme, TP at next structure level

### Kill Zone Timing
- London Kill Zone: 07:00-09:00 UTC
- NY Kill Zone: 13:00-15:00 UTC
- London Close: 15:00-17:00 UTC
- Funding rate settlements: 08:00, 16:00, 24:00 UTC (create predictable sweeps)
- **Skip trading outside kill zones** — range/chop destroys scalping edges

### 1MS Method (Universal Filter)
Three-layer confirmation before any entry:
1. **Market Structure** — HH/HL (long) or LH/LL (short), skip if messy
2. **Momentum** — EMA 9/21/50 stacked, volume present
3. **Sentiment** — Funding rate not extreme, L/S ratio balanced, RSI not exhausted

## Important Notes

- This skill provides **analysis and signals**, not automatic execution
- Always validate signals against your own risk tolerance
- Past performance doesn't guarantee future results
- Start paper trading before using real funds
- Commission and slippage erode scalping profits — always account for them

## References

Research backed by:
- 1minscalper.com 1MS Method framework
- ICT/SMC liquidity sweep methodology
- Order flow delta divergence research (Kalena, AlgoStorm)
- Volume profile techniques (POC, VA, LVN)
- MEXC-specific zero-fee optimization