---
name: improvement-evaluator
description: "当需要验证 Skill 改进是否真正提升了 AI 执行效果时使用。通过预定义任务集（YAML）运行 AI 任务，判定 pass/fail，输出 execution_pass_rate。不用于文档结构评分（用 improvement-learner）或候选打分（用 improvement-discriminator）。"
license: MIT
triggers:
  - evaluate skill execution
  - run task suite
  - execution pass rate
  - 执行效果评估
  - 任务集验证
---

# Improvement Evaluator

Measures whether a Skill actually makes AI perform better on real tasks.

## When to Use
- Verify that a SKILL.md change improves AI task execution (not just document structure)
- Run a task suite against a candidate SKILL.md and compare with baseline
- Get execution_pass_rate as a concrete quality metric

## When NOT to Use
- **只想检查 SKILL.md 结构质量** → use `improvement-learner`
- **只想给候选打分** → use `improvement-discriminator`
- **跑全流程** → use `improvement-orchestrator`

## Task Suite Format (YAML)
(reference: references/task-format.md)

## 3 Judge Types
| Judge | Mechanism | Use When |
|-------|-----------|----------|
| ContainsJudge | Check output contains expected keywords | Deterministic checks |
| PytestJudge | Run pytest on AI output | Structured output validation |
| LLMRubricJudge | LLM scores against rubric | Semantic quality (mock mode available) |

<example>
Evaluate a skill with a task suite:
$ python3 scripts/evaluate.py --input ranking.json --candidate-id c1 --task-suite tasks.yaml --state-root /tmp/state
→ {"execution_pass_rate": 0.80, "baseline_pass_rate": 0.70, "delta": 0.10, "verdict": "pass"}
</example>

<anti-example>
Using evaluator without a task suite:
→ Will output verdict="skipped" — evaluator requires a task_suite.yaml
</anti-example>

## CLI
python3 scripts/evaluate.py --input <ranking.json> --candidate-id <id> --task-suite <tasks.yaml> --state-root <dir> [--pass-k 1] [--baseline-cache-dir <dir>] [--output <path>]

## Output Artifacts
| Request | Deliverable |
|---------|------------|
| Evaluate candidate | JSON with execution_pass_rate, baseline_pass_rate, delta, verdict |

## Related Skills
- **improvement-discriminator**: Semantic scoring (stage before evaluator)
- **improvement-gate**: Quality gate (stage after evaluator)
- **improvement-orchestrator**: Full pipeline coordination


## Quick Start

```bash
# Evaluate a skill using its task suite
python3 scripts/evaluate.py \
  --input /path/to/ranking-artifact.json \
  --candidate-id cand-01-docs \
  --task-suite /path/to/task_suite.yaml \
  --state-root ~/.openclaw/shared-context/intel/auto-improvement/state

# Standalone baseline evaluation (no ranking artifact needed)
python3 scripts/evaluate.py \
  --standalone \
  --task-suite /path/to/task_suite.yaml \
  --skill-path /path/to/skill
```
