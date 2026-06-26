# Recipe: Valuation Check (DCF vs Price)

## Goal
Compare FMP's DCF model estimate to the current market price, descriptively and with heavy caveats — never as a recommendation.

## When to use
The user asks "is <company> overvalued/undervalued", "what's the fair value", or "how does the DCF compare to price". Reframe any "should I buy" into a data comparison plus disclaimer.

## Inputs
- Company name or ticker.
- `FMP_API_KEY` in the environment.

## Steps
1. **Resolve & confirm** the symbol (search → profile). Note `currency`.
2. **Pull DCF:** `/discounted-cash-flow?symbol=<TICKER>`. Read `dcf` (model intrinsic value/share), the comparison `price`/`Stock Price`, and `date`.
3. **Pull a fresh quote** (optional) `/quote?symbol=<TICKER>` for the current market price as-of timestamp.
4. **Add context** (optional): `/key-metrics` for `peRatio`, `evToSales` to frame the valuation.
5. **Compare descriptively:** state model DCF vs market price, the gap, and the as-of date.
6. **Caveat heavily and disclaim.** Make clear this is a single model's estimate built on assumptions (growth, discount rate, terminal value) and is not advice or a price target.

## Output
- DCF value/share + currency + model `date`.
- Market price + currency + as-of.
- A neutral comparison ("model estimate is above/below current price by X").
- Caveats about model assumptions.
- Source + not-investment-advice disclaimer.

## Example
> **TSLA valuation check (USD; FMP `/discounted-cash-flow`, date 2026-05-29)**
> FMP DCF model estimate: 210.00 USD/share.
> Market price: 245.00 USD (FMP `/quote`, delayed, as of 2026-05-30).
> The model's estimate is ~14% below the current market price. **This is one model's estimate** based on assumptions (growth, discount rate, terminal value) that may not hold; it is not a price target. Source: FMP. *Informational only, not investment advice — verify independently.*

(Illustrative format only — report live API values.)

## Edge cases
- **Negative or missing `dcf`** → model couldn't produce a meaningful value (often for unprofitable/early companies); say so, don't force a number.
- **Stale model `date`** → flag that the DCF run may predate recent results.
- **Empty array** → symbol wrong or not covered; re-resolve.

## Production notes
- 1–2 calls. Cache the DCF in-session.
- Never output "undervalued → buy" as a conclusion; keep it a descriptive comparison.
- Always include the disclaimer for any valuation framing.
