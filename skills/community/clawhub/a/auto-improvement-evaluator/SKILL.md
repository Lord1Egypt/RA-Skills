---
name: improvement-evaluator
category: tool
description: "当需要验证 Skill 改进是否真正提升了 AI 执行效果时使用。通过预定义任务集（YAML）运行 AI 任务，判定 pass/fail，输出 execution_pass_rate。不用于文档结构评分（用 improvement-learner）或候选打分（用 improvement-discriminator）。"
license: MIT
triggers:
  - evaluate skill execution
  - run task suite
  - execution pass rate
  - 执行效果评估
  - 任务集验证
version: 0.1.0
author: OpenClaw Team
---

# Improvement Evaluator

Measures whether a Skill actually makes AI perform better on real tasks.

## When to Use
- Verify that a SKILL.md change improves AI task execution (not just document structure)
- Run a task suite against a candidate SKILL.md and compare with baseline
- Get execution_pass_rate as a concrete quality metric
- Run standalone evaluation on current SKILL.md to discover baseline failures

## When NOT to Use
- **只想检查 SKILL.md 结构质量** → use `improvement-learner`
- **只想给候选打分** → use `improvement-discriminator`
- **跑全流程** → use `improvement-orchestrator`

## 2 Modes

| Mode | When | Required Params |
|------|------|-----------------|
| **Pipeline** | Called by orchestrator after discriminator | `--input`, `--candidate-id`, `--task-suite`, `--state-root` |
| **Standalone** | Direct evaluation of current SKILL.md | `--standalone`, `--task-suite`, `--state-root`, `--skill-path` |

## CLI

```bash
# Pipeline mode: evaluate candidate vs baseline
python3 scripts/evaluate.py --input ranking.json --candidate-id cand-01-docs \
  --task-suite tasks.yaml --state-root ./state \
  [--pass-k 1] [--eval-threshold 6.0] [--baseline-cache-dir /cache] [--mock] [--output eval.json]

# Standalone mode: evaluate current SKILL.md directly
python3 scripts/evaluate.py --standalone --task-suite tasks.yaml \
  --state-root ./state --skill-path /path/to/skill [--mock]
```

| Param | Default | When to change |
|-------|---------|---------------|
| `--eval-threshold` | 6.0 | Orchestrator sets per-category thresholds (e.g., docs=5.0, prompt=7.0) |
| `--pass-k` | 1 | Raise to 3 for flaky tasks |
| `--mock` | false | Use in CI or when `claude` CLI is not installed |
| `--baseline-cache-dir` | None | Set to avoid re-running baseline on unchanged SKILL.md |

## 3 Judge Types

| Judge | `type` in YAML | Mechanism | Use When |
|-------|----------------|-----------|----------|
| **ContainsJudge** | `contains` | Check output contains all strings in `expected` list | Deterministic keyword/format checks |
| **PytestJudge** | `pytest` | Run pytest on `fixtures/{test_file}` against AI output | Structured output validation (JSON, code) |
| **LLMRubricJudge** | `llm-rubric` | LLM scores output against `rubric` text (mock mode: random pass) | Semantic quality evaluation |

## Task Suite YAML Format

```yaml
skill_id: my-skill
version: "1.0"
tasks:
  - id: task-001
    prompt: "Given X, produce Y"
    judge: {type: contains, expected: ["keyword1", "keyword2"]}
  - id: task-002
    prompt: "Generate a config file"
    judge: {type: pytest, test_file: fixtures/test_config.py}
  - id: task-003
    prompt: "Explain concept Z"
    judge: {type: llm-rubric, rubric: "Must cover A, B, C with examples"}
```

## Conditional Evaluation

- **Score threshold**: candidates with discriminator score < `--eval-threshold` are skipped (verdict=`skipped`)
- **Baseline abort**: if baseline pass_rate < 0.2 (20%), evaluation aborts with verdict=`error` — indicates broken task suite
- **Baseline caching**: SHA256(skill_content + suite_path) → 7-day TTL cache to avoid re-running unchanged baselines

<example>
Pipeline mode: candidate vs baseline comparison
$ python3 scripts/evaluate.py --input ranking.json --candidate-id c1 --task-suite tasks.yaml --state-root ./state
→ Candidate pass rate: 0.80 (4/5 tasks passed)
→ Baseline pass rate: 0.60 (3/5 tasks passed)
→ {"execution_pass_rate": 0.80, "baseline_pass_rate": 0.60, "delta": 0.20, "verdict": "pass"}
</example>

<anti-example>
Using evaluator without task suite:
→ Evaluator requires --task-suite. Without it, orchestrator skips evaluator entirely.
→ No --standalone without --task-suite either — both modes require it.
</anti-example>

## Output Artifact

```json
{"stage": "evaluated", "verdict": "pass",
 "evaluation": {"execution_pass_rate": 0.80, "baseline_pass_rate": 0.60, "delta": 0.20},
 "candidate_results": [{"task_id": "t1", "passed": true, "score": 1.0}],
 "next_step": "gate_decision", "next_owner": "gate"}
```

## Related Skills

- **improvement-discriminator**: Provides scores; evaluator checks `score >= eval_threshold`
- **improvement-gate**: RegressionGate checks evaluator verdict via `--evaluation` artifact
- **improvement-orchestrator**: Calls evaluator as stage 3; runs standalone baseline, injects failures to generator
- **improvement-generator**: Consumes baseline-failures.json for targeted SKILL.md fixes
