---
name: build-protocol-decision
description: "Rigorous workflow for high-stakes decision-making: investments (stocks/crypto/real-estate), major purchases, technology selection, supplier choice. Use when the decision commits >$1000 or >1 day of effort, is hard to reverse, or involves tradeoffs between multiple alternatives. Inherits build-protocol core rules, adds decision-specific: real-time data verification mandate (never trust document prices), methodology transparency (PE/DCF/MA required, no gut calls), position-sizing discipline, stop-loss as first-class rule, daily P/L tracking. Guards against 'Sycophancy of Precision'—writing '+12.85%' looks trustworthy but precision ≠ accuracy. Triggers on: 'should I buy/invest in X', 'compare options', 'pick a vendor', '选哪个', '投资策略', '操盘手册', 'which option', 'buy vs build', '怎么选'."
version: 1.0.1
---

# Build Protocol · Decision

> Apply rigorous process to decisions that cost money, time, or opportunity—before committing, not after.
>
> Inherits the 8 Iron Rules from `build-protocol`. Adds 3 decision-specific rules and a 10-step workflow tuned for high-stakes choices.

## When to Use

**Triggers** (any one):
- Decision commits **>$1,000 or >1 day of effort**
- Decision is **hard to reverse** (stocks, hardware, vendor contracts, hiring)
- Multiple alternatives with real tradeoffs exist
- Investment, trading, or portfolio questions
- Technology selection, supplier choice, buy-vs-build
- Explicit: "should I buy X", "compare options", "pick a vendor", "选哪个", "怎么选"

**Don't use for**:
- Reversible, low-cost choices (which coffee to order)
- Pure knowledge production (use `build-protocol` instead)
- Decisions already made—this is pre-decision, not post-rationalization

---

## Inherits from build-protocol (8 Iron Rules)

| # | Rule | Decision context |
|---|---|---|
| 1 | **Independent Audit unmissable** | Audit = verify methodology + data freshness, not just content |
| 2 | **Plan before Execute** | Map options before picking; list constraints before scoring |
| 3 | **≤2 parallel sub-agents** for shared-state research (writing/editing same files); ≤4 acceptable for independent investigations | Inherits build-protocol concurrency reasoning; see `trinity-harness` for general-purpose limits |
| 4 | **Why This Way** | Every recommendation needs methodology, not just "I think" |
| 5 | **Version + Errata iteration** | Revisit decision log when facts change |
| 6 | **3-layer consistency** | Data source ↔ analysis ↔ recommendation must align |
| 7 | **Anti-Sycophancy content** | Must list downsides and failure modes; all-upside = fake |
| 8 | **Independent review ≠ self-audit** | Recommendation author ≠ final reviewer |

---

## Decision-specific 3 New Iron Rules

| # | Rule | Why |
|---|---|---|
| 9 | **Real-time data verification — never trust document prices** | Document prices are stale within 24h. A written "$X" that hasn't been verified live is fiction. |
| 10 | **Methodology transparency (PE/DCF/MA/decision matrix required — no gut calls)** | "I think this is a good buy" is not analysis. Every recommendation must show its math. |
| 11 | **Stop-loss first, profit-target second** | Asymmetric downside means exits matter more than entries. Define maximum loss before opening any position. |

---

## The Decision Workflow (10 Steps)

### Pre-decision (Steps 1–4)

**Step 1 — Research: Gather options**
- List all candidates (don't anchor on first option)
- Source: web search, product reviews, market data, expert opinions
- Output: options list with brief description of each

**Step 2 — Set constraints**
- Budget ceiling (hard limit)
- Timeline (when must decision be made / when does it take effect)
- Hard-no's (non-negotiable disqualifiers)
- Risk tolerance (for investments: max drawdown you can stomach)

**Step 3 — Fetch real-time data** ⚠️ non-skippable
- **Stocks**: `curl "https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlcv&h&e=csv"`
- **Crypto**: CoinGecko API or Binance spot price
- **Products**: scrape current listing price (Amazon/retailer)
- **Services**: current vendor pricing page (not cached / not PDF)
- If real-time data is unavailable → state explicitly, do not substitute document prices

**Step 4 — Compare on dimensions (build comparison matrix)**
- Define 4–8 scoring dimensions relevant to this decision
- Score each option per dimension (1–5 or weighted %)
- Make tradeoffs explicit; no option should be "best on all dimensions"

### Decision (Steps 5–7)

**Step 5 — Apply methodology**
- **Investments**: PE ratio (vs sector median), DCF estimate, technical levels (MA50/MA200), catalyst timeline
- **Purchases**: TCO (total cost of ownership over 3 years), not just sticker price
- **Technology/vendor**: Gartner-style magic quadrant or weighted decision matrix
- Show your work. If you used PE, show the number. If you used DCF, show the inputs.

**Step 6 — Plan B and exit conditions**
- Investments: hard stop-loss level, reason to exit (not just price but thesis invalidation trigger)
- Purchases: return policy window, resale value estimate
- Tech/vendor: contract termination terms, migration cost estimate
- Define these **before** committing, not after things go wrong

**Step 7 — Make decision + document rationale**
- State the chosen option clearly
- One-paragraph "Why This" (not why the others are bad—why this one fits the constraints)
- One-paragraph "Why Not the Alternatives" (must be honest, not dismissive)
- Date-stamp the decision (facts change; you need to know how old this reasoning is)

### Post-decision (Steps 8–10)

**Step 8 — Execute with position sizing**
- Investments: size = (account risk per trade) ÷ (entry − stop-loss). Never max-leverage on first entry.
- Purchases: confirm budget compliance before checkout
- Tech/vendor: phased rollout if possible; don't migrate 100% on day one

**Step 9 — Track P/L daily** (not weekly, not monthly)
- Record entry price, current price, unrealized P/L in a daily log
- For non-investment decisions: track KPIs that validate the decision (e.g., tool adoption rate, cost savings vs projection)
- Daily tracking catches thesis-breaking events early; weekly/monthly is too slow

**Step 10 — Review and adjust (kill bad bets fast)**
- Weekly: is thesis still intact? Did the stop-loss get hit?
- Monthly: compare actual outcome vs pre-decision projection
- If thesis is broken: exit at stop-loss, do not average down hoping it recovers
- Log lessons in a decision postmortem (even for winners—understand why it worked)

---

## The "Sycophancy of Precision" Warning ⚠️

**The problem**: Writing `+12.85%` feels more credible than "about +13%". But precision ≠ accuracy. When the underlying data is an estimate or an outdated figure, adding decimal places is misleading—it manufactures false confidence.

**How it shows up**:
- AI stitches together multi-source data and presents blended numbers as if they're exact
- Historical document prices get reused as if they're current
- Compound calculations give precise outputs from imprecise inputs

**The rule**:
- Any number derived from estimates → append "(est.)" or "(含估算)"
- Any number from a source >24h old → append the source date
- Round to 2 significant figures when inputs are uncertain; don't carry false precision
- Example: `+12.85% (est., based on 3-day average)` not just `+12.85%`

---

## Real-time Data Sources Required

| Asset class | Source | Command / URL |
|---|---|---|
| US stocks | Stooq | `curl "https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlcv&h&e=csv"` |
| US stocks (alt) | Yahoo Finance | `curl "https://query1.finance.yahoo.com/v8/finance/chart/SYMBOL"` |
| Crypto | CoinGecko | `curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"` |
| Products | Retailer page | Direct web fetch; no cached PDFs |
| Forex | Stooq | `curl "https://stooq.com/q/l/?s=USDJPY&f=sd2t2ohlcv&h&e=csv"` |

**🔴 Never use**: Prices from documents, spreadsheets, or chat history. Even a price from yesterday's analysis is stale.

---

## Anti-patterns (Decision-specific)

| ❌ Anti-pattern | Why it fails |
|---|---|
| "I think it should work" without backtesting | Gut calls without data = coin flip with extra steps |
| No stop-loss defined before entry | You will rationalize holding through any loss |
| Doubling down on a loser "to average down" | Throwing good money after bad; thesis may already be broken |
| Fake precision ("+12.85%" without methodology) | Sycophancy of precision; decimal places don't add accuracy |
| Cherry-picking favorable data | Confirmation bias in analysis = surprises at execution |
| Using document prices instead of live data | 24h-old stock price is meaningless for a decision made today |
| Daily P/L tracking skipped (tracking weekly/monthly) | Weekly is too slow to catch a thesis-breaking move |
| "Buy more to feel better" after a loss | Emotions ≠ analysis; size down when uncertain, not up |
| Recommendation with no methodology shown | "It looks good" is not analysis |
| All-upside analysis (no failure modes listed) | Real decisions have tradeoffs; omitting downside = sycophancy |

---

## Gotchas

- **Polymarket / prediction market cost basis** ≠ current MTM value (look up current contract price before calculating P/L)
- **Document prices expire within 24h** for liquid assets; within weeks for products
- **AI recommendation confidence ≠ data freshness** — a confident-sounding AI answer with no live data check is high-risk
- **MA/RSI are lagging indicators** — they describe past price action, not future movement; use as context, not predictions
- **DCF sensitivity is high** — small changes to discount rate or terminal growth change the output by 30–50%; always run a range, not a single number
- **Position sizing compounds errors** — if your entry price is wrong by 5%, your stop-loss distance is wrong too; use real-time price in sizing calculation

---

## References

- `references/decision-workflow.md` — Full 10-step workflow with per-step checklists
- `references/investment-playbook-template.md` — Generic investment playbook template (anonymized)
- `references/audit-script-decision.sh` — Bash script to verify methodology transparency and data freshness

## Related Skills

- `build-protocol` — Parent skill for long-form knowledge production (8 Iron Rules source)
- `academic-research-hub` — For decisions requiring deep literature review
- `feishu-bitable` — For tracking decision logs and P/L records in Bitable

---

_Distilled: 2026-04-30 · Inherits: build-protocol v1.1_
_Validated on: Investment decision audits, technology selection, major purchase comparisons_
