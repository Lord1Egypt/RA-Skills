---
name: Commodity Macro Signal
version: 1.0.2
description: "Analyze energy, metals, and agricultural commodity markets alongside macro indicators to generate cross-asset macro signals."
author: finskills
metadata:
  openclaw:
    requires:
      env:
        - FINSKILLS_API_KEY
    primaryEnv: FINSKILLS_API_KEY
  homepage: https://github.com/finskills/commodity-macro-signal
---

# Commodity Macro Signal

Analyze global commodity markets to extract macro signals for inflation, growth,
and supply chain dynamics using free-tier Finskills API data. Covers energy
(crude oil, natural gas), precious metals (gold, silver), industrial metals
(copper), agricultural products, and FRED/IMF commodity indices — then synthesizes
investment implications across asset classes.

---

## Setup

**API Key required** — [Register at https://finskills.net](https://finskills.net) to get your free key.  
Header: `X-API-Key: <your_api_key>`
> **Get your API key**: Register at **https://finskills.net** — free tier available, Pro plan unlocks real-time quotes, history, and financials.

---

## When to Activate This Skill

Activate when the user:
- Asks about oil, gold, copper, natural gas, silver, or agricultural commodity prices
- Wants to understand what rising/falling commodity prices mean for markets
- Asks "is this inflationary or deflationary?"
- Wants a commodity-driven macro analysis
- Asks about Dr. Copper, gold/silver ratio, oil equity ratio
- Wants to know how commodities affect specific sectors (energy, materials, airlines, etc.)

---

## Data Retrieval — Finskills API Calls

### 1. All Commodity Spot Prices (Snapshot)
```
GET https://finskills.net/v1/free/commodity/prices
```
Extract the full commodity price dashboard:
- Energy: `crude_oil_wti`, `crude_oil_brent`, `natural_gas`, `heating_oil`, `gasoline`
- Metals: `gold`, `silver`, `platinum`, `copper`, `aluminum`, `iron_ore`
- Agricultural: `corn`, `wheat`, `soybeans`, `coffee`, `cotton`, `sugar`

### 2. Individual Commodity History (for trend analysis)
For key commodities, fetch 1-year daily history:
```
GET https://finskills.net/v1/free/commodity/history/{symbol}
```
Target symbols: `WTI` (crude oil), `gold`, `copper`, `natgas`, `wheat`  
Extract: date, price, change

### 3. FRED Commodity Data Series
```
GET https://finskills.net/v1/free/commodity/fred
```
Lists all available FRED commodity series.

```
GET https://finskills.net/v1/free/commodity/fred/{seriesId}
```
Key series to pull:
- `DCOILWTICO`: WTI Crude Oil Daily Price
- `GOLDAMGBD228NLBM`: Gold Price Daily
- `PCOPPUSDM`: Copper Price Monthly
- `TERMCBPER24NS`: Not applicable — use commodity endpoint instead

### 4. IMF Commodity Index
```
GET https://finskills.net/v1/free/commodity/imf
```
Extract: IMF primary commodity price index (energy, metals, food sub-indices)  
Use for: broad commodity cycle positioning (secular bull/bear)

---

## Analysis Workflow

### Step 1 — Commodity Price Dashboard

Create a snapshot of all key commodities with direction signals:

For each commodity, classify:
- **Near-term trend** (1-month): using price change % from history
- **Medium-term trend** (3-month): using price change % from history
- **Annual trend** (1-year): YTD change

```
Direction = {RALLYING ↑ / FALLING ↓ / FLAT ~} based on 1M change
```

### Step 2 — Key Macro Signal Derivation

**Oil Price Signal (Economic Activity + Inflation):**
- WTI > $90/bbl: Demand or supply-driven? Check supply context
  - Demand-driven high prices (global growth): Bullish for equities (especially energy, materials)
  - Supply-constriction high prices (OPEC cut): Stagflationary (bad for most assets)
- WTI $60–$90: Normal regime, not a major headwind
- WTI < $60: Disinflation signal; positive for airlines, transport, consumer discretionary

**Gold Signal (Safe Haven + Real Rate Indicator):**
Gold is inversely correlated with real interest rates (nominal rate - inflation expectations):
- Gold rising while rates rising: Unusual strength → fear of financial crisis or dollar weakness
- Gold rising while rates stable/falling: Real rates falling → inflationary signal
- Gold falling while rates rising: Normal correlation → risk-on, growth regime

**Gold/Silver Ratio:**
```
Gold_Silver_Ratio = gold_price / silver_price
```
- Ratio > 80: Economic uncertainty, risk-off (gold outperforms industrial silver)
- Ratio < 60: Industrial demand strong, economic expansion (silver outperforms)

**Copper Signal ("Dr. Copper" — Economic Barometer):**
- Copper rising: Global manufacturing expansion, China construction activity strong
- Copper falling: Global slowdown signal, watch emerging markets
- Copper/Gold Ratio: Rising ratio → economic growth; Falling → risk-off

```
Copper_Gold_Ratio = copper_price (in cents/lb) / gold_price (in $/oz)
```
When ratio rises: Yields typically follow — confirms growth regime
When ratio falls: Deflationary forces at work

**Natural Gas Signal (Seasonal + Domestic):**
- Winter: High nat gas = positive for utilities, LNG exporters, coal substitution
- Summer: High nat gas = heat wave demand; positive for utilities

**Agricultural Commodities Signal (Food Inflation):**
- Wheat > $7/bushel: Food inflation pressure, CPI food component rising
- Corn, Soy: Input cost for livestock, ethanol, food processing

### Step 3 — Commodity Cycle Classification

Classify the current phase of the commodity super-cycle:

| Phase | Characteristics | Signal |
|-------|----------------|--------|
| **Early Bull** | Energy/metals rising from cyclical lows; USD weakening | Buy commodities, energy stocks, miners |
| **Middle Bull** | Broad commodity rally; tight supply; high margins | Overweight materials, energy; watch inflation |
| **Late Bull** | Speculative excess; soft commodities surging | Central bank tightening; equities under pressure |
| **Early Bear** | Commodities peak; demand destruction; rate hike impact | Short energy, reduce materials |
| **Middle Bear** | Broad selloff; energy struggling; metals weak | Defensive positioning |
| **Late Bear** | Commodity lows; capex cuts building future supply deficit | Accumulate energy/materials for next cycle |

Assign to current phase based on: direction of multiple commodity prices + interest rate environment.

### Step 4 — Asset Class Implications Matrix

Based on commodity signals, generate implications for asset classes:

| Commodity Signal | Asset Class Implication |
|----------------|------------------------|
| Oil ↑ (demand) | Energy stocks ↑; Airlines ↓; Discretionary ↓; Oil-exporting EM ↑ |
| Oil ↑ (supply cut) | All equities ↓; Gold ↑; TIPS ↑; Consumer sentiment ↓ |
| Oil ↓ | Airlines ↑; Consumer discretionary ↑; Energy stocks ↓; EM exporters ↓ |
| Gold ↑, Rates ↓ | Risk-off; Bonds ↑; USD ↓; Miners ↑ |
| Gold ↓, Rates ↑ | Risk-on; Equities ↑; Value > Growth |
| Copper ↑ | Industrials ↑; Emerging markets ↑; Materials ↑ |
| Copper ↓ | Global slowdown; Defensive sectors ↑ |
| Broad Agri ↑ | CPI food component ↑; Consumer staples mixed; EM stress |
| Broad Commodity Rally | TIPS ↑; Energy ↑; Materials ↑; Value ↑ over Growth |
| Broad Commodity Decline | Equities mixed; Discretionary ↑; Disinflation tailwind |

### Step 5 — Sector-Level Impact

Map to specific equity sectors:
- **Energy (XLE)**: Directly correlated with WTI crude
- **Materials (XLB)**: Copper, aluminum, iron ore, potash
- **Industrials (XLI)**: Broad commodity demand signal
- **Consumer Staples (XLP)**: Wheat, corn, sugar as input costs
- **Consumer Discretionary (XLY)**: Gasoline price as consumer purchasing power headwind
- **Utilities (XLU)**: Natural gas as fuel input cost
- **Airlines**: Jet fuel (kerosene, highly correlated to crude) as major cost
- **Miners/Gold stocks (GDX)**: Gold and silver price leverage

---

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║    COMMODITY MACRO SIGNAL REPORT  —  {DATE}                 ║
╚══════════════════════════════════════════════════════════════╝

🛢️  ENERGY
  WTI Crude Oil:   ${price}/bbl   {+/-}%  1M  {+/-}%  3M  {+/-}%  YTD
  Brent Crude:     ${price}/bbl   {+/-}%  1M
  Natural Gas:     ${price}/MMBtu {+/-}%  1M
  Gasoline:        ${price}/gal   {+/-}%  1M
  Oil Signal:  →  {DEMAND-DRIVEN SURGE / SUPPLY CUT SURGE / NORMAL RANGE / DEFLATIONARY DROP}

🥇 PRECIOUS METALS
  Gold:     ${price}/oz    {+/-}%  1M  {+/-}%  3M  {+/-}%  YTD
  Silver:   ${price}/oz    {+/-}%  1M
  Platinum: ${price}/oz    {+/-}%  1M
  Gold/Silver Ratio: {ratio:.1f}  →  {RISK-OFF / NORMAL / RISK-ON}
  Gold Signal: →  {SAFE HAVEN DEMAND / REAL RATES FALLING / NORMAL}

⚙️  INDUSTRIAL METALS ("Dr. Copper")
  Copper:   ${price}¢/lb   {+/-}%  1M  {+/-}%  3M
  Aluminum: ${price}/ton   {+/-}%  1M
  Iron Ore: ${price}/ton   {+/-}%  1M
  Copper/Gold Ratio: {ratio:.4f}  →  {Growth signal rising / Declining = risk-off}
  Industrial Signal: →  {EXPANSION / SLOWING / CONTRACTION}

🌾 AGRICULTURAL
  Corn:    ${price}/bu     {+/-}%  1M
  Wheat:   ${price}/bu     {+/-}%  1M
  Soybeans:${price}/bu     {+/-}%  1M
  Coffee:  ${price}¢/lb    {+/-}%  1M
  Agri Signal: →  {FOOD INFLATION PRESSURE / STABLE / DEFLATIONARY}

📊 IMF COMMODITY INDICES
  IMF All Commodities:  {index}  {+/-}%  3M
  IMF Energy Sub-Index: {index}  {+/-}%  3M
  IMF Metals Index:     {index}  {+/-}%  3M
  IMF Food Index:       {index}  {+/-}%  3M
  Cycle Phase: →  {EARLY BULL / MIDDLE BULL / LATE BULL / EARLY BEAR / LATE BEAR}

💡 MACRO SYNTHESIS
  Inflationary pressure:   {HIGH / MODERATE / LOW}
  Growth signal:           {EXPANSION / MIXED / CONTRACTION}
  USD implication:         {BEARISH on USD / NEUTRAL / BULLISH on USD}

📈 ASSET CLASS IMPLICATIONS
  OVERWEIGHT:   {asset classes and sectors benefiting from current commodity signals}
  UNDERWEIGHT:  {asset classes hurt by current commodity signals}

  Sector Playbook:
    Energy (XLE):       {↑ Strong tailwind / → Neutral / ↓ Headwind}
    Materials (XLB):    {↑ / → / ↓}
    Industrials (XLI):  {↑ / → / ↓}
    Airlines:           {↑ / → / ↓}
    Consumer:           {↑ / → / ↓}
    Gold Miners (GDX):  {↑ / → / ↓}

🔍 KEY SIGNAL TO WATCH
  {The one commodity ratio or indicator that best captures current macro regime transition,
   and what a move above/below X level would imply for portfolio positioning.}
```

---

## Limitations

- Commodity spot prices may lag physical markets by 1 business day.
- Supply-driven vs. demand-driven price changes require judgment — always consider news context.
- Agricultural commodity prices are highly seasonal and weather-dependent.
- The copper/gold ratio as a growth signal works best over multi-month periods, not day-to-day.
