# Agent Budget Controller — Usage Examples

## Example 1: Basic Setup

```bash
# Initialize
$ budget init
✅ Initialized budget tracking at /Users/you/.openclaw/budget
Next steps:
  1. Set limits: budget set --daily 3.00 --weekly 15.00 --monthly 50.00
  2. Log usage: budget log --agent my-agent --model gpt-4o --input-tokens 1000 --output-tokens 500
  3. Check status: budget status

# Set global limits
$ budget set --daily 5.00 --weekly 25.00 --monthly 100.00
✅ Set global daily limit: $5.00
✅ Set global weekly limit: $25.00
✅ Set global monthly limit: $100.00

# Set agent-specific limits
$ budget set --agent ubik-pm --daily 2.00
✅ Set daily limit for ubik-pm: $2.00

$ budget set --agent chloe-life --daily 1.50
✅ Set daily limit for chloe-life: $1.50
```

## Example 2: Logging Usage

```bash
# After calling Claude Sonnet
$ budget log \
  --agent ubik-pm \
  --model "claude-sonnet-4-5" \
  --input-tokens 5000 \
  --output-tokens 1500 \
  --verbose

✅ Logged usage for ubik-pm
   Model: claude-sonnet-4-5
   Tokens: 5000 in, 1500 out
   Cost: $0.0375

# After calling Gemini Flash (cheaper)
$ budget log \
  --agent ubik-pm \
  --model "gemini-2.5-flash" \
  --input-tokens 30000 \
  --output-tokens 3000 \
  --verbose

✅ Logged usage for ubik-pm
   Model: gemini-2.5-flash
   Tokens: 30000 in, 3000 out
   Cost: $0.0063
```

## Example 3: Checking Status

```bash
# Global status
$ budget status

📊 Agent Budget Status (2026-03-17)

Global Limits:
  Daily:   $1.82 / $5.00  (36.4%) ⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛
  Weekly:  $8.45 / $25.00 (33.8%) ⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛
  Monthly: $22.10 / $100.00 (22.1%) ⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛

By Agent:
  ubik-pm:     $0.95 today  (claude-sonnet: $0.80, gemini-flash: $0.15)
  chloe-life:  $0.62 today  (gpt-4o-mini: $0.62)
  openclaw-dev: $0.25 today (claude-sonnet: $0.25)

# Agent-specific status
$ budget status --agent ubik-pm

📊 Agent Budget Status (2026-03-17)

Agent: ubik-pm

  ✅ Daily: $0.95 / $2.00 (47.5%) ⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛
  ✅ Weekly: $4.20 / $14.00 (30.0%) ⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛
  ✅ Monthly: $12.50 / $56.00 (22.3%) ⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛
```

## Example 4: Alert Scenarios

### Warning (70-89%)
```bash
$ budget status --agent heavy-user

📊 Agent Budget Status (2026-03-17)

Agent: heavy-user

  ⚠️ Daily: $1.45 / $2.00 (72.5%) ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛
  ✅ Weekly: $5.20 / $15.00 (34.7%) ⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛
  ✅ Monthly: $18.40 / $60.00 (30.7%) ⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛
```

### Critical (90-99%)
```bash
$ budget status --agent expensive-agent

📊 Agent Budget Status (2026-03-17)

Agent: expensive-agent

  🔴 Daily: $1.85 / $2.00 (92.5%) ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛
  ⚠️ Weekly: $10.50 / $15.00 (70.0%) ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛
  ✅ Monthly: $38.20 / $100.00 (38.2%) ⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛
```

### Exceeded (≥100%)
```bash
$ budget status --agent runaway-agent

📊 Agent Budget Status (2026-03-17)

Agent: runaway-agent

  🚫 Daily: $2.15 / $2.00 (107.5%) ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
  🔴 Weekly: $13.80 / $15.00 (92.0%) ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛
  ⚠️ Weekly: $68.50 / $100.00 (68.5%) ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛
```

## Example 5: Budget Check (Scripting)

```bash
# Check if limits exceeded
$ budget check
Budget check for Global:
  daily: ✅ OK
  weekly: ✅ OK
  monthly: ✅ OK

$ echo $?
0  # Exit code 0 = OK

# Check specific agent
$ budget check --agent runaway-agent
Budget check for Agent 'runaway-agent':
  daily: 🚫 EXCEEDED
  weekly: 🚫 EXCEEDED
  monthly: ✅ OK

$ echo $?
1  # Exit code 1 = Exceeded
```

Use in scripts:
```bash
#!/bin/bash

# Pre-flight check
if ! budget check --agent my-agent; then
  echo "❌ Budget exceeded for my-agent"
  notify-send "Budget Alert" "Agent my-agent exceeded limits!"
  exit 1
fi

# Make LLM call...
```

## Example 6: Reports

### Daily Report
```bash
$ budget report --period day

📈 Budget Report: Today
Period: 2026-03-17 to 2026-03-17

Total Cost: $4.25

By Agent:
  ubik-pm: $1.80
  chloe-life: $1.45
  openclaw-dev: $1.00
```

### Agent-Specific Report
```bash
$ budget report --period week --agent ubik-pm

📈 Budget Report: This Week
Period: 2026-03-17 to 2026-03-17

Agent: ubik-pm
Total Cost: $8.45

By Model:
  claude-sonnet-4-5: $6.20
  gemini-2.5-flash: $1.80
  gpt-4o-mini: $0.45
```

## Example 7: Agent Management

```bash
# List all agents
$ budget agents

📋 Agents (5 total):

  chloe-life (limits set | active last 7d)
  openclaw-dev (limits set | active last 7d)
  test-agent (active last 7d)
  ubik-pm (limits set | active last 7d)
  old-agent (limits set)

# Show recent activity (30 days)
$ budget agents --days 30

📋 Agents (8 total):

  ubik-pm (limits set | active last 30d)
  chloe-life (limits set | active last 30d)
  ...
```

## Example 8: Custom Model Pricing

```bash
# View current pricing
$ budget pricing

💰 Model Pricing (per 1M tokens):

Model                     Input      Output
---------------------------------------------
claude-haiku-3.5          $0.80      $4.00
claude-opus-4             $15.00     $75.00
claude-sonnet-4-5         $3.00      $15.00
gemini-2.0-flash          $0.10      $0.40
gemini-2.5-flash          $0.15      $0.60
gemini-2.5-pro            $1.25      $10.00
gpt-4o                    $2.50      $10.00
gpt-4o-mini               $0.15      $0.60
o1                        $15.00     $60.00
o1-mini                   $3.00      $12.00

# Add custom model
$ budget pricing --update \
  --model my-custom-llm \
  --input-price 1.00 \
  --output-price 4.00

✅ Updated pricing for my-custom-llm
   Input: $1.00 per 1M tokens
   Output: $4.00 per 1M tokens

# Now shows in list
$ budget pricing | grep my-custom
my-custom-llm             $1.00      $4.00
```

## Example 9: Usage History

```bash
# Last 7 days
$ budget history --last 7d

📜 Usage History (last 7d, 42 records):

2026-03-17 14:32 | ubik-pm         | claude-sonnet-4-5    | $0.0375
2026-03-17 14:20 | chloe-life      | gpt-4o-mini          | $0.0124
2026-03-17 13:45 | ubik-pm         | gemini-2.5-flash     | $0.0063
2026-03-17 12:10 | openclaw-dev    | claude-sonnet-4-5    | $0.0450
...

Total: $8.45

# Last 24 hours
$ budget history --last 24h

📜 Usage History (last 24h, 15 records):

2026-03-17 14:32 | ubik-pm         | claude-sonnet-4-5    | $0.0375
2026-03-17 14:20 | chloe-life      | gpt-4o-mini          | $0.0124
...

Total: $2.40
```

## Example 10: OpenClaw Integration

### Heartbeat Check (HEARTBEAT.md)
```markdown
## Budget Monitoring

Every 6 hours:
1. Check: `budget status`
2. If any agent >70%: note in memory
3. If any agent >90%: notify Director
4. If any exceeded: escalate immediately with cost breakdown
```

### Cron Daily Report
```bash
# Add to crontab
0 9 * * * cd ~/skills/agent-budget-controller && \
  budget report --period day | \
  openclaw message send --target -1001234567890 --caption "📊 Daily Budget Report"
```

### Pre-call Wrapper Script
```bash
#!/bin/bash
# scripts/safe-agent-call.sh

set -e

AGENT=$1
shift

# Check budget before spawning
budget check --agent "$AGENT" || {
  echo "❌ Budget exceeded for $AGENT" >&2
  budget status --agent "$AGENT" >&2
  exit 1
}

# Spawn agent
echo "✅ Budget OK, spawning $AGENT..."
openclaw agents spawn "$AGENT" "$@"

# Note: Logging happens inside agent's post-call hook
```

## Example 11: Emergency Response

```bash
# Agent exceeded limit
$ budget check --agent runaway-agent
Budget check for Agent 'runaway-agent':
  daily: 🚫 EXCEEDED
  weekly: 🚫 EXCEEDED
  monthly: ✅ OK

# Investigate
$ budget report --period day --agent runaway-agent

📈 Budget Report: Today
Period: 2026-03-17 to 2026-03-17

Agent: runaway-agent
Total Cost: $5.40

By Model:
  claude-opus-4: $4.80  ← 🚨 Expensive model!
  claude-sonnet-4-5: $0.60

# Check recent calls
$ budget history --last 6h | grep runaway-agent

2026-03-17 14:45 | runaway-agent   | claude-opus-4        | $1.20
2026-03-17 14:40 | runaway-agent   | claude-opus-4        | $1.60
2026-03-17 14:35 | runaway-agent   | claude-opus-4        | $2.00  ← Loop!

# Action: Terminate agent, adjust limits
$ pkill -f runaway-agent
$ budget set --agent runaway-agent --daily 1.00  # Reduce limit
```

## Example 12: Multi-Agent Comparison

```bash
# Compare all agents today
$ budget report --period day

📈 Budget Report: Today
Period: 2026-03-17 to 2026-03-17

Total Cost: $12.45

By Agent:
  expensive-agent: $5.20  ← 🔴 41.8% of total
  ubik-pm: $3.10
  chloe-life: $2.15
  dev-agent: $1.50
  qa-agent: $0.50

# Check specific agent details
$ budget status --agent expensive-agent

📊 Agent Budget Status (2026-03-17)

Agent: expensive-agent

  🔴 Daily: $5.20 / $5.00 (104.0%) ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
  ⚠️ Weekly: $18.40 / $25.00 (73.6%) ⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛
  ✅ Monthly: $52.10 / $100.00 (52.1%) ⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛
```

## Tips & Best Practices

1. **Set conservative limits** — Start low, increase as needed
2. **Use agent-specific limits** — High-traffic agents get smaller budgets
3. **Monitor weekly** — Catch trends before monthly bill
4. **Log verbosely during testing** — Use `-v` flag to debug
5. **Check before long-running tasks** — `budget check` at start of cron jobs
6. **Archive old logs** — Move `usage.jsonl` monthly to keep it fast
7. **Update pricing quarterly** — API providers change rates
8. **Use cheaper models** — Gemini Flash for simple tasks, Claude Opus only when needed

## Common Workflows

### Daily Morning Routine
```bash
# 1. Check overnight usage
budget status

# 2. Review any alerts
budget check || echo "⚠️ Limits exceeded!"

# 3. Generate report
budget report --period day
```

### Weekly Review
```bash
# 1. Full weekly report
budget report --period week

# 2. Agent comparison
budget agents --days 7

# 3. Adjust limits if needed
budget set --agent heavy-user --weekly 30.00
```

### Incident Response
```bash
# 1. Identify runaway agent
budget history --last 1h

# 2. Get cost breakdown
budget report --period day --agent suspicious-agent

# 3. Block future calls
budget set --agent suspicious-agent --daily 0.01

# 4. Notify team
budget status | mail -s "Budget Alert" team@company.com
```
