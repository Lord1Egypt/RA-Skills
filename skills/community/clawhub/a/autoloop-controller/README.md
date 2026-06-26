# autoloop-controller

Persistent improvement loop for AI skills. Wraps the improvement-orchestrator pipeline in a loop with convergence detection, cost control, and cross-session state persistence.

## What It Does

Runs the 5-stage improvement pipeline (generate, discriminate, evaluate, execute, gate) repeatedly on a target skill until one of five termination conditions fires:

1. Maximum iterations reached
2. Cost cap exceeded
3. Score plateau detected (no improvement over N rounds)
4. Oscillation detected (alternating keep/reject pattern)
5. Consecutive errors exceeded (circuit breaker)

State is written to disk after every iteration, so the loop survives crashes and resumes seamlessly.

## Quick Start

```bash
# Run up to 5 improvement rounds with a $20 budget
python3 scripts/autoloop.py \
  --target ./skills/my-skill \
  --state-root /tmp/autoloop-state \
  --max-iterations 5 \
  --max-cost 20.0 \
  --mode single-run
```

## Modes

| Mode | Description |
|------|-------------|
| `single-run` | All iterations in one process, then exit |
| `continuous` | Loop with cooldown between iterations (default 30 min) |
| `scheduled` | One iteration per invocation; pair with system cron |

## Project Structure

```
autoloop-controller/
  SKILL.md              # Skill definition (triggers, usage, reference)
  README.md             # This file
  scripts/
    autoloop.py         # Main controller logic
    convergence.py      # Plateau and oscillation detection
    cost_tracker.py     # Immutable cost tracking
    run-eval.sh         # Shell wrapper for cron scheduling
  references/
    state-format.md     # autoloop_state.json schema documentation
    scheduling-guide.md # Cron and scheduling setup guide
  tests/                # pytest test suite
```

## Output Files

- `autoloop_state.json` -- Full loop state (scores, history, resume data)
- `iteration_log.jsonl` -- Append-only per-iteration log (timing, cost, decisions)

## Dependencies

- Python 3.10+
- `lib.common` from the repository root (shared JSON utilities)
- `improvement-orchestrator` skill (invoked as subprocess)

## License

MIT
