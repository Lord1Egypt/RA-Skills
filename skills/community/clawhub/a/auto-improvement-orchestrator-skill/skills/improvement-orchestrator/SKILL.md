---
name: improvement-orchestrator
description: "当需要一键跑完「生成→评分→评估→执行→门禁」全流程、失败后自动重试、或批量改进多个 skill 时使用。不用于单独评估 skill 质量（用 improvement-learner）或手动打分（用 improvement-discriminator）。"
license: MIT
triggers:
  - improve skill
  - run improvement pipeline
  - self-improvement loop
  - orchestrate improvement
  - 批量改进
  - 一键优化
version: 0.1.0
author: OpenClaw Team
---

# Improvement Orchestrator

Coordinates the full improvement pipeline: Generator → Discriminator → Evaluator → Executor → Gate.

## When to Use

- Run a full improvement cycle on one or more skills
- Coordinate the 5-stage pipeline end-to-end (with optional evaluator)
- Retry failed improvements with trace-aware feedback (Ralph Wiggum loop)

## When NOT to Use

- **只想检查 skill 质量评分** → use `improvement-learner`
- **只想手动给候选打分** → use `improvement-discriminator`
- **只想改一个文件** → use `improvement-executor`
- **只想查基准数据** → use `benchmark-store`

## Pipeline

```
propose → discriminate → evaluate* → execute → gate
         ↻ Ralph Wiggum: fail → inject trace → retry (max 3)
         * evaluate is optional — skipped if no task_suite.yaml exists
```

<example>
正确用法: 对一个 skill 运行全流程改进
$ python3 scripts/orchestrate.py --target /path/to/skill --state-root ./state
→ 自动完成: 生成候选 → 多人盲审 → 任务评估 → 执行变更 → 6层门禁
→ 失败时自动注入 trace 重试（最多 3 次）
</example>

<anti-example>
错误用法: 只想看评分却用了 orchestrator
$ python3 scripts/orchestrate.py --target /path/to/skill  # 会执行变更！
→ 应该用: python3 improvement-learner/scripts/self_improve.py --skill-path /path/to/skill --max-iterations 1
</anti-example>

## CLI

```bash
python3 scripts/orchestrate.py \
  --target /path/to/skill \
  --state-root /path/to/state \
  --max-retries 3 \
  --auto
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Full pipeline | JSON with all stage outputs, final scores, execution trace |
| Retry cycle | Updated candidates with injected failure traces |

## Related Skills

- **improvement-generator**: Produces candidate proposals (stage 1)
- **improvement-discriminator**: Multi-reviewer panel scoring (stage 2)
- **improvement-evaluator**: Task suite execution validation (stage 3, optional)
- **improvement-executor**: Applies changes with backup/rollback (stage 4)
- **improvement-gate**: 6-layer quality gate (stage 5)
- **benchmark-store**: Frozen benchmarks and Pareto front data

## References

- [Architecture](references/architecture.md) — System design and data flow
- [Guardrails](references/guardrails.md) — Safety rules and protected targets
- [End-to-End Demo](references/end-to-end-demo.md) — Complete walkthrough
