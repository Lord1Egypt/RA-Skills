---
name: improvement-generator
category: tool
description: "当需要为目标 skill 生成改进候选、把上次失败信息注入下一轮生成、或分析历史记忆模式来避免重复失败时使用。支持 --trace 注入失败上下文。不用于打分（用 improvement-discriminator）或评估（用 improvement-learner）。"
license: MIT
triggers:
  - generate candidates
  - propose improvements
  - 生成候选
  - 改进建议
version: 0.1.0
author: OpenClaw Team
---

# Improvement Generator

Produces ranked improvement candidates from target analysis, feedback signals, and failure traces.

## When to Use

- 为目标 skill 生成结构化改进候选
- 把上次失败的 trace 注入下一轮（GEPA trace-aware）
- 根据记忆模式避开已经失败过 >=3 次的策略

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`
- **评估 skill 结构** → use `improvement-learner`
- **全流程** → use `improvement-orchestrator`

## CLI

```bash
python3 scripts/propose.py \
  --target /path/to/skill \        # REQUIRED: skill directory or single file
  --state-root /path/to/state \    # default: lib/state_machine.DEFAULT_STATE_ROOT
  --source memory.json \           # repeatable: feedback/memory/baseline-failures sources
  --max-candidates 4 \             # default 4: max candidates to generate
  --trace failure_trace.json \     # inject prior failure trace for retry prioritization
  --run-id custom-run-id \         # default: auto-generated from target
  --output candidates.json \       # default: {state-root}/candidate_versions/{run-id}.json
  --lane generic-skill             # default: generic-skill
```

| Param | Default | When to change |
|-------|---------|---------------|
| `--max-candidates` | 4 | Lower to 2 for fast iteration; raise for diverse exploration |
| `--trace` | None | Pass when retrying after gate revert — deprioritizes failed category |
| `--source` | [] | Add feedback.jsonl, memory files, or evaluator baseline-failures.json |
| `--run-id` | auto | Set explicitly when integrating with external tracking |

## 6 Candidate Categories

| Category | Risk | Executor Support | Description |
|----------|------|-------------------|-------------|
| `docs` | low | Yes (`append_markdown_section`) | Append operator notes/limitations to Markdown docs |
| `reference` | low | Yes (`append_markdown_section`) | Add control-plane-friendly notes to reference files |
| `guardrail` | low | Yes (`append_markdown_section`) | Add conservative auto-promote rules to guardrail docs |
| `prompt` | medium | No | SKILL.md prompt restructure (requires manual review) |
| `workflow` | medium | No | Workflow adapter/orchestration hook changes |
| `tests` | medium | No | Smoke-check/validation test cases |

## Trace-Aware Generation

When `--trace` is provided, `adjust_candidates_from_trace()` deprioritizes the category that failed in the prior run and boosts alternatives:
```
failure_trace.json: {"candidate_id": "cand-01-docs", "reason": "gate rejected"}
→ docs candidates moved to end, reference/guardrail candidates boosted to front
```

## Evaluator-Driven Fix (`_find_evaluator_failures` + `_llm_propose_skill_fix`)

When `--source` includes a `baseline-failures.json` (type=`evaluator_baseline_failures`), the generator:
1. Reads failed task details (task_id, score, error)
2. Sends current SKILL.md + failures to `claude -p` to get a targeted fix
3. Returns an `eval-fix` candidate as highest priority (risk_level=low, executor_support=True)

## Correction Hotspots (`_find_correction_hotspots`)

Scans feedback.jsonl sources for user correction events (`outcome=correction|partial`). Returns `dimension_hint → count` mapping used to prioritize candidates that address the most-corrected dimensions.

<example>
正确: 第一次生成 + 有 evaluator baseline failures
$ python3 scripts/propose.py --target /path/to/skill --source baseline-failures.json --state-root ./state
→ 候选 1: LLM-proposed SKILL.md fix targeting failed tasks (category=prompt, risk=low)
→ 候选 2-4: template candidates (docs, reference, guardrail)
→ stdout: /state/candidate_versions/run-001.json
</example>

<anti-example>
错误: 同一个 category 失败 3 次后还继续重试
→ 应该用 --trace 注入失败信息让 generator 自动切换到其他 category
</anti-example>

## Output Artifact

```json
{"schema_version": "1.0", "run_id": "...", "stage": "proposed",
 "candidates": [{"id": "cand-01-docs", "category": "docs", "risk_level": "low",
   "execution_plan": {"action": "append_markdown_section", "section_heading": "## Operator Notes",
     "content_lines": ["..."]}, ...}],
 "failure_trace_used": false, "truth_anchor": "/state/candidate_versions/run-001.json"}
```

## Related Skills

- **improvement-discriminator**: Scores the candidates this skill produces → called by orchestrator as stage 2
- **improvement-orchestrator**: Calls generator as stage 1, passes `--source` with failure traces
- **improvement-evaluator**: Baseline failures fed back as `--source` to inform candidate generation
