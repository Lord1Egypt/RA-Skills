---
name: covered-call-strategy
description: "Covered call portfolio strategy analysis and optimization. Use when the user asks about covered call (备兑认购期权) investment strategy, Roll Up/Roll Down decisions, option strike price selection, portfolio structure optimization, or any questions about combining stock holdings with short call options. Triggers on: 备兑call、备兑权证、covered call、Roll Up、Roll Down、行权价选择、期权组合策略、call option strategy、期权到期决策."
---

# Covered Call Portfolio Strategy

Analyze and optimize covered call (备兑认购期权) portfolio strategies with full upside/downside scenario modeling.

## Core Framework

### First Principle: Covered Call Caps Upside, Does NOT Protect Downside

This is the most common and costly misconception:

| Misconception | Reality |
|--------------|---------|
| "Short call at $580 provides downside protection" | ❌ The call only caps upside at $580. If stock drops to $400, the call expires worthless — stock falls freely |
| "Higher strike = more protection" | ❌ Strike price only determines where upside is capped, not where downside is stopped |
| "Rolling up protects my gains" | ❌ Rolling up costs premium, reducing downside cushion. It releases upside but reduces the premium buffer |

**The only downside protection in a covered call comes from the premium received.** Period.

### Key Metrics

| Metric | Formula | Meaning |
|--------|---------|---------|
| **Net Premium** | Total premium received - Roll/close costs | Downside cushion (the only one) |
| **Effective Sell Price** | Strike price + (Net Premium per share) | What you actually get if assigned |
| **Upside Cap** | Strike price | Maximum stock sell price before premium |
| **Downside Break-even** | Stock cost basis - Net Premium per share | Price where total P&L = 0 |

## Analysis Workflow

When user asks for covered call strategy analysis, follow this sequence:

### Step 1: Map Current Position

Extract and tabulate:

```
Stock Holdings:
| Batch | Shares | Cost Basis | Current Price |

Option Positions:
| Call | Direction | Strike | Expiry | Premium Received | Current Price |
```

Calculate:
- Total shares vs total short calls (must be 1:1 covered)
- Net premium per share
- Current P&L (stock + options)

### Step 2: Define Strategy Options

Common strategies (always include "Do Nothing" as baseline):

| Strategy | Description | When to Consider |
|----------|------------|-----------------|
| **Do Nothing** | Hold current positions to expiry | Baseline comparison |
| **Roll Up** | Buy back current call, sell higher strike | Stock has risen, want to release upside |
| **Roll Down** | Buy back current call, sell lower strike | Stock has dropped, want more premium |
| **Close Position** | Buy back call, hold stock naked | Want full upside flexibility |
| **Mixed Roll** | Roll some calls, keep others | Diversified approach |

### Step 3: Calculate Net Premium for Each Strategy

This is the critical calculation most people get wrong:

```
Net Premium = (All premiums received historically)
            - (Costs to buy back/roll current positions)
            + (Premiums from new positions sold)
```

**Roll Up reduces net premium.** This is the true cost — not the debit paid, but the reduction in downside cushion.

### Step 4: Build Scenario Matrix

For each strategy, calculate total P&L at key price points:

**Required price points:**
1. Deep downside (-30% from current)
2. Moderate downside (-15%)
3. Current price
4. Each strike price
5. Moderate upside (+15%)
6. Significant upside (+30%)

**For each cell:**
```
Total P&L = Stock P&L + Net Premium + Assignment Income (if ITM)
```

Where:
- Stock P&L = (Sell Price - Cost Basis) × Shares
- If call ITM at expiry: Sell Price = Strike Price (for assigned shares)
- If call OTM at expiry: Sell Price = Market Price (for unassigned shares)

### Step 5: Identify Optimal Strategy by Outlook

| Market Outlook | Recommended Strategy | Reasoning |
|---------------|---------------------|-----------|
| Strongly bearish | Do Nothing or Roll Down | Preserve maximum premium cushion |
| Slightly bearish | Do Nothing | Premium cushion > upside release value |
| Neutral (near strike) | Do Nothing or Partial Roll | Premium cushion roughly equals upside release |
| Slightly bullish | Roll 1 call (partial) | Release some upside, keep some cushion |
| Strongly bullish | Full Roll Up or Close | Upside release value > premium cushion loss |

### Step 6: Present Decision Framework

Never recommend a single strategy. Present the trade-off:

**Roll Up = Spending premium cushion to buy upside space**

Quantify this trade explicitly:
- Cost in premium cushion: $X
- Upside space released: $Y per share
- Break-even stock price where Roll Up becomes superior: $Z

## Common Pitfalls (Lessons Learned)

These are real errors made during live analysis — do not repeat:

### Pitfall 1: Mistaking Cap for Floor
> "The $580 call provides downside protection at $580"

**WRONG.** The $580 call means if stock > $580, your shares get called away at $580. If stock < $580, the call expires worthless and you bear full downside.

### Pitfall 2: Ignoring Net Premium Impact
> "Roll Up costs $9,600 but releases $24,000 upside"

The $9,600 reduces your net premium cushion. In downside scenarios, you're $9,600 worse off than doing nothing. The "released upside" only materializes if the stock actually rises.

### Pitfall 3: Forgetting Assignment Mechanics
> "If stock drops to $400, the $580 call gets assigned"

**WRONG.** Call buyers only exercise when it's profitable — i.e., when stock price > strike. Deep ITM calls get assigned. Deep OTM calls expire worthless.

### Pitfall 4: Asymmetric Position Sizing
> "Roll 1 call to $820, keep 1 at $580"

Check: after the roll, how many shares are free? The answer is always zero in a fully covered position. Each short call covers exactly 100 shares. There are no "free shares" unless you deliberately close a call without selling a new one.

### Pitfall 5: Static Analysis Only
Covered call decisions are path-dependent. Today's optimal strategy may need adjustment in 2 months. Always specify:
- **Monitoring triggers**: At what stock price should the strategy be re-evaluated?
- **Next action**: What to do if the stock reaches the new strike?

## Advanced Scenarios

For complex multi-call positions with different strikes and cost bases, see [references/multi-strike-model.md](references/multi-strike-model.md).

For Roll Up/Roll Down decision frameworks with quantitative thresholds, see [references/roll-decision.md](references/roll-decision.md).
