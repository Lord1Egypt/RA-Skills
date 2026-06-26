# Action Audit Guide

How to measure whether your agents are actually doing things.

## The Action Ratio

For each agent session, score it:

```
Action Ratio = (external actions taken) / (total output sections)
```

- **> 0.5** — Healthy. Agent is doing more than talking.
- **0.2 - 0.5** — Drifting. Research is crowding out action. Tighten the prompt.
- **< 0.2** — Report mode. Restructure the prompt immediately.

## Red Flags

Watch for these in agent output:

### Planning Language (immediate red flag)
- "I recommend we..."
- "Next steps would be to..."
- "We should consider..."
- "I'll create this in the next session..."
- "A good approach would be..."
- "Here's a strategy for..."

**Fix:** Add to prompt: `DO NOT PLAN. EXECUTE. If you write "I will..." or "we should...", STOP and DO IT instead.`

### Research Without Action
Agent spends 80% of its session researching, produces detailed findings, then ends without doing anything with them.

**Fix:** Structure prompt as "Research X, then [action] based on findings." Never let research be the final step.

### Invisible Output
Agent says "I posted" or "I sent the email" but there's no URL, post ID, or confirmation in the logs.

**Fix:** Require proof for every action: "Log all actions with URLs, IDs, or response codes to [file]."

### Comfortable Defaults
Agent consistently picks the easiest action (e.g., always writes a blog draft, never sends cold emails).

**Fix:** Rotate required actions. Use "MANDATORY" labels for harder actions. Or require a mix: "at least 1 email AND 1 community post."

### Session Inflation
Agent writes 500 lines but only 10 lines are actual action. The rest is analysis, context-setting, and recommendations.

**Fix:** Set explicit output structure. "Actions section first, then brief notes. Actions must be at least 50% of output."

## Quick Audit Checklist

Run this weekly across all agent sessions:

```
For each shift/cron session this week:
  1. Did it produce at least 1 external action? [Y/N]
  2. Is there proof (URL/ID/confirmation)? [Y/N]
  3. Was the action quality acceptable? [Y/N]
  4. Did research serve the action (not replace it)? [Y/N]

Score: count of Y / total checks
Target: > 75%
```

## When NOT to Audit for Action

Some sessions are legitimately report-only:

- **Security audits** — the report IS the deliverable
- **Weekly analyst reviews** — synthesis for human decision-making
- **System health checks** — monitoring IS the action
- **Human-requested analysis** — when a human explicitly asks for a report

The test: did a human request this analysis, or did the agent default to it because it's easier than doing something?

## Measuring Impact Over Time

Track these weekly:

| Metric | What it measures |
|---|---|
| External actions per shift | Volume of output |
| Unique platforms touched | Distribution breadth |
| Actions with proof (%) | Accountability |
| Report-only sessions (%) | Planning drift |
| New leads/followers/submissions | Actual business impact |

The ultimate measure: **are the actions producing results?** 100 tweets that nobody sees may technically be "actions" but they're not effective. Pair action audits with outcome tracking.
