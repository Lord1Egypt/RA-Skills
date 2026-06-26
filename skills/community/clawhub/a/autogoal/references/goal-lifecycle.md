# Goal Lifecycle Patterns

## Pattern 1: Periodic-Review Goal

**Best for**: Ongoing goals like "improve trading win rate" or "keep server uptime above 99.9%"

**How it works**:
1. Initial intake → creates goal record + sets up a cron job
2. Cron job fires every N hours/days with the goal check-in prompt
3. Each run evaluates progress, takes action, logs it, and adapts strategy
4. Goal stays active until explicitly closed

**When to set `everyMs`:**
| Goal type | Suggested interval | Reason |
|-----------|-------------------|--------|
| Trading profit | 2-6h | Market moves hourly, but too-frequent checks waste tokens |
| Server uptime | 12-24h | Already monitored via Nagios; goal checks overall trend |
| Learning project | 24-72h | Needs human cycles between checks |
| Habit building | 24h | Daily accountability |

## Pattern 2: One-Shot Goal

**Best for**: Build/achieve something finite — "migrate Caddy to Traefik"

**How it works**:
1. Initial intake → creates goal record, NO cron job
2. Work is done conversationally through normal agent interaction
3. Goal is closed when work completes

## Pattern 3: Alert-Decay Goal

**Best for**: Goals that should escalate if stale — "fix the leaking faucet" or "update SSL certs"

**How it works**:
1. Initial intake → creates goal record + cron job at slow cadence (24h)
2. Each check evaluates: is there forward progress?
3. After N check-ins with zero progress → escalate (notify user more urgently)
4. After 2N zero-progress check-ins → suggest closing or abandoning

## Pattern 4: Parameter-Tuning Goal

**Best for**: "Make profit on Kalshi" or "Improve Alpaca win rate"

**How it works**:
1. Initial intake → creates goal with `metrics` tracking current values
2. Cron job runs the domain pipeline (e.g. Kalshi auto-trader)
3. After each run, compares results to previous metrics
4. If trending negative → adapt strategy (tighten edge, change sizing)
5. If trending positive → keep strategy, look for optimization
6. Logs each parameter change as a strategy update

**Key references for domain-specific parameter tuning:**
- Kalshi: `automation/trading/kalshi/data/trade_policy.json`
- Alpaca: `/home/brandon/alpaca-trading/`

## Strategy Adaptation Heuristics

When a goal is not making progress, try these in order:

1. **Narrow scope** — focus on one sub-goal instead of the whole thing
2. **Change cadence** — shorter check intervals for tighter feedback
3. **Change approach** — different tools, different API, different method
4. **Ask the user** — "I've tried X and Y, neither improved Z. What else should I try?"
5. **Pause the goal** — set status to paused if user is unresponsive or blockers exist

## Progress Signals

| Signal | Meaning |
|--------|---------|
| Metric improves over 2+ checks | Strategy is working, keep going |
| Metric flat for 3+ checks | Strategy may need tuning |
| Metric degrades for 2+ checks | Something is wrong, adapt immediately |
| Cannot take action (no tools/permissions) | Escalate to user |
| Goal achieved | Close it, celebrate briefly |
