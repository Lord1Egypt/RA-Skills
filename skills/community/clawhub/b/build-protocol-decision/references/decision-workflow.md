# Decision Workflow — 10-Step Detailed Checkpoints

> Companion to `build-protocol-decision` SKILL.md.
> Each step includes: purpose, required inputs, actions, checkpoint criteria, and common failure modes.

---

## Overview

```
PRE-DECISION          DECISION              POST-DECISION
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ 1. Research  │      │ 5. Methodology│      │ 8. Execute   │
│ 2. Constraints│─────▶│ 6. Plan B    │─────▶│ 9. Track P/L │
│ 3. Live Data │      │ 7. Decide    │      │ 10. Review   │
│ 4. Compare   │      └──────────────┘      └──────────────┘
└──────────────┘
```

**Total time budget** (rough guide):
| Decision type | Steps 1-4 | Steps 5-7 | Steps 8-10 |
|---|---|---|---|
| Investment (single position) | 30–60 min | 20–30 min | Daily (5 min) |
| Major purchase ($1k–$10k) | 1–3 h | 1 h | Weekly (10 min) |
| Technology selection | 1–3 days | Half day | Monthly (30 min) |
| Vendor contract | 1–2 weeks | 2–3 days | Quarterly |

---

## PRE-DECISION

### Step 1 — Research: Gather Options

**Purpose**: Avoid anchoring on the first option you encounter.

**Required inputs**:
- Decision topic / asset class / product category
- Initial scope (price range, geography, technology stack)

**Actions**:
1. Generate a list of at least 3 candidates (force yourself beyond the obvious)
2. For each: 2–3 sentence description, source, last-updated date
3. Flag any options that are already disqualified (document why—prevents revisiting)

**Checkpoint** ✅:
- [ ] ≥3 candidates documented
- [ ] Each candidate has a source and date
- [ ] No option has been pre-selected before constraints are set

**Failure modes**:
- ❌ Starting with one option and building a case for it (confirmation bias anchor)
- ❌ Only researching options you already know (availability heuristic)

---

### Step 2 — Set Constraints

**Purpose**: Define the decision space before evaluating options. Constraints set after seeing options are rationalized backward.

**Required inputs**:
- Budget ceiling (hard limit — any option above this is disqualified regardless of quality)
- Timeline (when must decision be final, when does it take effect)
- Hard-no's (non-negotiable disqualifiers: e.g., no vendor lock-in, no leverage >2x, no proprietary format)
- Risk tolerance (for investments: max drawdown you can sustain without being forced to exit)

**Actions**:
1. Write out each constraint in a table: Constraint | Type (Hard/Soft) | Reason
2. Apply hard constraints to filter the options list from Step 1
3. Document how many candidates remain after filtering

**Checkpoint** ✅:
- [ ] Hard constraints documented before scoring begins
- [ ] Filtered candidates list produced
- [ ] Risk tolerance stated in measurable terms (%, $, days)

**Failure modes**:
- ❌ Setting constraints after scoring begins ("we'll make an exception for this one")
- ❌ No hard constraints at all — every constraint is "flexible"

---

### Step 3 — Fetch Real-time Data ⚠️ Non-skippable

**Purpose**: All analysis is worthless if built on stale prices or outdated specs.

**Required inputs**:
- List of candidates from Steps 1–2
- Asset identifiers (ticker symbols, product URLs, vendor pricing pages)

**Actions**:

**For stocks / ETFs**:
```bash
# Stooq (free, no API key)
curl "https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlcv&h&e=csv"
# Returns: Date,Open,High,Low,Close,Volume
```

**For crypto**:
```bash
# CoinGecko (free tier)
curl "https://api.coingecko.com/api/v3/simple/price?ids=COIN_ID&vs_currencies=usd&include_24hr_change=true"
```

**For products**:
- Fetch the current product listing page (web_fetch)
- Extract: current price, date of page, stock status
- Note any sale/promo end date

**For services/SaaS**:
- Fetch current pricing page (not a PDF, not a cached version)
- Note pricing tier, per-seat cost, annual vs monthly delta

**Data recording format**:
```
| Asset/Product | Live Price | Source | Fetched At | 24h Change |
|---|---|---|---|---|
| SYMBOL        | $XX.XX     | Stooq  | 2026-04-30 | -1.2%      |
```

**Checkpoint** ✅:
- [ ] Live price fetched for every candidate under analysis
- [ ] No document prices used; if live data unavailable, explicitly stated as "data unavailable"
- [ ] Fetch timestamp recorded (within past 4h for liquid assets)

**Failure modes**:
- ❌ Using prices from a previous analysis document
- ❌ "I know roughly what it costs" without fetching
- ❌ Fetching once and reusing data from an hour-old analysis as if still current

---

### Step 4 — Compare on Dimensions (Comparison Matrix)

**Purpose**: Make tradeoffs explicit and scorable rather than gestalt / gut feel.

**Required inputs**:
- Filtered candidates from Step 2
- Live data from Step 3

**Actions**:
1. Define 4–8 scoring dimensions relevant to this decision type:
   - Investments: upside potential, downside risk, liquidity, catalyst timeline, valuation (PE/DCF)
   - Purchases: price/performance, durability, ecosystem, total cost of ownership
   - Technology: capability fit, integration cost, vendor stability, migration cost, licensing
2. Assign weights to dimensions (must sum to 100%)
3. Score each candidate per dimension (1–5 scale)
4. Calculate weighted score
5. Flag any dimension where one option is significantly better — this often reveals the real decision

**Comparison matrix template**:
```
| Dimension     | Weight | Option A | Option B | Option C |
|---|---|---|---|---|
| Dim 1         | 30%    | 4 (1.2)  | 3 (0.9)  | 5 (1.5)  |
| Dim 2         | 25%    | 3 (0.75) | 5 (1.25) | 2 (0.5)  |
| Dim 3         | 20%    | 5 (1.0)  | 4 (0.8)  | 3 (0.6)  |
| Dim 4         | 15%    | 2 (0.3)  | 3 (0.45) | 4 (0.6)  |
| Dim 5         | 10%    | 4 (0.4)  | 2 (0.2)  | 3 (0.3)  |
| **Total**     | 100%   | **3.65** | **3.60** | **3.50** |
```

**Checkpoint** ✅:
- [ ] ≥4 scoring dimensions defined
- [ ] Weights assigned and sum to 100%
- [ ] No option scores best on every dimension (if it does, you've gamed the dimensions)
- [ ] Live prices from Step 3 used in scoring, not cached numbers

**Failure modes**:
- ❌ Dimensions chosen to favor a pre-selected option
- ❌ All dimensions equally weighted (implies no priorities)
- ❌ One option wins on all dimensions — either dimensions are wrong or cherry-picked

---

## DECISION

### Step 5 — Apply Methodology

**Purpose**: Replace gut calls with transparent, reproducible reasoning.

**Investment methodology** (choose the most applicable):

| Method | Use when | Inputs needed |
|---|---|---|
| **PE ratio** | Established profitable companies | EPS (TTM), sector median PE |
| **DCF (range)** | Long-horizon growth companies | Revenue growth rate, margin trajectory, discount rate |
| **Technical levels** | Entry/exit timing | MA50, MA200, key support/resistance |
| **Catalyst analysis** | Event-driven positions | Upcoming earnings, product launches, regulatory decisions |

Show your numbers:
```
PE Analysis:
- Current PE: 22x
- Sector median PE: 18x
- Premium/discount: +22% premium
- Justification for premium (if any): [specific growth catalyst]
- Conclusion: 🟡 fairly valued to slightly expensive at current price
```

**Purchase methodology**:
- TCO = purchase price + maintenance + consumables + opportunity cost of capital, over 3 years
- Compare TCO, not just sticker price

**Technology / vendor methodology**:
- Weighted decision matrix (Step 4) + qualitative strategic fit
- Must include: integration cost estimate, switching cost estimate, vendor longevity assessment

**Checkpoint** ✅:
- [ ] Methodology explicitly named (not just "I think")
- [ ] Numbers shown, not just conclusions
- [ ] At least one downside or risk acknowledged for the top-scoring option
- [ ] Estimates labeled as estimates (not presented as exact)

---

### Step 6 — Plan B and Exit Conditions

**Purpose**: Define your exit *before* you're emotional about the position.

**For investments**:
```
Stop-loss: $XX.XX (entry − (entry × max_loss_pct))
Thesis invalidation trigger: [specific event that means the thesis is broken, e.g.,
  "revenue growth drops below 10% YoY", "product launch delayed >6 months"]
Exit on: stop-loss hit OR thesis invalidation trigger, whichever comes first
```

**For purchases**:
- Return window: X days / restocking fee: Y%
- Resale value estimate at 1 year / 3 years
- Break-even usage: if used fewer than X times, it wasn't worth it

**For tech/vendor**:
- Contract notice period and termination clauses
- Data export format and migration cost to alternative
- Acceptable performance minimum (SLA); below what threshold do you switch?

**Checkpoint** ✅:
- [ ] Stop-loss level (or equivalent exit threshold) defined as a number, not "if things go wrong"
- [ ] Thesis invalidation trigger defined separately from price (price alone is not a thesis)
- [ ] Exit conditions set BEFORE execution, not left for later

**Failure modes**:
- ❌ "I'll exit if it drops too much" (vague — "too much" expands as losses grow)
- ❌ No thesis trigger defined — you'll find reasons to hold through any loss
- ❌ "I can always average down" — this is a rationalization, not an exit plan

---

### Step 7 — Make Decision + Document Rationale

**Purpose**: Commit with a clear record so future-you can judge whether the reasoning was sound.

**Decision record template**:
```markdown
## Decision Record — [Title] — [Date]

**Decision**: [Chosen option]
**Date**: YYYY-MM-DD HH:MM (timezone)
**Decision-maker**: [Role / name optional]

### Why This Option
[1–2 paragraphs: what the matrix showed, what the methodology confirmed,
 what specific features/metrics made this the right choice given constraints]

### Why Not the Alternatives
- Option B: [specific reason it lost — be honest, not dismissive]
- Option C: [specific reason it lost]

### Key Assumptions
- [Assumption 1 that must hold for this to work out]
- [Assumption 2]

### Known Risks
- 🔴 [Major risk and mitigation]
- 🟡 [Moderate risk]

### Exit Conditions (from Step 6)
- Stop-loss / return threshold: [value]
- Thesis invalidation trigger: [specific event]

### Review Date
- Next check-in: [date]
```

**Checkpoint** ✅:
- [ ] Chosen option stated clearly (not "leaning toward")
- [ ] Both "Why This" and "Why Not" documented
- [ ] Known risks include at least one 🔴
- [ ] Exit conditions from Step 6 copied in

---

## POST-DECISION

### Step 8 — Execute with Position Sizing

**Purpose**: Enter with a calculated size, not an emotional one.

**Investment position sizing**:
```
Max account risk per trade: R (e.g., 1% of portfolio)
Entry price: P_entry (from live data — Step 3)
Stop-loss: P_stop (from Step 6)
Risk per share: P_entry − P_stop

Position size (shares) = (Account value × R) ÷ (P_entry − P_stop)
Position size ($) = shares × P_entry
```

Example (do not use actual values — illustrative only):
```
Account: $10,000 | R: 1% = $100 risk
Entry: $50.00 | Stop: $47.00 | Risk/share: $3.00
Shares: $100 ÷ $3.00 = 33 shares
Position size: 33 × $50 = $1,650 (16.5% of account)
```

**General position sizing principles** (not rules — context-dependent):
- First entry in a new position: smaller size, scale in after thesis confirms
- High-conviction, liquid assets: can size higher (within personal risk tolerance)
- Illiquid or high-volatility assets: size down proportionally
- Never size so large that a stop-loss hit would cause you to change behavior (panic, revenge trade)

**Checkpoint** ✅:
- [ ] Position size calculated from live entry price, not estimated price
- [ ] Max loss in $ calculated and accepted before executing
- [ ] Single position does not exceed personal concentration limit

---

### Step 9 — Track P/L Daily

**Purpose**: Catch thesis-breaking events early. Weekly tracking is too slow for liquid assets.

**Daily P/L log format**:
```markdown
## P/L Log — [Asset/Decision name]

| Date       | Entry $ | Current $ | Unrealized P/L | Unrealized P/L % | Notes              |
|---|---|---|---|---|---|
| 2026-05-01 | $50.00  | $51.20    | +$39.60        | +2.4%            | Earnings beat     |
| 2026-05-02 | $50.00  | $49.80    | -$6.60         | -0.4%            | Market sold off   |
| 2026-05-03 | $50.00  | $47.10    | -$95.70        | -5.8%            | ⚠️ Near stop-loss |
```

**Thesis check (weekly, in the Notes column)**:
- Is the original thesis still intact?
- Any new information that would change the decision?
- Stop-loss still appropriate, or has thesis strengthened / weakened?

**For non-investment decisions**:
- Track the KPIs defined as success criteria in Step 7
- Weekly cadence acceptable for purchases or vendor decisions

**Checkpoint** ✅:
- [ ] P/L log updated at least daily for active positions
- [ ] Current price fetched live (not estimated) for each log entry
- [ ] Stop-loss level visible in the log

---

### Step 10 — Review and Adjust

**Purpose**: Learn from outcomes and kill bad positions before they become catastrophic.

**Weekly review**:
1. Is the thesis still intact? (Check the thesis invalidation trigger from Step 6)
2. Did price hit stop-loss? → Exit. Do not negotiate with rules you set when you were rational.
3. Any new information materially changes the analysis? → Update the decision record (Step 7).
4. Is the position sized correctly for current volatility?

**Monthly review**:
1. Compare actual outcome vs projection in Step 7
2. If diverging: why? Was the analysis wrong, or are the facts changing?
3. Decide: hold / adjust / exit with documented rationale

**Decision postmortem template** (after exit):
```markdown
## Postmortem — [Decision title] — [Exit date]

**Entry**: [price / date] | **Exit**: [price / date] | **P/L**: [$ and %]
**Thesis at entry**: [1-sentence summary]
**What actually happened**: [1–2 sentences]
**What I got right**: 
**What I got wrong**:
**Would I make the same decision again with the same information?** [Yes/No/Partially]
**What to do differently next time**:
```

**Checkpoint** ✅:
- [ ] Weekly thesis check completed for all active positions
- [ ] No position held past stop-loss without documented re-evaluation
- [ ] Postmortem completed within 1 week of exit (win or loss)

---

## Quick Reference Card

```
BEFORE YOU COMMIT: Have you...
  [ ] Listed ≥3 alternatives?
  [ ] Set hard constraints BEFORE scoring?
  [ ] Fetched LIVE prices (not document prices)?
  [ ] Built a comparison matrix?
  [ ] Named your methodology (PE / DCF / weighted matrix)?
  [ ] Defined a stop-loss or exit threshold?
  [ ] Written a decision record with risks?
  [ ] Calculated position size from live price?

AFTER YOU COMMIT:
  [ ] Daily P/L log running?
  [ ] Weekly thesis check scheduled?
  [ ] Postmortem planned for exit date?
```

---

_Part of `build-protocol-decision` skill · 2026-04-30_
