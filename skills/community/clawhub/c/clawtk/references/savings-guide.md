# ClawTK Savings Guide

## Where Your Money Goes (Typical OpenClaw User)

| Cost Center | % of Bill | What Causes It |
|-------------|-----------|----------------|
| Heartbeats | 30-50% | Background checks sending full context every 30min |
| Session context | 20-30% | Messages + tool outputs accumulating in session |
| Tool outputs | 15-25% | Large CLI outputs (git log, test results, ls) stored in context |
| Model choice | 5-10% | Using Opus for simple tasks |
| Images | 3-5% | Screenshots at full resolution |

## How ClawTK Reduces Each Cost

### Free Tier (30-50% savings)

1. **Heartbeat isolation** cuts the biggest cost center by ~97%
2. **Heartbeat interval** reduces frequency by ~45%
3. **Cheap heartbeat model** reduces per-heartbeat cost by ~98%
4. **Context cap** prevents runaway accumulation
5. **Spend caps** prevent catastrophic overnight burns
6. **Retry loop detection** catches the "$47 overnight" problem

### Pro Tier (60-80% savings)

Everything in Free, plus:

7. **ClawTK Engine compression** reduces CLI output tokens by 60-90% — the single biggest lever for active users
8. **Semantic caching** skips the LLM entirely for repeated tasks
9. **Custom spend caps** tuned to your usage patterns

## Real Numbers

**Before ClawTK** (typical active user):
- Heartbeat cost: ~$3/hr (100K tokens x $0.003/1K x 10 heartbeats/day)
- Session cost: $15-30/day
- Monthly: $150-300

**After ClawTK Free**:
- Heartbeat cost: ~$0.03/hr (97% reduction)
- Session cost: $10-20/day
- Monthly: $50-100

**After ClawTK Pro**:
- Heartbeat cost: ~$0.03/hr
- Session cost: $5-10/day (ClawTK Engine compression)
- Monthly: $30-60
