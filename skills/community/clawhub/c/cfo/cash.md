# Cash, Runway, and Treasury

## 13-Week Cash Flow Forecast

The core CFO instrument. Direct method — actual dollars in and out, never the accrual P&L.

- Update every Monday. Track forecast vs actual per week; if collections miss by >10% two weeks running, your DSO assumption is wrong — fix the model, don't annotate the miss.
- Model inflows at historical collection speed, not contract terms. A "net 30" customer base that actually pays in 47 days is a 47-day base.
- Payroll is the anchor outflow: largest, most rigid, and the one whose miss is unrecoverable. Build the forecast around payroll dates and mark them on the sheet.
- Include the lumpy items people forget: quarterly tax payments, annual insurance and software renewals, the calendar month that carries three payroll cycles, bonus and commission payouts, and any lender delivery or repayment date.
- Any week whose ending balance falls below one payroll is an escalation, not a data point (SKILL.md Red Flags).

| Week | Beginning Cash | Inflows | Outflows | Ending Cash |
|------|----------------|---------|----------|-------------|
| 1 | $500K | $100K | $80K | $520K |
| 2 | $520K | $50K | $120K | $450K |

Inflows: customer payments by expected (not invoiced) date, funding wires, credit draws, refunds, tax credits. Outflows: payroll, rent, vendors, debt service, taxes, one-times.

**Forecast accuracy is itself a metric.** Score weekly variance and report the quarterly hit rate. A forecast that has stayed within 5% for two quarters earns the board's trust in the runway number; one nobody scores is a spreadsheet, not an instrument.

## Runway and Default Alive

```
Runway (months) = Cash / Forecast monthly net burn
```

Forecast burn includes signed offers, committed contracts, and known one-times over the next 6 months. Worked example: $2.4M cash, trailing burn $150K/mo, three signed hires adding ~$60K/mo fully loaded → forecast burn $210K → runway 11.4 months. The trailing number said 16 — a 5-month error in the direction that kills you.

**Default alive vs default dead** (Paul Graham): project current revenue growth against forecast burn — do you reach cash-flow positive before cash hits zero? If default dead, the only options are raise, cut, or grow faster, and the choice must be made in weeks, not quarters.

**Runway thresholds** (canonical — fundraising timing and the cost-cut trigger ladder both key off this table):

| Runway | State |
|--------|-------|
| 18+ months | Strong; raise only opportunistically |
| 12–17 months | Healthy; prepare the next round |
| 6–11 months | Act now: active raise or cuts that extend past 12 |
| < 6 months | Emergency: cut deep, bridge, or accept dictated terms |

Always report runway with its assumption attached — "11 months at forecast burn including the three signed offers" — never as a bare number. Two people quoting different runways are almost always quoting different burns.

## Working Capital

```
Cash conversion cycle = DSO + DIO − DPO
```

For software, DIO is zero and the cycle reduces to DSO minus DPO: the number of days you finance your customers. Positive and growing means growth consumes cash — the faster you sell, the tighter the bank balance.

**Collect faster (AR):**
- Invoice the day of delivery. DSO = AR ÷ revenue × days in period; one day of DSO on $12M annual revenue ≈ $33K of cash ($12M ÷ 365).
- Escalation ladder by days past due: 3 days before due, a reminder → day 1, a polite email → day 15, a call to the AP contact by name → day 30, the account owner calls the buyer → day 45, service-suspension notice per the contract → day 60, collections or legal. Publish the ladder so it is not renegotiated per account.
- Review aged AR weekly with sales in the room. Collections is a relationship problem wearing a finance costume: the person the customer knows gets paid faster than the invoice does.
- Early-pay discount math: offering 2/10 net 30 costs ~37% annualized (2/98 × 365/20). Offer it only when your cost of capital exceeds that or survival needs the cash — it is expensive money dressed as a courtesy.
- Annual prepay (commonly one to two months free in SaaS) converts 12 months of collection risk into day-one cash; usually the cheapest financing available. Its maximum worth to you: `cost of capital × months accelerated ÷ 12` — at a 30% cost of capital and ~5.5 months of average acceleration, a prepay discount above ~14% is you paying more for the cash than the cash is worth.
- Credit-check new customers above a size you set; bad debt is a 100% discount. One payer above ~20% of revenue is a cash risk before it is a diligence problem.

**Pay strategically (AP):**
- Use full terms by default; paying early without a discount donates your float.
- Take vendor early-pay discounts when annualized return (same formula, reversed) beats your cost of capital.
- Run payments on a fixed weekly cycle rather than ad hoc: the forecast becomes reliable and every payment passes one checkpoint where controls apply.
- Never stretch critical single-source suppliers — the relationship is worth more than the float.

## Treasury Policy

Post-SVB (2023) baseline, after solvent companies spent days unable to reach their own money:

- Operating cash at two or more banks, with enough at the secondary to cover at least one full payroll cycle. FDIC insures $250K per depositor, per insured bank, per ownership category; every dollar above that is unsecured credit exposure to that bank. Deposit-network products spread balances across institutions to extend coverage.
- Sweep excess into Treasury money-market funds or a T-bill ladder, with maturities laddered against the 13-week so a redemption is never forced at a bad moment. Policy priority order: preserve capital > liquidity > yield — a CFO who chases yield with runway is confusing jobs.
- Once excess cash exceeds a few months of burn, write a one-page board-approved investment policy: permitted instruments, maturity limits, concentration limits, and who is authorized to move money.
- Check for cash-dominion or minimum-balance clauses before moving anything: a lender may control where operating cash is allowed to sit, and a cash-dominion clause sweeps collections to a lender-controlled account the moment a covenant breaches.

## Cash Flow Patterns

Set `business_model` in config; the pattern below sizes the buffer.

- **Subscription**: predictable inflows; churn shows up in cash with a lag — the P&L sees it first, the bank account a quarter later.
- **Usage-based**: inflows track the customer's activity, so their bad quarter is your bad quarter with no notice. Buffer against the trailing trough, and never annualize a peak month — a trailing 3-month average is the only defensible run rate.
- **Transactional**: lumpy; size the cash buffer to your worst historical trough quarter, not the average.
- **Marketplace**: float between collection and payout can make you cash-positive while unprofitable — never confuse float with earnings. Watch processor holdbacks; they appear precisely when volume spikes.
- **Services**: cash follows delivery and utilization; unbilled work in progress is the silent receivable nobody ages.

