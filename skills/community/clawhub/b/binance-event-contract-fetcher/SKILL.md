# Binance Event Contract Full Data Fetcher

## 1. Scenario Definition
- **Trigger Timing**: Auto-run every minute after Agent startup; also supports manual trigger via `/binance-fetch-data`; runs 24/7, aligned with Binance 7×24 trading hours
- **Core Intent**: Provide 100% accurate, delay-free Binance official native data for the 3-tier resonance strategy; reject all third-party data sources
- **Context**: Targets only BTCUSDT & ETHUSDT pairs; covers only 10min/30min/60min Event Contract cycles; provides underlying data support for signal calculation, ICT recognition, and risk control

## 2. Goal Setting
Complete Binance official API data fetch within 1 second per minute; output standardized BTC/ETH full-dimension data with 100% accuracy; price data fully matches Binance Event Contract settlement spot index price; provide error-free data source for strategy signal calculation.

## 3. Execution Rules

### 3.1 Data Source Rule
- **MUST** connect ONLY to Binance Official REST API & WebSocket API
- **MUST** call `https://api.binance.com` (or appropriate endpoint)
- **PROHIBITED**: Calling any third-party data platform (Huobi, OKX, etc.)

### 3.2 Fixed Fetch Pairs
- BTCUSDT (primary)
- ETHUSDT (secondary)

### 3.3 Mandatory Fetch Data Dimensions

**K-line Data:**
- Cycles: 1min / 10min / 30min / 1h / 4h
- Fields: open, high, low, close, volume, turnover
- Fetch latest 200 K-lines per cycle for indicator calculation

**Liquidity Data:**
- BTC/ETH spot order book top 10 bid/ask depth
- Calculate total bid/ask amount
- Verify if total bid or ask ≥ 500,000 USDT

**Market Data:**
- Latest spot index price (Binance Event Contract settlement anchor)
- 24h price change
- Bid-ask spread

**Contract Rule Data:**
- Current available expiration cycles (10min/30min/1h)
- Single trade limit (5-250 USDT)
- Daily loss limit rules

### 3.4 Running Rule
- Auto-start cron task at Agent startup
- Run at second 0 of every minute
- Auto-cache data after fetch
- Sync to all related Skills for call

### 3.5 Data Verification Rule
- Auto-verify data integrity after each fetch
- Auto-retry 3 times if interface timeout or data missing
- Trigger exception alert if retry failed
- Use previous valid cached data as fallback
- No impact on strategy running if cache available

## 4. Example Output

### ✅ Positive Example (Standard Output)
```
【 Binance Event Contract Data Fetch Completed | 2026-03-18 12:10:00 】
1. Pair: BTCUSDT
   - Latest Index Price: 68245.32 USDT
   - 10min K-line: Open 68198.45 / High 68289.12 / Low 68176.33 / Close 68245.32 / Volume 128.34 BTC
   - Liquidity: Bid Depth 892,000 USDT | Ask Depth 945,000 USDT | Qualified ✓
   - Available Cycles: 10min / 30min / 1h Event Contract — ALL AVAILABLE
2. Pair: ETHUSDT
   - Latest Index Price: 3842.18 USDT
   - 10min K-line: Open 3839.76 / High 3845.22 / Low 3838.11 / Close 3842.18 / Volume 986.25 ETH
   - Liquidity: Bid Depth 627,000 USDT | Ask Depth 583,000 USDT | Qualified ✓
   - Available Cycles: 10min / 30min / 1h Event Contract — ALL AVAILABLE
Data synced to signal calculation module | Cache valid for 60s
```

### ❌ Negative Example (Forbidden Output)
- Fetch BTC/ETH data from exchanges other than Binance (Huobi/OKX etc.)
- Only output price without volume, liquidity, or other strategy-required data
- Use expired K-line data with delay over 1 minute

## 5. Boundary Definition

### Forbidden Operations
1. Do NOT call Binance trading API for entry/settlement — only data fetch and verification
2. Do NOT fetch data of pairs other than BTC/ETH
3. Do NOT store user account privacy data

### Exception Handling
1. When Binance API is under maintenance or rate limit → push alert immediately, stop invalid fetch, auto-restart after API recovery
2. Do NOT output invalid data to signal calculation module if data verification failed

### Fallback Strategy
If fetch fails 3 times consecutively → push "Data Fetch Exception" alert immediately, pause signal generation until data returns to normal, avoid false signal caused by wrong data

## Installation
```bash
npx clawhub@latest install binance-event-contract-data-fetcher --dir /workspace/skills
```

## Auto-Run Trigger
24/7, run every minute automatically after activation
