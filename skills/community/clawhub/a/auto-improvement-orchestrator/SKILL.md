---
name: improvement-orchestrator
category: orchestration
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
propose → discriminate → evaluate* → execute → gate (7-layer)
         ↻ Ralph Wiggum: fail → inject trace → retry (max N)
         * evaluate skipped if: no --task-suite, OR low-risk docs/reference/guardrail (adaptive complexity)
```

**Adaptive Complexity Skip**: candidates with `risk_level=low` AND `category in (docs, reference, guardrail)` skip the evaluator stage entirely. Other categories always run evaluator when `--task-suite` is provided.

**Evaluator→Gate Forwarding**: if evaluator produces an artifact, its path is forwarded to gate via `--evaluation`, enabling RegressionGate to check evaluator verdict.

**Baseline Evaluation**: when `--task-suite` is given, orchestrator first runs evaluator in `--standalone` mode on the current SKILL.md to discover which tasks fail, then injects those failures as `--source` feedback to the generator.

## CLI

```bash
python3 scripts/orchestrate.py \
  --target /path/to/skill \        # REQUIRED: skill directory or file to improve
  --state-root /path/to/state \    # REQUIRED: where artifacts are written
  --source feedback.json \         # repeatable: memory/feedback/trace files
  --max-retries 3 \                # default 3: Ralph Wiggum retry attempts
  --task-suite tasks.yaml \        # enables evaluator stage (real LLM eval)
  --eval-mock                      # evaluator uses mock execution, no claude CLI
```

| Param | Default | When to change |
|-------|---------|---------------|
| `--target` | (required) | Always set — path to the skill dir to improve |
| `--state-root` | (required) | Always set — persistent state/artifact directory |
| `--source` | [] | Add feedback.json, memory files, or prior failure traces |
| `--max-retries` | 3 | Raise to 5 for hard-to-improve skills; lower to 1 for fast iteration |
| `--task-suite` | None | Provide to enable LLM-based evaluator; omit for docs-only changes |
| `--eval-mock` | false | Use in CI/testing to skip real `claude -p` calls |

<example>
正确用法: 对一个 skill 运行全流程改进（含 evaluator）
$ python3 scripts/orchestrate.py --target /path/to/skill --state-root ./state --task-suite tasks.yaml
→ 0. Baseline evaluation: 发现 2 个 task 失败，注入 generator
→ 1. 生成候选 → 2. 多人盲审 → 3. 任务评估 → 4. 执行变更 → 5. 7层门禁
→ 失败时自动注入 trace 重试（最多 3 次）
→ stdout: /path/to/state/pipeline-summary.json
</example>

<anti-example>
错误用法: 只想看评分却用了 orchestrator
$ python3 scripts/orchestrate.py --target /path/to/skill --state-root ./state
→ 会实际执行变更！应该用 improvement-learner 的 self_improve.py
</anti-example>

## Error Handling

- 每个 subprocess 有 1200s 超时，超时抛 RuntimeError
- evaluator 失败不中断流程（打印警告继续），但 evaluation_failure_trace 会注入下轮
- gate 返回 `revert` 时自动调用 `extract_failure_trace()` 写入 `traces/trace-{run_id}.json`
- pipeline-summary.json 最终输出到 `{state-root}/pipeline-summary.json`

## Output

最终输出 `pipeline-summary.json`：
```json
{"target": "/path/to/skill", "attempts": 2, "max_retries": 3,
 "final_decision": "keep", "final_candidate_id": "cand-01-docs",
 "final_artifact_path": "/state/receipts/gate-run001-cand-01.json"}
```

`final_decision` 取值: `keep` | `revert` | `reject` | `pending_promote` | `no_candidates` | `no_accepted_candidates`

## Related Skills

- **improvement-generator**: Produces candidate proposals (stage 1) — orchestrator calls `propose.py`
- **improvement-discriminator**: Multi-reviewer panel scoring (stage 2) — orchestrator calls `score.py`
- **improvement-evaluator**: Task suite execution validation (stage 3) — called only when `--task-suite` provided; baseline failures injected as `--source`
- **improvement-executor**: Applies changes with backup/rollback (stage 4) — orchestrator calls `execute.py`
- **improvement-gate**: 7-layer quality gate (stage 5) — receives `--evaluation` artifact when evaluator ran
