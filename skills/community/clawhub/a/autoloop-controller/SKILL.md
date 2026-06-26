---
name: autoloop-controller
description: "When continuous automated improvement of a Skill is needed. Wraps improvement-orchestrator in a persistent loop with convergence detection (plateau/oscillation), cost control, and cross-session state persistence. Not for single-shot improvement (use improvement-orchestrator) or quality scoring (use improvement-learner)."
license: MIT
triggers:
  - continuous improvement
  - autoloop
  - keep improving
  - 持续改进
  - 自动循环
  - 一直优化
---

# Autoloop Controller

Wraps improvement-orchestrator in a persistent loop with convergence detection and cost control. Each iteration runs the full 5-stage pipeline (generate, discriminate, evaluate, execute, gate), then checks five termination conditions before deciding whether to continue. State is persisted to disk after every iteration, so the loop survives crashes and can resume across sessions.

## When to Use

- Continuously improve a skill over multiple iterations until scores plateau
- Run overnight improvement (Karpathy autoresearch style) where you start the loop, walk away, and review results next morning
- Schedule periodic improvement cycles via system cron (scheduled mode exits after each run, cron triggers the next)
- Resume a previously interrupted improvement run from saved state
- Apply budget-constrained batch improvement when you want to spend at most $N improving a skill
- Drive a skill from EMERGING to SOLID quality tier through compounding gains across rounds
- Detect and halt on oscillation patterns (keep-reject-keep-reject) that waste resources without convergence
- Compare improvement velocity across skills by examining iteration_log.jsonl outputs

## When NOT to Use

- **Single-shot improvement** -- use `improvement-orchestrator` directly; the autoloop overhead (state persistence, convergence checks) adds no value for one-off runs
- **Only want quality scores** -- use `improvement-learner`; the autoloop controller calls the orchestrator which does more than just scoring
- **Only want baseline/benchmark data** -- use `benchmark-store`; autoloop does not interact with the Pareto front database directly
- **Manual interactive improvement** -- autoloop is designed for unattended operation; if you want to review each candidate before applying, run orchestrator manually

## Why Continuous Loop with Convergence Detection

**Problem**: A single improvement-orchestrator run typically raises 1-2 quality dimensions by 0.05-0.15 points. Moving a skill from EMERGING (weighted score < 0.60) to SOLID (> 0.80) requires 4-8 compounding rounds because each round exposes new weaknesses that were masked by more severe ones. Running these rounds manually means remembering to re-invoke, tracking which iteration you are on, and monitoring for diminishing returns.

**Tradeoff**: Automated looping captures compounding gains that single-shot improvement misses -- each round fixes issues revealed by the previous round's improvements. But unbounded loops waste money: after 3-5 rounds, most skills hit a plateau where further iterations produce reject decisions or marginal gains below noise. The default $50 cost cap and 3-round plateau window balance thoroughness against waste. Because the loop persists state to disk after every iteration, a crash at iteration 4 of 10 loses zero progress -- the next invocation picks up at iteration 5 with full score history intact.

**Because** convergence detection uses two independent signals (plateau: no score improvement over N rounds; oscillation: alternating keep/reject decisions), the controller avoids both the false-stop problem (plateau alone would halt on a temporary dip followed by recovery) and the infinite-loop problem (oscillation alone would not catch gradual flatlining). The circuit breaker (consecutive errors) adds a third safety net for infrastructure failures.

## 3 Modes

| Mode | Trigger | Behavior | Best For |
|------|---------|----------|----------|
| single-run | CLI one-shot | Runs all iterations in sequence, then exits | Batch improvement during work hours |
| continuous | CLI long-running | Loop with configurable cooldown between iterations | Overnight unattended runs |
| scheduled | System cron | Exits after one iteration; cron triggers the next run | Production recurring improvement |

In **single-run** mode, the controller loops through all iterations within a single process invocation, checking termination conditions between each. In **continuous** mode, it inserts a cooldown period (default 30 minutes) between iterations to spread LLM API load. In **scheduled** mode, the process exits after each iteration and relies on an external scheduler (cron) to invoke the next run; the persisted state file ensures continuity.

## Termination (5 conditions, OR logic)

The controller evaluates all five conditions after each iteration. Any single condition triggers a stop.

1. **max_iterations reached** -- Hard cap on total pipeline runs. Default: 5. Set via `--max-iterations`. The controller compares `iterations_completed` against this cap. Use higher values (10-15) for skills starting at EMERGING tier; lower values (3-5) for skills already at SOLID.

2. **cost_cap exceeded** -- Cumulative estimated cost across all iterations. Default: $50. Set via `--max-cost`. Cost is estimated at ~$0.10/minute of pipeline execution time. When the running total meets or exceeds the cap, the loop halts with status `stopped_cost`. Always set this explicitly in continuous mode to avoid surprise bills.

3. **score plateau detected** -- No weighted score improvement over the last N consecutive rounds (default N=3, set via `--plateau-window`). The detector compares the best score in the most recent N rounds against the historical best before that window. A plateau means the skill has reached a local optimum for the current improvement strategy.

4. **oscillation detected** -- Alternating keep/reject decisions over the last 4 rounds (e.g., keep-reject-keep-reject). This pattern indicates the generator is producing changes that pass the gate on one round but cause regressions caught on the next. Oscillation wastes cost without net progress.

5. **consecutive errors exceeded** -- N consecutive pipeline failures (default N=3, set via `--max-consecutive-errors`). Acts as a circuit breaker for infrastructure issues (LLM rate limits, network failures, disk full). The counter resets to zero after any successful iteration.

```python
# Termination check logic (simplified from autoloop.py)
def should_stop(state) -> tuple[bool, str]:
    if state.iterations_completed >= state.max_iterations:
        return True, "max_iterations reached"
    if state.total_cost_usd >= state.max_cost_usd:
        return True, "cost_cap exceeded"
    if detect_plateau(state.score_history, window=state.plateau_window):
        return True, "plateau detected"
    if detect_oscillation(state.score_history, window=4):
        return True, "oscillation detected"
    if state.consecutive_errors >= state.max_consecutive_errors:
        return True, "consecutive_errors exceeded"
    return False, ""
```

<example>
Correct: Run 5 iterations with a $20 budget cap
$ python3 scripts/autoloop.py \
    --target ./skills/my-skill \
    --state-root /tmp/autoloop-state \
    --max-iterations 5 \
    --max-cost 20.0 \
    --mode single-run
-> Runs the orchestrator up to 5 times
-> Stops early if plateau detected (3 consecutive rounds with no improvement)
-> Stops early if cumulative cost reaches $20
-> State saved to /tmp/autoloop-state/autoloop_state.json for resumption
</example>

<anti-example>
Running continuous mode without explicit cost cap:
$ python3 scripts/autoloop.py --target ./skills/my-skill --state-root /tmp/state --mode continuous
-> DANGEROUS: no --max-cost flag means the default $50 cap applies
-> In continuous mode with 30-minute cooldown, this could run for hours
-> Always set --max-cost explicitly when using continuous mode
</anti-example>

## CLI

Full argument reference:

```bash
python3 scripts/autoloop.py \
  --target <skill_path>              # Required. Path to the skill directory
  --state-root <dir>                 # Required. Directory for state persistence
  --max-iterations 5                 # Max pipeline runs (default: 5)
  --max-cost 50.0                    # Budget ceiling in USD (default: 50.0)
  --plateau-window 3                 # Rounds without improvement before stop (default: 3)
  --cooldown-minutes 30              # Minutes between iterations in continuous mode (default: 30)
  --max-consecutive-errors 3         # Circuit breaker threshold (default: 3)
  --mode single-run                  # single-run | continuous | scheduled
  --dry-run                          # Simulate without calling orchestrator
```

### Scheduling with Cron (scheduled mode)

```bash
# Add to crontab: run every 4 hours at minute 17
17 */4 * * * /path/to/scripts/run-eval.sh /path/to/skill /path/to/state

# run-eval.sh wraps autoloop.py in --mode single-run with logging
# Each cron invocation picks up state from the previous run
```

## State Recovery After Crash

The controller writes `autoloop_state.json` after every iteration. If the process crashes mid-iteration (OOM, network timeout, Ctrl-C), the state file reflects the last completed iteration. Restarting with the same `--state-root` resumes from that checkpoint.

```bash
# Check current state after a crash
cat /tmp/autoloop-state/autoloop_state.json | python3 -m json.tool

# Resume from where it left off -- same command as the original run
python3 scripts/autoloop.py \
  --target ./skills/my-skill \
  --state-root /tmp/autoloop-state \
  --max-iterations 10 \
  --max-cost 30.0 \
  --mode single-run
# -> Loads existing state, sees iterations_completed=4, continues from iteration 5
```

State fields that carry across sessions: `iterations_completed`, `total_cost_usd`, `score_history`, `plateau_counter`, `current_scores`, `consecutive_errors`. The `status` field is reset to `running` on resume. CLI arguments (`--max-iterations`, `--max-cost`, etc.) override persisted values, so you can tighten or relax limits between sessions.

## Handoff Document Format

When the autoloop completes (any termination condition), it prints a summary to stdout. For integration with other tools or human review, parse the state file:

```json
{
  "schema_version": "1.0",
  "target": "./skills/my-skill",
  "iterations_completed": 5,
  "max_iterations": 10,
  "total_cost_usd": 18.42,
  "max_cost_usd": 30.0,
  "status": "stopped_plateau",
  "current_scores": {
    "accuracy": 0.87,
    "coverage": 0.92,
    "trigger_quality": 0.85,
    "knowledge_density": 0.78
  },
  "score_history": [
    {"iteration": 1, "weighted_score": 0.65, "decision": "keep"},
    {"iteration": 2, "weighted_score": 0.72, "decision": "keep"},
    {"iteration": 3, "weighted_score": 0.78, "decision": "keep"},
    {"iteration": 4, "weighted_score": 0.78, "decision": "reject"},
    {"iteration": 5, "weighted_score": 0.79, "decision": "keep"}
  ],
  "plateau_counter": 3,
  "plateau_window": 3
}
```

The companion `iteration_log.jsonl` file contains one JSON object per line with per-iteration timing, cost, and artifact references. Use it for post-hoc analysis of improvement velocity.

## Output Artifacts

| Artifact | Path | Format | Description |
|----------|------|--------|-------------|
| Loop state | `<state-root>/autoloop_state.json` | JSON | Full controller state including scores, history, termination reason, and resume data. Updated after every iteration. |
| Iteration log | `<state-root>/iteration_log.jsonl` | JSONL | Append-only log with one entry per completed iteration: timing, cost, decision, candidate ID, and artifact path. |
| Orchestrator outputs | `<state-root>/` (subdirectories) | Mixed | Each iteration produces orchestrator-level artifacts (candidates, gate results, diffs) in the state root. |
| Console summary | stdout | Text | Human-readable summary printed on termination: iteration count, total cost, best score, and stop reason. |

The state file uses `schema_version: "1.0"` for forward compatibility. Unknown fields are ignored on load, so older controllers can read state files written by newer versions.

## Related Skills

- **improvement-orchestrator**: The single-pipeline runner that autoloop wraps. Each autoloop iteration invokes one full orchestrator run (generate, discriminate, evaluate, execute, gate). Use orchestrator directly for one-off improvements.
- **improvement-learner**: Provides the 9-dimension quality scores that autoloop uses for convergence detection. The learner's weighted score feeds into plateau and oscillation detectors.
- **improvement-discriminator**: Multi-reviewer panel scoring within each orchestrator run. Autoloop does not call the discriminator directly; it is invoked by the orchestrator.
- **improvement-generator**: Produces candidate proposals within each orchestrator run. When autoloop detects oscillation, this often indicates the generator needs a different strategy.
- **benchmark-store**: Pareto front data and quality tier thresholds. Autoloop does not write to benchmark-store, but the scores it tracks are comparable to benchmark baselines.
