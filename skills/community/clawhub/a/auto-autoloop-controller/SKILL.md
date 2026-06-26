---
name: autoloop-controller
category: orchestration
description: "When continuous automated improvement of a Skill is needed. Wraps improvement-orchestrator in a persistent loop with convergence detection (plateau/oscillation), cost control, and cross-session state persistence. Not for single-shot improvement (use improvement-orchestrator) or quality scoring (use improvement-learner)."
license: MIT
triggers:
  - continuous improvement
  - autoloop
  - keep improving
  - 持续改进
  - 自动循环
  - 一直优化
version: 0.1.0
author: OpenClaw Team
---

# Autoloop Controller

Wraps improvement-orchestrator in a persistent loop with convergence detection and cost control.

## When to Use
- Continuously improve a skill over multiple iterations (overnight runs)
- Schedule periodic improvement cycles via cron
- Run a fixed number of improvement iterations with automatic plateau detection

## When NOT to Use
- **Single-shot improvement** → use `improvement-orchestrator`
- **Only want scores** → use `improvement-learner`
- **Only want baseline data** → use `benchmark-store`

## CLI

```bash
python3 scripts/autoloop.py \
  --target /path/to/skill \        # REQUIRED: skill directory to improve
  --state-root /path/to/state \    # REQUIRED: persistent state directory
  --max-iterations 5 \             # default 5: total iterations before stop
  --max-cost 50.0 \                # default 50.0: cost cap in USD
  --plateau-window 3 \             # default 3: consecutive no-improvement rounds → stop
  --cooldown-minutes 30 \          # default 30: delay between iterations in continuous mode
  --mode single-run \              # single-run | continuous | scheduled
  --dry-run                        # simulate without calling orchestrator
```

| Param | Default | When to change |
|-------|---------|---------------|
| `--max-iterations` | 5 | Raise to 20 for overnight runs; lower to 2 for quick tests |
| `--max-cost` | $50.0 | Lower to $5 for testing; raise for production overnight runs |
| `--plateau-window` | 3 | Raise to 5 if improvements are slow but steady |
| `--cooldown-minutes` | 30 | Lower to 5 for rapid iteration; raise to 60 for rate-limited APIs |
| `--dry-run` | false | Use to test loop logic without running real orchestrator |

## 3 Modes

| Mode | Behavior | Exit Condition |
|------|----------|---------------|
| `single-run` | Loop through iterations, exit when termination hit | max_iterations / cost_cap / plateau / oscillation |
| `continuous` | Loop with `cooldown_minutes` sleep between iterations | Same + Ctrl+C saves state gracefully |
| `scheduled` | Run exactly 1 iteration then exit | Cron triggers next run; state persists in `autoloop_state.json` |

## Termination (4 conditions, OR logic)

1. `max_iterations` reached
2. `cost_cap` exceeded (rough estimate: ~$0.10/min of LLM time)
3. Score plateau: weighted_score no improvement for `plateau_window` consecutive rounds
4. Oscillation: keep-reject alternating pattern detected over 4-round window

## Cross-Session State

State persists in `{state-root}/autoloop_state.json` (dataclass → JSON):
```json
{"schema_version": "1.0", "target": "/path/to/skill",
 "iterations_completed": 3, "max_iterations": 5,
 "total_cost_usd": 1.23, "max_cost_usd": 50.0,
 "score_history": [{"iteration": 1, "weighted_score": 0.72, "decision": "keep"}, ...],
 "plateau_counter": 1, "status": "running"}
```

Resume a stopped run: just re-run the same command — `AutoloopState.load()` picks up from where it left off.

## Output Artifacts

- `handoffs/iteration-N.md` — per-iteration handoff with Decided/Rejected/Scores/Remaining sections for cross-iteration context survival
- `iteration_log.jsonl` — one JSON line per iteration: `{"iteration": 1, "decision": "keep", "weighted_score": 0.72, "cost_usd": 0.15, "candidate_id": "cand-01-docs"}`
- `autoloop_state.json` — full serialized state for cross-session resume

<example>
Run 5 iterations with cost cap:
$ python3 scripts/autoloop.py --target /path/to/skill --state-root ./state --max-iterations 5 --max-cost 10.0
→ --- Iteration 1/5 ---
→   Decision: keep  Weighted score: 0.7200  Cumulative cost: $0.1500
→ --- Iteration 2/5 ---
→   Decision: keep  Weighted score: 0.7800  Cumulative cost: $0.3100
→ --- Iteration 3/5 ---
→   Decision: keep  Weighted score: 0.7800  Cumulative cost: $0.4600
→ Stopped: plateau detected (no improvement in last 3 iterations)
→ State saved: ./state/autoloop_state.json
</example>

<anti-example>
Running continuous mode without checking cost cap:
$ python3 scripts/autoloop.py --target /path/to/skill --state-root ./state --mode continuous --max-cost 50.0
→ Default $50 cap applies. For overnight runs, explicitly set --max-cost.
→ Always verify cost cap BEFORE launching continuous mode.
</anti-example>

## Error Handling

- Orchestrator subprocess failure: `state.status = "error"`, stderr saved to `last_failure_trace`, loop exits
- KeyboardInterrupt (Ctrl+C): state saved as `status=completed`, graceful exit
- Unhandled exceptions: traceback saved to `last_failure_trace`, `status=error`, exit code 1

## Related Skills

- **improvement-orchestrator**: Single pipeline run (called as subprocess each iteration)
- **improvement-learner**: Provides dimension scores consumed by `_load_latest_scores()` for weighted_score computation
- **benchmark-store**: Pareto front data for convergence tracking
