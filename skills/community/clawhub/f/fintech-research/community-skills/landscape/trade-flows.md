# Trade Flows

description: Trade and capital flows, Stock Connect north/south flow, HKD liquidity. Triggers on "trade flows", "capital flows", "connect flow", "southbound", "northbound", "HKD liquidity".

## Workflow

### Step 1: Frame
Confirm focus: trade balances, Stock Connect flows, FDI/ODI, or HKD liquidity specifically.

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_macro_data(indicators=["CN_TRADE_BALANCE", "CN_EXPORTS", "CN_IMPORTS", "HK_TRADE_BALANCE", "HK_EXPORTS"], period="1y")`
- `get_macro_data(indicators=["STOCK_CONNECT_SOUTH", "STOCK_CONNECT_NORTH", "HK_FDI", "CN_FDI"], period="6mo")`

Then:
- `get_macro_data(indicators=["HKD_M2_GROWTH", "HK_INTERBANK_LIQUIDITY", "CN_FX_RESERVES"], period="6mo")`

### Step 3: Analyze
1. **Trade Flows**
   - China trade balance trend (surplus/deficit direction)
   - HK re-export trade (China → HK → world pipeline)
   - Key trading partners shift (ASEAN vs US vs EU)

2. **Stock Connect Flows**
   - Southbound ( mainland → HK ) daily/weekly cumulative
   - Northbound ( HK → mainland ) daily/weekly cumulative
   - Net flow direction as sentiment signal
   - Top southbound sectors (tech, finance, healthcare)

3. **Capital Account**
   - FDI into China trend
   - ODI from China (infrastructure, resource deals)
   - HK as conduit: percentage of China FDI routed through HK

4. **HKD Liquidity**
   - HKD M2 growth rate
   - Interbank liquidity level
   - HKMA intervention (weak side/strong side)
   - Linked exchange rate system health

### Step 4: Present
```
| Flow Type | Latest | 1M Avg | 3M Avg | Trend | Signal |
|-----------|--------|--------|--------|-------|--------|
| CN Trade Balance | ... | ... | ... | ... | ... |
| Southbound Daily | ... | ... | ... | ... | ... |
| Northbound Daily | ... | ... | ... | ... | ... |
| HKD M2 Growth | ... | ... | ... | ... | ... |
```

Add "Stock Connect Flow Chart" (text-based if no graphics):
- Weekly southbound cumulative flow (last 12 weeks)
- Flag if weekly southbound > HK$10bn (strong inflow)
- Flag if weekly southbound < -HK$5bn (significant outflow)

Add "HK Equity Market Implications" section.

## Important Notes
- Token: respect depth setting from style.md; flow summary first, detail on request
- HK-specific: Stock Connect southbound is the primary HK equity flow signal
- HKD liquidity and peg health are unique HK angles
- Note data lag if macro data is not real-time
- Max 2 parallel calls per step
