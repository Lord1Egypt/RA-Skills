# Yield Curve

description: CN-HK-US rates, HIBOR-LIBOR linkage, HKD currency peg stress test. Triggers on "yield curve", "rates", "HIBOR", "CNY rates", "Fed", "PBOC", "peg".

## Workflow

### Step 1: Frame
Confirm focus: China rates, HK rates, US rates, cross-market linkage, or full tri-polar view.

### Step 2: Gather data
Run in parallel (max 2 calls):
- `get_macro_data(indicators=["US_10Y", "US_2Y", "US_FFR", "CN_10Y", "CN_1Y", "CN_LPR_1Y", "HK_10Y", "HK_1Y"], period="1y")`
- `get_macro_data(indicators=["HIBOR_1M", "HIBOR_3M", "LIBOR_3M", "USD_HKD", "HKMA_BASE_RATE"], period="1y")`

Then:
- `get_macro_data(indicators=["CN_HK_BOND_SPREAD", "HKD_FORWARD_POINTS", "HK_M1", "HK_M2"], period="6mo")`

### Step 3: Analyze
1. **Yield Curve Shape** (each market)
   - US: 10Y-2Y spread (recession signal if inverted)
   - China: 10Y-1Y spread (growth signal if steep)
   - HK: 10Y-1Y spread (HIBOR-driven front end)

2. **HIBOR-LIBOR Linkage**
   - HIBOR should track LIBOR/SOFR under currency peg
   - Gap > 50bps sustained = stress signal
   - HKMA base rate follows Fed upper bound

3. **Currency Peg Stress Test**
   - Current USD/HKD vs 7.75-7.85 band
   - HKMA intervention history (weak side/strong side)
   - Forward points as market expectation

4. **Tri-Polar Convergence/Divergence**
   - PBOC easing vs Fed tightening → HK in middle
   - CN-HK bond spread → northbound/southbound flow signal

### Step 4: Present
```
| Market | 10Y | 2Y | Curve (10Y-2Y) | Trend |
|--------|-----|----|-----------------|-------|
| US | ... | ... | ... | ... |
| China | ... | ... | ... | ... |
| HK | ... | ... | ... | ... |

HIBOR-LIBOR Spread: ... bps (flag if >50bps)
USD/HKD: ... (band: 7.75-7.85)
Forward Points: ... (premium/discount signal)
Peg Stress: GREEN / YELLOW / RED
```

Add "Implications for HK Equities" section:
- HIBOR rise → property sector pressure
- CN easing → southbound flow support
- Peg stress → HKMA liquidity tightening

## Important Notes
- Token: respect depth setting from style.md; current levels first, history on request
- HK-specific: HIBOR and peg are the unique HK angles; always include
- Use latest available data; note data date if stale
- Max 2 parallel calls per step
