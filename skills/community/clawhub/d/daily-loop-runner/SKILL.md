---
name: daily-loop-runner
description: "Run one controlled daily project loop for a single active project. Use on: scheduled daily runs, planner-initiated project steps, resuming a project after cleanup, user requests for active project advancement. Triggered when a project needs to advance by one meaningful step per day."
---

# Daily Loop Runner

Advance one project by one meaningful step per loop. State read before execution, structured writeback after.

## Input

Required:
- `project_card` — full project card with current state, goals, blockers
- `latest_weekly_review` — most recent weekly review notes
- `recent_daily_logs` — list of recent daily loop logs (last 3-5)
- `open_questions` — unresolved questions from previous loops

Optional:
- `forced_bottleneck` — override automatic bottleneck selection

## Output Schema

```
today_objective: string               # one clear goal for today
selected_agent: string | null         # which agent or tool will execute
task_input: object                    # structured input for the selected agent
expected_output: string                # what success looks like
execution_summary: string             # what actually happened
findings: string[]                    # key discoveries
decisions: string[]                   # decisions made based on findings
next_action: string | null            # what to do tomorrow
project_card_updates: object          # fields to update on project card
writeback_payload: object             # structured record for project memory
safe_to_proceed: boolean              # false if state was incomplete
```

## Hard Rules

1. **One project per run.** Do not split focus.
2. **One bottleneck per run.** Pick the most critical blocker.
3. **One main action per run.** One meaningful step, not a sprint.
4. **No execution without state read.** Always read project_card and recent logs first.
5. **No successful completion without next_action.** Every loop must feed into the next.

## Loop Phases

### Phase 1: State Read
- Read project_card fully
- Read recent_daily_logs
- Note open_questions from previous runs
- Identify current project phase and milestone

### Phase 2: Bottleneck Selection
- Pick the single most critical bottleneck
- If forced_bottleneck provided, use it
- If nothing is blocking, advance the primary goal

### Phase 3: Task Input Construction
- Build a focused task_input for the selected agent
- Include: what to do, why it matters, what success looks like
- Exclude: everything else

### Phase 4: Execution
- Dispatch task to selected agent
- Wait for execution_summary and findings

### Phase 5: Writeback
- Update project_card with project_card_updates
- Write execution_summary + findings to daily log
- Populate next_action for tomorrow's loop
- Set safe_to_proceed = true

## Failure Handling

If state is incomplete (missing project_card, no recent logs, unclear objective):
- Stop the run immediately
- Set `safe_to_proceed = false`
- Request cleanup or missing-state repair
- Do not attempt execution with partial state

## State Machine

```
IDLE → READY → RUNNING → WRITING → DONE
                    ↓
              BLOCKED (if state incomplete)
```

Respect the state machine. Never skip from IDLE to RUNNING.
