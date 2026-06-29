# Investment Playbook Template

> Generic template for personal investment management.
> Anonymized — fill in your own values. Do not copy-paste without adapting to your situation.
> Review and update quarterly.

---

## Section 1 — Account & Risk Parameters

```yaml
# Fill in your actual values. These are INPUTS, not defaults.
account:
  total_capital:          "[your total investable capital]"
  liquid_reserve:         "[minimum cash to keep uninvested — suggest ≥3 months expenses]"
  investable_capital:     "[total_capital minus liquid_reserve]"

risk_controls:
  max_risk_per_trade:     "[% of portfolio to risk on a single trade — common range: 0.5%–2%]"
  max_single_position:    "[% of portfolio in one position — common range: 5%–20%]"
  max_sector_exposure:    "[% of portfolio in one sector — suggest ≤30%]"
  max_total_drawdown:     "[% loss that triggers full portfolio review — e.g., 20%]"
  cash_floor:             "[% to keep in cash at all times — e.g., 10%]"
```

**Hard risk line**: If total portfolio drawdown exceeds `max_total_drawdown`, stop all new entries and review every open position before adding anything.

---

## Section 2 — Performance Targets

> Targets should be realistic relative to your strategy, not aspirational numbers.
> A target you never hit is not a target — it's wishful thinking.

```yaml
targets:
  annual_return:          "[realistic target — benchmark against index for context]"
  max_annual_drawdown:    "[acceptable loss in a bad year]"
  win_rate:               "[not the primary metric — size matters more than win rate]"
  avg_risk_reward:        "[target: ≥1.5:1 on average — meaning average win ≥ 1.5x average loss]"
```

**Daily P/L target**: Not recommended. Daily targets create pressure to trade when there is no edge. Track daily P/L as a record, not as a goal.

**Weekly / monthly check-in**: Compare cumulative P/L vs plan. If >15% behind plan by midyear, review strategy — do not increase risk to catch up (this is how accounts blow up).

---

## Section 3 — Investable Instruments (Risk-tiered)

Group your instruments by risk level. This prevents accidentally treating a speculative position as if it were a low-risk allocation.

### Tier 1 — Lower Volatility (Core holdings)
- Broad market index funds / ETFs
- Investment-grade bonds
- Dividend-focused equity
- Target allocation: [X% of investable capital]
- Max single position: [Y% of total portfolio]

### Tier 2 — Growth / Moderate Risk
- Individual growth stocks (established sector leaders)
- Sector ETFs with specific thesis
- REITs
- Target allocation: [X% of investable capital]
- Max single position: [Y% of total portfolio]

### Tier 3 — Speculative / High Risk
- Small-cap individual stocks
- Cryptocurrencies
- Options (directional)
- Emerging market single-country exposure
- Target allocation: [X% of investable capital — keep small, e.g., ≤15%]
- Max single position: [Y% of total portfolio — strict, e.g., ≤5%]
- **Rule**: Only money you can afford to lose completely goes here

### Tier 4 — Do Not Touch
- Assets or strategies outside your defined competency
- Any instrument where you cannot explain the mechanism in one sentence
- Any instrument where exit may be illiquid or restricted

---

## Section 4 — Position Sizing Rules

**Formula** (from `decision-workflow.md`, Step 8):
```
Risk per trade ($) = Total portfolio × max_risk_per_trade (%)
Risk per share ($) = Entry price − Stop-loss price
Position size (shares) = Risk per trade ÷ Risk per share
Position size ($) = Shares × Entry price
```

**Scale-in protocol** (optional, for high-conviction ideas):
- Initial entry: 50% of target position at market
- Add: 25% more if thesis confirms within [X days/weeks]
- Add: final 25% only if thesis is clearly working
- Never add to a losing position unless you have a documented re-evaluation that changes the thesis

**Scale-out protocol** (profit-taking, optional):
- Sell [X%] at [target level 1]
- Sell [Y%] at [target level 2]
- Trail remaining with stop-loss at breakeven+

---

## Section 5 — Stop-Loss Rules (Hard)

**Definition**: A stop-loss is the price at which you exit regardless of how you feel about the position.

Rules:
1. Every position opened gets a stop-loss defined at entry. No exceptions.
2. Stop-loss is set based on chart structure or maximum acceptable loss — whichever is tighter.
3. Stop-loss can only be moved in the direction of the trade (up for longs, down for shorts). Never move it against the trade to "give it more room."
4. If stop-loss is hit: exit. Do not renegotiate with yourself. The version of you that set the stop-loss was more rational than the version watching it get hit.
5. After a stop-loss exit: 24-hour cooldown before re-entering the same ticker (prevent emotional re-entry).

**Thesis invalidation trigger** (separate from price):
- Define the specific event or data point that would mean your thesis is wrong
- If this trigger fires: exit immediately, regardless of price
- Examples: "revenue misses >15%", "regulatory approval denied", "key executive departure"

---

## Section 6 — Profit-Taking Strategy

> Not every exit is a stop-loss. Define your upside exits too.

**Target levels**: Set at least one profit target at entry. Without one, you will either exit too early (fear) or too late (greed).

**Trailing stop option**:
- Once position is [X%] profitable, move stop to breakeven
- Once position is [Y%] profitable, trail stop at [Z% below recent high]

**Time-based exit option**:
- If thesis requires a catalyst by [date] and catalyst doesn't materialize: exit regardless of price
- Example: "I expect earnings beat by Q3 — if it doesn't happen, thesis is wrong"

**"Let winners run" vs "take profits" trade-off**:
- Both can be right depending on strategy
- Chose one approach per position at entry; don't switch mid-trade based on how you feel

---

## Section 7 — Daily P/L Record Format

```markdown
## Daily P/L — [Month YYYY]

| Date       | Ticker | Shares | Entry  | Current | Day P/L ($) | Cum P/L ($) | Notes                |
|---|---|---|---|---|---|---|---|
| 2026-05-01 | XYZ    | 100    | $50.00 | $51.20  | +$120       | +$120       | Earnings beat        |
| 2026-05-02 | XYZ    | 100    | $50.00 | $49.80  | -$140       | -$20        | Market pullback      |
| 2026-05-03 | XYZ    | 100    | $50.00 | $47.10  | -$270       | -$290       | ⚠️ 4% from stop-loss |
| 2026-05-04 | XYZ    |  —     | $50.00 | —       | —           | —           | 🔴 Exited at stop    |

Monthly total: -$290 | Open positions P/L: $0 (closed) | Cash deployed: [X%]
```

**Notes column protocol**:
- Normal: brief market context
- ⚠️ Within 5% of stop-loss: add warning
- 🔴 Stop hit: log exit price and reason
- 💡 Thesis update: note any new information

**Current price source**: Must be fetched live at time of log entry. Do not estimate.

---

## Section 8 — Weekly Review Format

**Every [day of week], before market open** (or after close, consistent timing):

```markdown
## Weekly Review — Week of [YYYY-MM-DD]

### Open Positions
| Ticker | Entry | Current | P/L % | Thesis intact? | Action |
|---|---|---|---|---|---|
| XYZ | $50.00 | $52.30 | +4.6% | ✅ Yes | Hold |
| ABC | $120.00 | $114.50 | -4.6% | ⚠️ Weakening | Watch |

### Thesis Check (for each position)
- [Ticker]: [One-sentence thesis] — Still intact because [reason] / Weakening because [reason]

### Closed This Week
| Ticker | Entry | Exit | P/L $ | P/L % | Reason |
|---|---|---|---|---|---|

### Lessons / Observations
-

### Next Week Plan
- Watching: [tickers / events on radar]
- Not planning to open new positions unless: [specific criteria]
```

---

## Section 9 — Monthly Rebalancing Protocol

**End of each month**:

1. **Performance review**:
   - Actual P/L vs target (Section 2)
   - Win rate and avg risk-reward for closed trades
   - Biggest winner and biggest loser — what can you learn from each?

2. **Portfolio composition check**:
   - Current allocation by tier (Section 3) vs target
   - Any single position exceeding max single position limit? → Trim to limit
   - Any sector exceeding max sector exposure? → Trim or hedge

3. **Strategy review**:
   - Is the strategy working? (Look at ≥3 months of data, not one month)
   - Any systematic bias? (Always selling too early? Always holding losers too long?)
   - Any instrument category consistently underperforming? → Reduce allocation

4. **Cash management**:
   - Current cash % vs cash floor (Section 1)
   - Replenish cash floor if below minimum before adding new positions

5. **Playbook update**:
   - Any rules that need updating based on experience?
   - Update this document and timestamp the change

```markdown
## Monthly Summary — [Month YYYY]

Realized P/L: $ [X] ([X%] of portfolio)
Unrealized P/L: $ [X] ([X%] of portfolio)
Total trades: [N] | Winners: [N] | Losers: [N] | Breakeven: [N]
Win rate: [X%] | Avg winner: $[X] | Avg loser: $[X] | Avg R:R: [X:1]
Cash deployed at month-end: [X%]
Portfolio vs benchmark (e.g., SPY): [outperformed / underperformed / in-line]

Key lessons this month:
1.
2.
3.
```

---

## Section 10 — Emergency Protocols

**If total drawdown hits `max_total_drawdown`**:
1. Stop all new position entries immediately
2. Review every open position: is each thesis still intact?
3. Close any position where thesis is weakest or where you "hope" rather than "expect"
4. Do not resume trading until you understand why the drawdown happened
5. If you cannot explain it in writing, you don't understand it

**If a single position losses exceed `max_single_position` equivalent**:
1. Check if stop-loss was skipped or moved — if so, this is a process failure, not just a loss
2. Exit immediately; do not average down to "fix" the average
3. Write a postmortem before considering re-entry

**If you feel compelled to deviate from this playbook**:
- Write down why before deviating, not after
- If you cannot write a coherent rationale, do not deviate
- Emotions ("I just feel like it's going higher") are not a rationale

---

_Template version: 1.0 · 2026-04-30_
_Part of `build-protocol-decision` skill_
_Review and update quarterly. Date your changes._
