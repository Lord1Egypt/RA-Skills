# Debt, Credit Facilities, and Covenants

Debt buys time against an asset or a known milestone; equity buys time against a story. Debt is the cheapest capital in the stack until a covenant trips — at that point the lender, not you, controls the timing of every decision.

## Choosing the Instrument

| Instrument | Use | Cost shape | Secured on | Fails when |
|---|---|---|---|---|
| Revolver | Smoothing working-capital swings | Interest + unused-line fee | Eligible receivables (borrowing base) | AR ages or concentrates; base shrinks as sales slow |
| Term loan | A specific asset or fit-out | Fixed amortizing payments | The asset | Cash flow is variable and the payment is not |
| Venture debt | Extending runway to a named milestone after an equity round | Interest + warrants + final payment fee | All assets, often including IP | Metrics deteriorate; MAC and minimum-cash covenants bite |
| AR factoring | Immediate cash against invoices | Discount to face, per month | The invoices | Used as permanent financing; annualized cost is brutal |
| Equipment financing | Hardware, lab, fit-out | Fixed payments, sometimes lower rate | The equipment | Financing equipment you should have leased |
| Revenue-based financing | Marketing or growth spend with a measured payback | A fixed multiple repaid as a share of monthly revenue | The revenue stream | Growth slows: the share keeps applying and the effective rate climbs |
| Grants and credits | Non-dilutive funding for R&D or location-based programs | Application effort, reporting obligations | Nothing | Treated as timely cash — disbursement lags approval by months |
| Convertible note / SAFE | Bridge to a priced round | Dilution, not interest | Nothing | Treated as debt in planning — it is future equity |

Default: no debt before a priced round. Escape hatch: a revolver secured while healthy and left undrawn, which costs only the unused-line fee.

## Venture Debt — Canonical Numbers

Canonical home for venture-debt sizing: every venture-debt figure quoted elsewhere in this skill defers to the numbers below.

- Sized at roughly **25–35% of the last equity round**, raised within **6–12 months** of that close while metrics are still the ones the lender underwrote. Later, you are re-underwritten on data that has drifted.
- All-in cost = interest + **warrant coverage** (commonly quoted as a percentage of the facility, converted into shares at the last round price) + an end-of-term or final-payment fee. Comparing lenders on the headline rate alone is how the expensive facility wins.
- The real product is the **interest-only window**. Runway gained = net proceeds ÷ forecast monthly net burn, minus the amortization that starts inside your horizon. Worked: $4M drawn against $400K/mo burn looks like 10 months, but if amortization begins at month 12 at ~$110K/mo, months 13+ each cost you a quarter of a month of runway back.
- Draw deadlines are real: facilities commonly expire undrawn after a stated window. Model the draw date, not the signing date.

## Covenants

| Covenant | Typical test | How it trips | Pre-emptive move |
|---|---|---|---|
| Minimum cash / liquidity | Month-end balance above a floor, tested monthly | A slow collections month, not a bad business | Model every test date in the 13-week forecast |
| Minimum revenue or ARR | Trailing period vs a plan filed at signing | You re-plan downward and forget the covenant was set to the old plan | Re-file the plan with the lender when the board approves a new one |
| Reporting | Financials delivered within N days of month/quarter end | Late close — the most common technical default and the cheapest to avoid | Put lender delivery dates in the close calendar |
| Material adverse change | Subjective, lender's judgment | A down round, a key customer loss, a founder departure | Tell the lender before they read it somewhere else |
| Cash dominion / lockbox | Collections sweep to a lender-controlled account | Triggered by a covenant breach, not by default | Know the trigger; it removes your control of daily cash |

**Headroom rule**: any covenant test date inside the forecast window with under 10% headroom gets negotiated now, not at the test. Waivers before a breach cost a fee and a tighter term; waivers after a breach are repriced with your leverage gone.

## Revolvers and the Borrowing Base

- Advance rates commonly run **80–85% of eligible receivables** — and "eligible" excludes invoices aged past 90 days, balances above a concentration cap, foreign customers, intercompany, and anything disputed. A $2M AR ledger routinely supports far less than $1.6M of availability; ask for the eligibility schedule before you count the line as runway.
- Availability shrinks exactly when sales slow: the facility is procyclical. Never plan payroll against undrawn availability.
- Unused-line fees are the price of optionality; they are cheap insurance and belong in the budget as such.

## Factoring and Receivable Finance

- Quoted per month (commonly 1–3% of face); annualize before comparing to anything else. 2% per month is roughly 27% per year compounded — expensive money dressed as a service fee.
- **Recourse vs non-recourse**: recourse means you eat the bad debt anyway; non-recourse prices that risk in.
- Notification factoring tells your customers to pay a third party. That is a signal about your solvency that travels through the customer's AP department.

## Debt vs Equity

| Factor | Favor debt | Favor equity |
|---|---|---|
| Cash flow | Predictable, positive | Variable, negative |
| Dilution tolerance | Low | Higher acceptable |
| Use of funds | Asset purchase, bridge to a known event | Open-ended growth |
| Timeline | Short-term, defined | Long-term runway |
| Downside | You still owe it | You do not |

Debt is cheap until a covenant trips; equity is expensive but cannot be recalled. The test that decides it: if the bear case arrives, does this instrument make the bear case survivable or fatal?

## Before Signing

- Model the bear case with the debt service in it — if the bear case breaches a covenant, you are buying a trigger, not runway.
- Price the full stack: interest + warrants + fees + legal, expressed as a single annualized number.
- Read the events of default and the cure periods; those, not the rate, are the terms that matter.
- **Personal guarantees and founder liability never get agreed inside this skill** — counsel and the founder decide (SKILL.md Human-in-the-Loop).
- Keep the lender relationship warm with the same monthly reporting the board gets. Lenders forgive bad numbers they saw coming and punish surprises.
