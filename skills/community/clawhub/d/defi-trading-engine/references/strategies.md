# Trading Strategies

Four proven strategy templates for systematic DeFi trading. Each includes entry/exit rules, position sizing, timeframe, and risk parameters.

---

## 1. DCA (Dollar-Cost Averaging)

**Philosophy:** Remove emotion, accumulate quality assets systematically.

### Entry Rules
- **Trigger:** Time-based (daily, weekly, or bi-weekly)
- **Selection:** Pre-defined asset list (BTC, ETH, SOL, etc.)
- **No price discrimination:** Buy regardless of market conditions

### Exit Rules
- **None** (long-term hold strategy)
- Optional: Sell when target portfolio allocation exceeded (e.g., if ETH grows to >40% of portfolio, trim to 30%)

### Position Sizing
- Fixed USD amount per interval
- Example: $40 every Monday at 9:00 AM UTC

### Timeframe
- Weekly or bi-weekly is optimal for retail (minimizes fees)
- Daily for larger portfolios or high-conviction periods

### Risk Parameters
```json
{
  "strategy": "dca",
  "schedule": "weekly",
  "day_of_week": "monday",
  "time_utc": "09:00",
  "amount_per_buy": 40,
  "assets": ["BTC", "ETH", "SOL"],
  "allocation": {
    "BTC": 0.5,
    "ETH": 0.3,
    "SOL": 0.2
  }
}
```

### Pros
- ✅ Eliminates timing stress
- ✅ Proven over long term
- ✅ Works in any market (bull/bear/sideways)

### Cons
- ❌ No downside protection (keeps buying in crashes)
- ❌ Slow in bull markets (misses explosive gains)
- ❌ Requires discipline (easy to skip when scared)

### Best For
- Long-term believers
- Hands-off investors
- Accumulation phase (building a position over 6-24 months)

---

## 2. Momentum Swing

**Philosophy:** Ride short-term trends with tight risk management.

### Entry Rules
1. **Volume spike:** 24h volume > 1.5x the 7-day average
2. **Price momentum:** +3% or more in last 1 hour
3. **Liquidity check:** Minimum $100K liquidity (avoid thin markets)
4. **Trending status:** On CoinGecko or DexScreener trending list

All 4 conditions must be met.

### Exit Rules
- **Take profit:** +4% gain (lock in quick wins)
- **Stop loss:** -8% loss (cut losers fast)
- **Trailing stop (optional):** Once +6%, trail stop at -3% from peak
- **Time-based exit:** If no movement within 4 hours, exit at break-even or small loss

### Position Sizing
- $40 per trade (or 4% of portfolio, whichever is smaller)
- Max 5 concurrent positions

### Timeframe
- **Scan interval:** Every 15-30 minutes
- **Hold time:** Minutes to hours (not days)
- **Best hours:** High volatility periods (14:00-22:00 UTC)

### Risk Parameters
```json
{
  "strategy": "momentum_swing",
  "entry_conditions": {
    "volume_spike_ratio": 1.5,
    "price_change_1h_pct": 3.0,
    "min_liquidity_usd": 100000,
    "must_be_trending": true
  },
  "exit_conditions": {
    "take_profit_pct": 4,
    "stop_loss_pct": 8,
    "trailing_stop_pct": 3,
    "time_based_exit_hours": 4
  },
  "position_size_usd": 40,
  "max_positions": 5
}
```

### Pros
- ✅ High win rate (catch obvious pumps)
- ✅ Quick feedback loop (know within hours if trade worked)
- ✅ Tight risk control

### Cons
- ❌ Requires active monitoring (or automation)
- ❌ High false signals during sideways markets
- ❌ Can get chopped in volatile conditions

### Best For
- Active traders
- Automation-friendly (scan → execute → monitor)
- Bull markets (trends are clearer)

---

## 3. Mean Reversion

**Philosophy:** Buy fear, sell greed. Markets overreact.

### Entry Rules
1. **Oversold signal:** Price down >10% in 24h
2. **Quality filter:** Must be in top 200 by market cap (avoid shitcoins)
3. **Volume check:** 24h volume > $500K (avoid dead coins)
4. **Fundamental strength:** Not a scam/rug (check social, dev activity)
5. **Support level:** Bouncing off known support (if charting available)

### Exit Rules
- **Take profit:** +6-8% from entry (quick bounce)
- **Extended TP:** If momentum continues, hold to +12% with trailing stop
- **Stop loss:** -6% (tighter than momentum because we're catching a falling knife)
- **Time-based:** If no recovery within 48 hours, exit at current price

### Position Sizing
- $40 per trade
- Max 3 concurrent positions (mean reversion can take time)

### Timeframe
- **Scan interval:** Every 1-4 hours
- **Hold time:** Hours to days (wait for the bounce)
- **Best markets:** Sideways or early recovery from crash

### Risk Parameters
```json
{
  "strategy": "mean_reversion",
  "entry_conditions": {
    "price_drop_24h_pct": 10,
    "min_market_cap_rank": 200,
    "min_volume_24h_usd": 500000,
    "fundamental_check": true
  },
  "exit_conditions": {
    "take_profit_pct": 8,
    "extended_tp_pct": 12,
    "stop_loss_pct": 6,
    "time_based_exit_hours": 48
  },
  "position_size_usd": 40,
  "max_positions": 3
}
```

### Pros
- ✅ Buy when others are scared (contrarian edge)
- ✅ Good risk/reward (catch 10-20% bounces)
- ✅ Lower competition (most bots chase momentum, not reversals)

### Cons
- ❌ Catching falling knives (can keep dropping)
- ❌ Requires patience (bounces take time)
- ❌ Hard to distinguish "dip" from "collapse"

### Best For
- Patient traders
- Bear/sideways markets
- Quality coins with strong fundamentals

---

## 4. Asymmetric Bets

**Philosophy:** Small positions on high-upside, high-conviction opportunities. Risk $40 to make $400+.

### Entry Rules
1. **New listing or early-stage token:** <30 days since launch
2. **Strong narrative:** Fits current meta (e.g., AI agents, RWA, gaming)
3. **Social momentum:** Rapid growth in followers, mentions, community
4. **Team credibility:** Doxxed team, prior successful projects, or strong backers
5. **Liquidity threshold:** At least $50K liquidity (enough to enter/exit)
6. **Personal conviction:** You actually believe in the project (not just chasing hype)

All criteria must be met. This is NOT degen gambling—it's calculated risk on asymmetric upside.

### Exit Rules
- **Ladder out:** Sell 50% at 5x, 25% at 10x, let 25% ride
- **Stop loss:** -50% (you're risking half your position for 10x upside)
- **Time-based:** If no movement in 30 days, reevaluate (hold/sell)
- **Narrative shift:** If project pivots or team changes, exit immediately

### Position Sizing
- **$40 per bet** (small enough to lose, big enough to matter if it works)
- Max 3 concurrent bets (diversify the asymmetry)

### Timeframe
- **Hold time:** Weeks to months (not days)
- **Review interval:** Weekly (check narrative, team, social signals)
- **Best timing:** Early in a bull cycle (when new narratives emerge)

### Risk Parameters
```json
{
  "strategy": "asymmetric_bets",
  "entry_conditions": {
    "max_days_since_launch": 30,
    "narrative_strength": "high",
    "social_growth_rate": "rapid",
    "team_credibility": "verified",
    "min_liquidity_usd": 50000,
    "personal_conviction": true
  },
  "exit_conditions": {
    "sell_50_pct_at": "5x",
    "sell_25_pct_at": "10x",
    "let_ride_pct": 25,
    "stop_loss_pct": 50,
    "reevaluate_after_days": 30
  },
  "position_size_usd": 40,
  "max_positions": 3
}
```

### Pros
- ✅ Huge upside (10x-100x possible)
- ✅ Limited downside (only risk $40 per bet)
- ✅ Aligns with how VCs think (portfolio of small bets)
- ✅ Fun and engaging (following early projects)

### Cons
- ❌ Most bets will fail (win rate <30%)
- ❌ Requires deep research (can't automate fully)
- ❌ Emotional attachment (easy to hold losers too long)
- ❌ Illiquidity risk (hard to exit if project dies)

### Best For
- High-risk tolerance
- Researchers and narrative hunters
- Early-stage crypto enthusiasts
- Portfolio diversification (complement safer strategies)

---

## Combining Strategies

**Recommended Portfolio Allocation:**

- **50%:** DCA (core long-term holdings: BTC, ETH, SOL)
- **30%:** Momentum Swing (active trading, short-term gains)
- **15%:** Mean Reversion (opportunistic dip-buying)
- **5%:** Asymmetric Bets (lottery tickets with research)

This balances:
- **Stability** (DCA)
- **Cash flow** (Momentum)
- **Value hunting** (Mean Reversion)
- **Upside optionality** (Asymmetric)

---

## Backtesting Notes

Before running any strategy live:

1. **Paper trade for 2 weeks** (track trades without real money)
2. **Backtest on historical data** (if possible, test on last 3-6 months)
3. **Adjust parameters** based on results (tighten filters if win rate <50%)
4. **Start small** (half position size for first 10 trades)
5. **Review weekly** (run daily-review.py and adjust)

---

## Strategy Selection Flowchart

```
Are you comfortable with active management?
├─ NO → Use DCA (weekly buys, hands-off)
└─ YES ↓

Do you have time to monitor trades multiple times per day?
├─ NO → Use Mean Reversion (check once per day)
└─ YES ↓

Is the market trending strongly (bull or bear)?
├─ BULL → Use Momentum Swing (ride the trend)
├─ BEAR/SIDEWAYS → Use Mean Reversion (buy dips)
└─ UNCERTAIN → Combine both (50/50 allocation)

Do you enjoy deep research and high-risk/high-reward?
└─ YES → Add Asymmetric Bets (5-10% of portfolio)
```

---

**Last Updated:** 2026-03-13
**Version:** 1.0
