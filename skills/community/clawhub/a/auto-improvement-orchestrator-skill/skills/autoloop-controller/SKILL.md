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

Wraps improvement-orchestrator in a persistent loop with convergence detection and cost control.

## When to Use
- Continuously improve a skill over multiple iterations
- Run overnight improvement like Karpathy autoresearch
- Schedule periodic improvement cycles

## When NOT to Use
- **Single-shot improvement** → use `improvement-orchestrator`
- **Only want scores** → use `improvement-learner`
- **Only want baseline data** → use `benchmark-store`

## 3 Modes
| Mode | Trigger | Behavior |
|------|---------|----------|
| single-run | CLI / cron | One iteration then exit |
| continuous | CLI | Loop with cooldown until termination |
| scheduled | system cron | Exit after each run, cron triggers next |

## Termination (3 conditions, OR logic)
1. max_iterations reached
2. cost_cap exceeded
3. score plateau detected (N rounds no improvement)

<example>
Run 5 iterations of improvement:
$ python3 scripts/autoloop.py --target /path/to/skill --state-root /tmp/state --max-iterations 5 --mode single-run
→ Runs orchestrator up to 5 times, stops on plateau or cost cap
→ State saved to /tmp/state/autoloop_state.json for resumption
</example>

<anti-example>
Running continuous mode without cost cap:
$ python3 scripts/autoloop.py --target /path/to/skill --mode continuous
→ DANGEROUS: no --max-cost means default $50 cap applies
→ Always verify cost cap before continuous mode
</anti-example>

## CLI
python3 scripts/autoloop.py --target <skill_path> --state-root <dir> --max-iterations 5 --max-cost 50.0 --plateau-window 3 --cooldown-minutes 30 --mode [single-run|continuous|scheduled]

## Output Artifacts
| Request | Deliverable |
|---------|------------|
| Run loop | autoloop_state.json + iteration_log.jsonl |
| Check status | Current state with scores and termination reason |

## Related Skills
- **improvement-orchestrator**: Single pipeline run (wrapped by this skill)
- **improvement-learner**: Quality scoring (consumed by this skill)
- **benchmark-store**: Pareto front data


## Quick Start

```bash
# Run 5 improvement rounds on a skill
python3 scripts/autoloop.py \
  --target /path/to/skill \
  --state-root ~/.openclaw/shared-context/intel/auto-improvement/state \
  --max-rounds 5
```
