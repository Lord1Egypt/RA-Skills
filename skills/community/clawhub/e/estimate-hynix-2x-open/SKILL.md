---
name: estimate-hynix-2x-open
description: Estimate the fair opening or intraday value of Hong Kong-listed CSOP SK Hynix Daily (2x) Leveraged Product (07709.HK) from its latest NAV, KRX 000660 price, Nasdaq SKHY return, ADR conversion ratio, FX, and prior market discount. Use for 07709 fair-value, opening-price, premium/discount, tracking-risk, or cross-market arbitrage questions.
---

# Estimate Hynix 2x Open

Estimate a timestamped NAV fair value and a separate tradable-price scenario. Treat KRX 000660 as the primary price anchor and SKHY as an overnight direction check.

## Workflow

1. Record the analysis date, Hong Kong time, and intended estimate point.
   - KRX opens at 09:00 KST / 08:00 HKT.
   - SEHK opens at 09:30 HKT.
   - For a same-day SEHK opening estimate, use the latest KRX quote immediately before 09:30 HKT when available.
2. Fetch and timestamp these inputs:
   - 07709.HK last NAV per unit in HKD and prior SEHK market close.
   - KRX 000660 previous close, current-day open, and latest price.
   - Nasdaq `SKHY.O` previous close and latest close.
   - USD/KRW for ADR parity diagnostics.
   - Current and prior USD/HKD only if their change is material; otherwise use an HKD FX factor of `1`.
3. Verify symbols before calculation.
   - Wind may normalize `07709.HK` to `7709.HK`.
   - Query Nasdaq as `SKHY.O`; bare `SKHY` may collide with another security.
   - Confirm the SKHY ADS ratio from a current primary filing. The current ratio is ten ADSs per common share because one ADS represents one-tenth of one common share.
4. Apply the price hierarchy:
   - Primary: actual KRX opening/latest return.
   - Secondary: SKHY overnight percentage return.
   - Diagnostic only: SKHY absolute-price parity after ADS and FX conversion.
5. Run the bundled calculator. Example:

```bash
python3 scripts/estimate_open.py \
  --nav-hkd 27.249 \
  --product-prev-market 25.36 \
  --kr-prev-close 1322000 \
  --kr-open 1697000 \
  --kr-current 1628000 \
  --adr-prev-close 126.79 \
  --adr-close 149 \
  --usdkrw 1427.68
```

6. Report three separate outputs:
   - `NAV理论价`: prior NAV multiplied by the targeted 2x daily KRX return.
   - `折价延续价`: NAV theoretical value with the prior 07709 market discount carried forward.
   - `ADR信号价`: prior NAV with 2x SKHY overnight return; label it a cross-check, never the main value when ADR parity is distorted.
7. Give one executable conclusion with a central price and a scenario range. State that the estimate changes one-for-one with the KRX input through the formula below.

## Formulas

```text
r_KR = P_KR,anchor / P_KR,prev_close - 1
NAV理论价 = NAV_prev × (1 + 2 × r_KR + tracking_adjustment) × HKD_FX_factor

r_ADR = P_ADR,close / P_ADR,prev_close - 1
ADR信号价 = NAV_prev × (1 + 2 × r_ADR)

ADR隐含韩股价 = P_ADR,close × 10 × USDKRW
ADR绝对溢价 = ADR隐含韩股价 / P_KR,anchor - 1

昨日07709折价 = P_07709,prev_close / NAV_prev - 1
折价延续价 = NAV理论价 × (1 + 昨日07709折价)
```

Do not use the prior 07709 market close as the leverage calculation base. That price already contains a secondary-market premium or discount.

## Decision Rules

- If `|ADR绝对溢价| > 5%`, use SKHY only for percentage direction and flag impaired arbitrage.
- If the KRX market is open, the latest KRX return overrides the ADR return.
- If KRX has moved more than 20%, show both the KRX opening value and latest-price value because gap retracement materially changes 07709 fair value.
- If prior 07709 discount exceeds 5%, provide both NAV fair value and carried-discount tradable value.
- Do not treat the manager or market maker quote as the NAV itself. Separate fund NAV, indicative NAV, and exchange price.
- Do not call a point estimate exact. During extreme volatility, use a range of at least the ADR-signal value through the latest-KRX value, then explain which endpoint is more credible.

## Risk Checks

Always check:

- NAV timestamp and whether it belongs to the immediately preceding dealing day.
- KRX circuit breaker, daily price limit, suspension, or delayed quote.
- Swap and option capacity, creation/redemption availability, and market-maker effectiveness.
- Intraday tracking error, high derivative financing costs, bid-ask spread, and one-day leverage reset.
- Large SKHY ADS premium caused by incomplete cross-border conversion/arbitrage.
- USD/HKD conversion between USD NAV and HKD trading price.

Read [references/methodology.md](references/methodology.md) for source priority, product-document facts, and interpretation limits.
