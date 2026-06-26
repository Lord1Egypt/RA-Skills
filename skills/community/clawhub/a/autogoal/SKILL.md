---
name: autogoal
description: "Autonomous goal achievement skill.\n\nUse when the user says something like:\n
- 'I want to make profit in the #kalshi channel'\n
- 'Keep my homelab uptime above 99.9%'\n
- 'Improve my trading win rate'\n
- 'Make this project successful'\n
- 'Achieve this goal'\n
- 'I need a system to work toward X'\n
- Any open-ended long-term objective the user wants automated progress on\n\n
This skill wires up a goal with periodic check-ins, automatic strategy adaptation, and progress reporting.
It is NOT for one-off tasks — use it when the user wants ongoing, self-improving pursuit of a goal.\n\nTrigger examples:\n
- User: 'make this channel profitable'\n
- User: 'set up the goal system to maximize X'\n
- User: 'give openclaw a goal and it automatically does what it can to achieve that goal'"
---

# Goal-Achiever

Turn user goals into self-improving automated pursuit loops.

## How it works

```
User states goal
  ↓
1. INTAKE: Record goal + determine strategy
2. SCHEDULE: Create cron job for periodic check-ins
3. EXECUTE: Each cron run evaluates, acts, logs, adapts
4. CLOSE: Goal achieved or abandoned → clean up
5. REPORT: Surface progress to user periodically
```

## Step-by-step workflow

### 1. Intake

When a user states a goal, immediately:

a) Run the goal engine to create a record:
```
python3 scripts/goal_engine.py create "<goal statement>" --channel "<channel-id>"
```

b) Determine the initial strategy. Consider:
- What available skills/tools can act toward this goal?
- What metrics track progress? (profit, uptime, completion %)
- What's the right check-in cadence? (See `references/goal-lifecycle.md` for pattern guidance)
- Are there milestones to define?

c) Write the strategy to the goal:
```
python3 scripts/goal_engine.py adapt "<goal-id>" --strategy "<strategy description>"
```

### 2. Schedule

Generate and create a cron job for the periodic check-in loop:
```
python3 scripts/goal_engine.py cron "<goal-id>"
```
This prints JSON. Use the output to create an OpenClaw cron job (cron tool → add action).

**Default cadence**: every 1 hour (3,600,000 ms). Adjust based on goal type — see `references/goal-lifecycle.md`.

The cron job's payload includes: goal statement, current strategy, and step-by-step instructions for the check-in agent turn.

### 3. Execute (cron check-in)

Each cron-run agent turn should:

1. **Evaluate** — What's the current state? Has anything changed since the last check?
2. **Take action** — Do one concrete thing that moves toward the goal. Use whatever tools/skills make sense.
3. **Log** — Write what you did and the outcome:
   ```
   python3 scripts/goal_engine.py log-action "<goal-id>" --action "<what you did>" --result "<outcome>"
   ```
4. **Adapt** — If the current approach isn't working, change strategy:
   ```
   python3 scripts/goal_engine.py adapt "<goal-id>" --strategy "<new approach>"
   ```
5. **Report** — Tell the user what happened. Concise. Include metric movement if measurable.
6. **Close check** — If the goal is achieved, close it:
   ```
   python3 scripts/goal_engine.py close "<goal-id>" --status completed
   ```
   Then disable or remove the cron job.

### 4. Strategy Adaptation

If after 3 check-ins there's no measurable progress:
- Switch tactics (different tools, different approach)
- Read `references/goal-lifecycle.md` for adaptation heuristics
- Escalate to user: "I've tried X and Y but Z isn't improving. Ideas?"

### 5. Reporting

Check-ins report to the channel where the goal was stated. Key reporting patterns:
- **Progress summary**: "Goal X: metric improved from A to B (strategy: C is working)"
- **Strategy change**: "Switching approach from X to Y because Z wasn't improving"
- **Stuck signal**: "Need input on how to proceed with goal X"
- **Completion**: "Goal X achieved! 🎉"

## Goal Engine Script

`scripts/goal_engine.py` manages the goal registry (`goals_registry.json`).

### Core Commands
| Command | Usage |
|---------|-------|
| create | `create "<statement>" --channel "<id>"` |
| plan | `plan "<statement>" --depth L0-L4 [--strategy <type>]` — create with planning depth |
| list | `list [--status active\|paused\|completed\|abandoned]` |
| status | `status <goal-id>` — full JSON dump |
| update | `update <goal-id> --key <path> --value <json>` |
| log-action | `log-action <goal-id> --action "<text>" --result "<text>"` |
| adapt | `adapt <goal-id> --strategy "<new strategy>"` |
| advance | `advance <goal-id> --milestone "<desc>"` |
| close | `close <goal-id> --status completed\|abandoned` |
| set-metrics | `set-metrics <goal-id> --json '{"key": "value"}'` |
| set-session-state | `set-session-state <goal-id> --objective "..." --blocker "..." --next "..."` |
| set-risk-rules | `set-risk-rules <goal-id> --json '{"max_position_size": 100}'` |
| log-outcome | `log-outcome <goal-id> --action "..." --result "..." --lessons "..."` |
| learn | `learn <goal-id> --lesson "..."` |
| report | `report [--status active\|paused\|completed\|abandoned] [--stalled]` |
| cron | `cron <goal-id>` — print cron job JSON |

### Merged Features

This skill combines the best patterns from three OpenClaw skills:

**From Self-Improving Proactive Agent:**
- Session state tracking (objective, blocker, decision, next move)
- Self-improvement learning loop (lessons promote to HOT after 3 repetitions)
- Stalled goal detection

**From Plan:**
- Planning depth levels (L0-L4) with quick decision framework
- Strategy templates (sequential, parallel, iterative, spike, checkpoint)
- Outcome tracking for strategy self-improvement

**From Auto-Trading Strategy:**
- Risk rules for financial goals (position sizing, drawdown caps, trade limits)
- Metrics tracking integrated into check-in context

### Check-In Prompt Context

Each cron check-in automatically includes:
- Goal statement + status
- Plan depth and strategy
- Current session state (objective, blocker, next move)
- Risk rules (if set)
- Recent metrics
- Last 3 actions with results
- ⚠️ Stalled warning if applicable
- Step-by-step instructions with exact CLI commands

## Lifecycle Patterns

Read `references/goal-lifecycle.md` for detailed guidance on:
- Periodic-review vs one-shot vs parameter-tuning goals
- Suggested check-in cadences by goal type
- Strategy adaptation heuristics
- Progress signals

Read `references/planning-depth.md` for:
- Planning depth decision matrix
- Strategy template descriptions
- Outcome tracking workflow
- Risk rule configuration guide

## Cleanup

When a goal is completed or abandoned:
1. `python3 scripts/goal_engine.py close "<goal-id>" --status completed`
2. Disable/remove the associated cron job
3. Optionally archive the goal registry entry (status handles this)

## Safety

- Goals with financial stakes should start in paper/simulation mode (see `~/self-improving/` project notes for Kalshi/Alpaca)
- If a goal requires irreversible external actions, ask before acting the first time
- Abandoned goals remain in the registry but are skipped by cron — clean them up when the user is ready
