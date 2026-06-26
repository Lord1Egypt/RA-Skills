---
name: Crypto Market Analyst
version: 1.0.2
description: "Analyze Bitcoin, Ethereum, and major altcoins using real-time price, on-chain signals, and macro context from the Finskills API."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/crypto-market-analyst
---

# Crypto Market Analyst

Analyze the cryptocurrency market using real-time and historical price data from
the Finskills API free-tier crypto endpoints. Covers Bitcoin, Ethereum, and major
altcoins with market cap, dominance, volatility, and crypto-specific cycle analysis
(halving cycles, fear/greed dynamics, altcoin seasons). Synthesizes a structured
market regime classification and actionable positioning guidance.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks about Bitcoin, Ethereum, or altcoin prices
- Wants to understand current crypto market conditions
- Asks "is crypto in a bull or bear market?"
- Wants a market cap or dominance analysis
- Asks about crypto-specific concepts: halvings, altcoin season, Bitcoin dominance
- Asks to compare multiple crypto assets
- Wants to know the risk/opportunity in the crypto market right now

---

## Data Retrieval — Finskills API Calls

### 1. Market Overview (Top Coins by Market Cap)
```
GET https://finskills.net/v1/free/crypto/markets
```
Extract (for top 20+ coins):
- `id`: coin identifier (bitcoin, ethereum, solana, etc.)
- `name`, `symbol`
- `current_price`
- `market_cap`
- `market_cap_rank`
- `price_change_percentage_24h`
- `price_change_percentage_7d`
- `total_volume` (24h)
- `circulating_supply`
- `high_24h`, `low_24h`
- `ath` (all-time high), `ath_change_percentage` (% from ATH)

### 2. Single Coin Price + Details
For any specific coin the user asks about:
```
GET https://finskills.net/v1/free/crypto/price/{coinId}
```
Examples: `bitcoin`, `ethereum`, `solana`, `cardano`, `avalanche-2`, `chainlink`  
Extract: current price, market cap, volume, price change (24h, 7d, 30d)

### 3. Historical Price Data (Trend Analysis)
For BTC and ETH (primary assets), and any requested altcoin:
```
GET https://finskills.net/v1/free/crypto/history/{coinId}
```
Extract: date series, price series  
Compute: 7-day/30-day/90-day returns, drawdown from ATH, 30-day rolling volatility

---

## Analysis Workflow

### Step 1 — Market Cap & Dominance Analysis

From the markets data, compute:

**Total Crypto Market Cap:**
```
Total_MCap = sum(market_cap for all coins in response)
```

**Bitcoin Dominance:**
```
BTC_Dominance = BTC_market_cap / Total_market_cap × 100
```

**Ethereum Dominance:**
```
ETH_Dominance = ETH_market_cap / Total_market_cap × 100

Altcoin Dominance = 100 - BTC_Dominance - ETH_Dominance
```

**Dominance Signal:**

| BTC Dominance | Signal |
|--------------|--------|
| > 55% | Risk-off; Bitcoin outperforming; early bull or bear market |
| 45–55% | Balanced; mainstream phase; ETH/large caps performing |
| < 45% | Altcoin season; speculation elevated; late-cycle risk |

### Step 2 — Bitcoin Cycle Analysis

**Key Bitcoin Halving Cycle Facts:**
- Halving events approximately every 4 years (~210,000 blocks)
- Last halving: April 2024
- Historical pattern: Strongest appreciation typically 12–18 months post-halving
- Cycle phases: Accumulation → Early Bull → Full Bull → Peak → Distribution → Bear → Capitulation → Recovery

**Current Cycle Position:**
Based on time since last halving (April 19, 2024), estimate cycle phase:
- 0–6 months post-halving: Accumulation / Early Bull
- 6–18 months post-halving: Bull market expansion
- 18–30 months post-halving: Late bull, increasing volatility
- 30–48 months post-halving: Distribution / Bear market

**ATH Distance:**
```
BTC_ATH_Distance = (BTC_current_price / BTC_ath) - 1 (as %)
```
- Within 20% of ATH: Price discovery zone / near peak
- 20–60% below ATH: Bull market territory
- > 60% below ATH: Capitulation / deep bear

### Step 3 — Volatility & Risk Assessment

**30-Day Rolling Volatility (Annualized):**
From historical price data:
```
daily_returns = price.pct_change()
vol_30d_annualized = daily_returns.rolling(30).std() × sqrt(365) × 100
```

Crypto Volatility Regimes:
- < 40% annualized vol: Low volatility — consolidation or gradual bull
- 40–80%: Normal crypto volatility
- > 80%: High volatility — extreme moves likely in both directions
- > 120%: Crisis / capitulation volatility

**Drawdown from ATH:**
```
Max drawdown from ATH = (current_price - ath) / ath × 100
```

**Sharp Decline Detector (last 7 days):**
- If 7-day return < -20%: Cascade selloff / forced liquidation — potential bounce setup
- If 7-day return > +30%: Parabolic move — profit-taking warning

### Step 4 — Altcoin Season Index

Estimate altcoin season based on dominance ratios and altcoin vs. BTC performance:

**Altcoin Season Signal:**
- If > 75% of top 50 altcoins outperformed BTC in last 30 days: **Altcoin Season** 🔥
- If 25–75% outperformed: **Ambiguous / Mixed** market
- If < 25% outperformed BTC: **Bitcoin Season** — capital concentrated in BTC

From the markets data, compute how many of the top 20 coins beat BTC's 7-day return:
```
beating_btc = count(coin for coin in top_20 if coin.7d_return > BTC.7d_return)
ratio = beating_btc / 20
```
- > 0.75: Altcoin season
- 0.25–0.75: Mixed
- < 0.25: Bitcoin season

### Step 5 — Layer-1 Competition Analysis

For major L1 blockchains (ETH, SOL, ADA, AVAX), compute relative performance vs. BTC:
```
Relative_Return = coin_7d_return - BTC_7d_return
```
Identify which L1s are gaining / losing market share.

### Step 6 — Macro Correlation Assessment

Crypto increasingly correlates with risk assets (Nasdaq) during certain regimes:
- If broad equity market is in risk-off (use `/v1/market/summary` if available): Crypto headwind
- If monetary policy is tightening (high real rates): Suppresses speculative assets including crypto
- BTC as "digital gold" narrative: Check if gold is also rallying (use `/v1/free/commodity/price/gold`)

Note the correlation context without making definitive claims.

### Step 7 — Sentiment Proxy

Use market data as a sentiment proxy (actual Fear & Greed Index data unavailable):

**Sentiment Estimation from Data:**
- **Extreme Greed**: BTC within 10% of ATH + altcoins > BTC + high volume
- **Greed**: BTC 10–25% from ATH + broad crypto market rising
- **Neutral**: Mixed performance + normal volume
- **Fear**: BTC 25–50% from ATH + altcoins underperforming + declining volume
- **Extreme Fear**: BTC > 50% from ATH + most altcoins at deep losses + low volume / capitulation

---

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║    CRYPTO MARKET REPORT  —  {DATE}                          ║
╚══════════════════════════════════════════════════════════════╝

📊 MARKET OVERVIEW
  Total Crypto Market Cap: ${X}T / ${X}B
  24H Volume:             ${X}B

  BTC Dominance:  {X.X}%   [{Signal: Risk-Off / Balanced / Altcoin Season}]
  ETH Dominance:  {X.X}%
  Altcoin Dom.:   {X.X}%
  Season:  →  {BITCOIN SEASON / MIXED / ALTCOIN SEASON 🔥}

₿ BITCOIN
  Price:            ${price}   24H: {+/-X}%   7D: {+/-X}%   30D: {+/-X}%
  Market Cap:       ${X}B
  ATH:              ${ath} (${ath_distance}% from ATH)
  30D Volatility:   {X}% annualized
  
  Cycle Status:     {N} months since April 2024 halving
                    Phase: {ACCUMULATION / EARLY BULL / BULL EXPANSION / LATE BULL / BEAR}
  
  BTC Regime:  →  {ACCUMULATION / BULL MARKET / RISK ZONE / BEAR MARKET}

Ξ ETHEREUM  
  Price:            ${price}   24H: {+/-X}%   7D: {+/-X}%
  Market Cap:       ${X}B  
  ETH/BTC Ratio:    {ratio}  [{ETH strong vs BTC / ETH lagging BTC}]
  ATH Distance:     {-X}%

🌐 TOP ALTCOINS  (vs. BTC 7D: {BTC_7d}%)

  Rank  Name       Symbol  Price       7D        vs. BTC   MCap
  ──── ────────── ──────  ──────────  ───────   ───────   ─────────
   3   Solana      SOL   ${price}    {+/-X}%   {+/-X}%   ${B}B
   4   XRP         XRP   ${price}    {+/-X}%   {+/-X}%   ${B}B
   5   BNB         BNB   ${price}    {+/-X}%   {+/-X}%   ${B}B
   6   Avalanche   AVAX  ${price}    {+/-X}%   {+/-X}%   ${B}B
   7   Cardano     ADA   ${price}    {+/-X}%   {+/-X}%   ${B}B
   ...

  Top Performers (7D, vs BTC):  {list top 3 outperformers}
  Laggards (7D, vs BTC):        {list top 3 underperformers}
  Altcoins beating BTC (7D):    {N}/20 = {%} → {Altcoin Season / Mixed / BTC Season}

📉 RISK ASSESSMENT
  Market-Wide Drawdown from ATH: {X}%
  Estimated Sentiment:    {EXTREME GREED / GREED / NEUTRAL / FEAR / EXTREME FEAR}
  Key Risk:               {Specific concern if elevated}

💡 POSITIONING SIGNALS
  BTC View:    {BULLISH — accumulate / NEUTRAL — hold / BEARISH — reduce}
  ETH vs. BTC: {ETH gaining / losing relative strength → flip / hold allocation}
  Altcoin Exposure: {Max exposure now / Reduce to BTC+ETH only}
  
  Rationale: {2-sentence synthesis of the above data points}

📌 MACRO CONTEXT
  {Note any relevant macro factors: Fed policy, equity correlation, dollar strength, gold comparison}

🔍 KEY LEVEL TO WATCH
  {The most important price level or ratio to monitor for a regime shift signal}
```

---

## Limitations

- Crypto markets trade 24/7; data may be minutes old but not real-time tick data.
- Regulatory risks (SEC actions, country bans) are not captured in price data alone.
- Halving cycle analysis is based on historical patterns — the 4th+ cycles may behave differently.
- DeFi-specific metrics (TVL, protocol revenue, DEX volume) are outside this skill's scope.
- Crypto is a highly speculative asset class; treat all analysis as research, not investment advice.
