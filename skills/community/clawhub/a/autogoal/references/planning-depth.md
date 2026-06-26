# Planning Depth & Strategy Reference

Match planning depth to goal complexity. Track outcomes to improve over time.

## Planning Depth Levels

| Level | When | Format |
|-------|------|--------|
| **L0** | Trivial, done before | No plan, just execute |
| **L1** | Simple, low risk | Mental checklist, no doc |
| **L2** | Medium complexity | Bullet list, share with channel |
| **L3** | Complex, multi-step | Detailed plan with milestones |
| **L4** | High stakes, novel | Full plan + human validation |

### Quick Decision

| Signal | Level |
|--------|-------|
| Done this before successfully | L0-L1 |
| Clear single deliverable | L1-L2 |
| Multiple components | L3 |
| Dependencies between steps | L3 |
| High stakes / hard to redo | L4 |
| Ambiguous success criteria | L3-L4 |
| Estimated >30 min work | L3+ |

**Default:** When uncertain, use L2. A quick plan costs minutes; a failed one-shot costs hours.

## Strategy Templates

### Sequential
Best for: Linear workflows, clear dependencies
```
1. Step A (blocks B)
2. Step B (blocks C)
3. Step C (final output)
```
Use when: Each step needs previous step's output

### Parallel
Best for: Independent components
```
Track 1: A1 → A2 → A3
Track 2: B1 → B2 → B3
Merge: Combine A3 + B3
```
Use when: Work can happen simultaneously

### Iterative
Best for: Uncertain requirements, creative work
```
Cycle 1: Draft → Feedback → Revise
Cycle 2: Draft → Feedback → Revise
Cycle N: Until acceptable
```
Use when: Can't get it right first try

### Spike
Best for: Technical unknowns
```
1. Spike: Prove feasibility (timeboxed)
2. Decide: Continue or pivot
3. Execute: Full implementation if spike succeeded
```
Use when: Not sure if approach will work

### Checkpoint
Best for: Long tasks, high stakes
```
1. Milestone A → Validate with human
2. Milestone B → Validate with human
3. Milestone C → Final delivery
```
Use when: Course correction needed mid-flight

## Strategy Selection Quick Guide

| Situation | Strategy |
|-----------|----------|
| Clear steps, dependencies | Sequential |
| Multiple independent parts | Parallel |
| Subjective output (writing, design) | Iterative |
| Technical risk | Spike |
| >1 day duration | Checkpoint |
| High stakes, novel | Checkpoint + Iterative |

## Recording Outcomes

After each check-in, log the outcome with lessons:

```
python3 goal_engine.py log-outcome <goal-id> \
  --action "What you did" \
  --result "success|partial|failure" \
  --lessons "What to do differently"
```

After 3+ sessions, run `python3 goal_engine.py learn <goal-id> --lesson "<durable insight>"` to reinforce it. After 3 repetitions, it auto-promotes to HOT.

## Risk Rules (for Financial Goals)

Set risk parameters at goal creation or during a check-in:

```
python3 goal_engine.py set-risk-rules <goal-id> --json '{
  "max_position_size": 100,
  "max_drawdown": 0.15,
  "max_daily_trades": 10,
  "stop_loss_percent": 0.05,
  "max_exposure_percent": 60
}'
```

Rules show up in every check-in prompt and the report view.

## Strategy Outcome Tracking

Over time, patterns emerge:

| Goal Type | Best Depth | Best Strategy |
|-----------|-----------|---------------|
| Kalshi prediction markets | L2 | Checkpoint |
| Crypto paper trading | L2 | Sequential |
| Alpaca swing trading | L2 | Checkpoint |
| Homelab infrastructure | L3 | Spike → Sequential |
| New feature/experiment | L3 | Spike → Iterative |

Keep this updated as goals complete and outcomes accumulate.
