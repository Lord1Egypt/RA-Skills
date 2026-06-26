# Financial Tracker — Advanced Patterns

*by The Agent Ledger | theagentledger.com*

---

## 1. Multi-Stream Revenue Dashboard

If you run more than one income stream (e.g., digital products + services + affiliate), configure a stream-aware dashboard:

**Tell your agent:**
> "Set up a multi-stream revenue dashboard. My streams are: [list them]."

Your agent creates a `finance/streams.md` file:

```markdown
# Revenue Streams

| Stream | MTD | Goal | % of Goal | YTD |
|--------|-----|------|-----------|-----|
| digital-products | $587 | $2,000 | 29% | $587 |
| services | $660 | $2,000 | 33% | $660 |
| affiliate | $0 | $500 | 0% | $0 |
| **Total** | **$1,247** | **$4,500** | **27.7%** | **$1,247** |
```

**Trigger:** "Give me the stream dashboard" or include it in your weekly review prompt.

**Why it matters:** Single-source income concentration is the most common financial risk for solopreneurs. This makes it visible before it becomes a crisis.

---

## 2. Revenue Cadence Tracking

Track not just *how much* you earned, but *when* — because timing matters for cash flow:

```markdown
## March 2026 — Revenue by Week

| Week | Income | Running Total | % of Monthly Goal |
|------|--------|---------------|-------------------|
| Mar 1–7 | $320 | $320 | 6.4% |
| Mar 8–14 | $660 | $980 | 19.6% |
| Mar 15–21 | $267 | $1,247 | 24.9% |
| Mar 22–31 | — | — | — |
```

**Tell your agent:** "Track my revenue by week this month."

Use this to spot patterns: Do you tend to earn on specific days? Does your cadence improve after newsletter sends? Knowing your revenue rhythm helps you plan.

---

## 3. Automated Month-End Close

Set up a monthly cron (or heartbeat check) to automatically close the books:

**Heartbeat addition:**
```markdown
## Month-End Check (run on last day of month)
- Check if today is the last day of the month
- If yes: generate monthly P&L from income-log.md and expense-log.md
  → Append to monthly-summary.md
  → Update finance-state.json (reset current_month, update ytd)
  → Update tax-estimates.md with Q total if quarter end
  → Flag any cash flow warnings
  → Brief me with the summary
```

**Cron alternative:**
```bash
openclaw cron add \
  --name "month-end-close" \
  --cron "0 18 28-31 * *" \
  --model "anthropic/claude-haiku-3-5" \
  --session isolated \
  --message "Check if today is the last day of the month. If yes, run the month-end close: generate P&L from finance/income-log.md and finance/expense-log.md, append to finance/monthly-summary.md, update finance-state.json, and send me a summary." \
  --announce \
  --to "[YOUR_TELEGRAM_CHAT_ID]" \
  --tz "America/Chicago"
```

---

## 4. Expense Audit Ritual

Once a quarter, run a full expense audit to find waste:

**Tell your agent:**
> "Run a quarterly expense audit. Pull all expenses from expense-log.md for Q[n], categorize them, and flag anything that looks redundant, unused, or over-budget."

Your agent produces:

```markdown
## Q1 2026 Expense Audit

Total Expenses: $547.50
vs. Budget ($1,500): 36.5% ✅ well under

**By Category:**
| Category | Total | % of Spend |
|----------|-------|------------|
| Tools/software | $240 | 43.8% |
| Platform fees | $187 | 34.2% |
| Education | $120 | 21.9% |

**Flags:**
- ⚠️ Canva Pro + Adobe Express both active — potential duplicate ($28/mo)
- ✅ AI tools ($60/mo) — high-leverage, keep
- ⚠️ $120 course purchased March 15 — no related project logged in project-tracker
```

---

## 5. Price Sensitivity Tracking

When you change prices, log it and track the revenue impact:

```markdown
## Price Changes

| Date | Product | Old Price | New Price | Reason |
|------|---------|-----------|-----------|--------|
| 2026-03-01 | Premium Guide | $0 (free) | $49 | Launch |
| 2026-04-01 | Premium Guide | $49 | $79 | Regular price |
```

**Tell your agent:** "Log a price change: [product], from $[old] to $[new], reason: [why]."

After each price change, compare average monthly revenue before and after:
> "Compare revenue from digital-products before and after March 1."

---

## 6. Goal-to-Revenue Mapping

Link your financial goals to income sources so you know exactly what needs to happen:

```markdown
## Revenue Plan — Q2 2026

Monthly target: $5,000

**How I'll get there:**

| Source | Expected | Confidence | Driver |
|--------|----------|------------|--------|
| Premium guide sales | $2,000 | 60% | Newsletter list + Reddit |
| Consulting | $2,000 | 80% | Existing clients |
| Etsy | $500 | 70% | Organic SEO |
| Affiliate | $500 | 40% | New — untested |
| **Total Expected** | **$5,000** | — | — |
```

**Tell your agent:** "Build a revenue plan for next month. My sources and expected amounts are: [list]."

Review actual vs plan at month end:
> "Compare Q2 revenue plan to actuals."

---

## 7. Income Concentration Risk Monitor

The most dangerous financial position for a solopreneur: one source > 60% of revenue.

Add to `HEARTBEAT.md`:
```markdown
## Income Risk Check
- Pull last 30 days from finance/income-log.md
- Calculate income concentration by source
- If any single source > 60%: flag as ⚠️ CONCENTRATION RISK
- If any single source > 80%: flag as 🔴 CRITICAL — one client/product risk
```

Your agent will surface this automatically during briefings.

---

## 8. Annual Financial Review

At year-end, your agent generates a comprehensive annual review:

**Tell your agent:** "Generate my annual financial review for 2026."

```markdown
## 2026 Annual Financial Review

**Revenue**
Total Income: $XX,XXX
vs. Annual Goal ($60,000): XX%
Best Month: [month] ($X,XXX)
Worst Month: [month] ($X,XXX)
Average Month: $X,XXX

**Expenses**
Total Expenses: $X,XXX
Largest Category: tools/software ($X,XXX)
vs. Annual Budget: XX%

**Net Income: $XX,XXX**
Estimated Tax Reserve (30%): $X,XXX

**Revenue Mix:**
| Source | Total | % |
|--------|-------|---|
| digital-products | $X,XXX | XX% |
| services | $X,XXX | XX% |

**Year-Over-Year:**
(Not available — first year tracked)

**Flags:**
- [key observations]

**Top 3 Financial Lessons from 2026:**
1. [agent reflects on biggest patterns from the data]
2. 
3. 
```

---

## 9. Integration: Solopreneur Assistant Weekly Review

Add financial data to your weekly review automatically:

In `SOUL.md` or `AGENTS.md`, instruct your agent:
```markdown
When running the weekly business review, always include:
- Current month revenue vs target (from finance/finance-state.json)
- Any active cash flow flags
- YTD net income and estimated tax reserve
Pull this from the finance/ directory before generating the weekly review.
```

---

## 10. Newsletter Revenue Tracking

If your newsletter drives product sales, track the correlation:

```markdown
## Newsletter → Revenue Log

| Issue | Send Date | Products Linked | Revenue (7-day) | Revenue (30-day) |
|-------|-----------|----------------|-----------------|------------------|
| #3 | 2026-03-07 | Premium Guide | $147 | TBD |
| #2 | 2026-02-20 | — | $0 | $0 |
```

**Tell your agent:** "Log newsletter revenue: Issue #3, sent March 7, generated $147 in the following 7 days."

Over time, this tells you which issues convert to revenue and which don't — invaluable for deciding what content to prioritize.

---

*Advanced Patterns v1.0.0 — by [The Agent Ledger](https://www.theagentledger.com)*
*Free to use under [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/). Subscribe for premium guides and advanced blueprints.*

> ⚠️ **Disclaimer:** These patterns are organizational frameworks only. Nothing here constitutes financial, tax, legal, or investment advice.
