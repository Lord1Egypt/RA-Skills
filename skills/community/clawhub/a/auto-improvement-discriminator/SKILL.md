---
name: improvement-discriminator
category: review
description: "当需要对改进候选多人盲审打分、用 LLM 做语义评估、判断候选是否应被接受、或打分结果全是 hold 想知道为什么时使用。支持 --panel 多审阅者盲审和 --llm-judge 语义评估。不用于结构评估（用 improvement-learner）或门禁决策（用 improvement-gate）。"
license: MIT
triggers:
  - score candidate
  - evaluate improvement
  - multi-reviewer panel
  - LLM judge
  - 候选打分
  - 盲审
version: 0.1.0
author: OpenClaw Team
---

# Improvement Discriminator

Multi-signal scoring engine. Blends heuristic rules, evaluator rubrics, LLM-as-Judge, and multi-reviewer blind panel to score, rank, and recommend actions on improvement candidates.

## When to Use / NOT to Use

- Score and rank candidates, run panel blind review, run LLM-as-Judge semantic evaluation, diagnose `hold` results
- **NOT** for structural evaluation (improvement-learner), gate decisions (improvement-gate), or file changes (improvement-executor)

## CLI

```
python3 scripts/score.py --input CANDS.json [--output SCORED.json] [--state-root DIR]
  [--panel] [--llm-judge {claude,openai,mock}] [--use-evaluator-evidence]
```

| Param | Description |
|-------|-------------|
| `--input` | Required. Candidate artifact JSON from generator |
| `--output` | Output path. Default: `{state-root}/rankings/{run_id}.json` |
| `--state-root` | State directory. Default: `state/` |
| `--panel` | Enable 4-reviewer blind panel (structural, conservative, user_advocate, security_auditor) |
| `--llm-judge` | Enable LLM-as-Judge. Backends: `claude` (Anthropic API), `openai`, `mock` (deterministic, no key) |
| `--use-evaluator-evidence` | Blend skill-evaluator rubric/category/boundary evidence |

## Scoring Modes and Blending Weights

| Mode | Blending |
|------|----------|
| Heuristic only (default) | 100% heuristic (base 4.0 + category bonus + source refs - risk penalty) |
| `--use-evaluator-evidence` | 70% heuristic + 30% evaluator |
| `--llm-judge` | 60% heuristic + 40% LLM |
| Both flags | 50% heuristic + 30% LLM + 20% evaluator |
| `--panel` | 4 reviewers score independently; cognitive label decides final recommendation |

Category bonuses: docs=4.0, reference=3.5, guardrail=3.5, workflow=1.5, tests=1.5, prompt=1.0.
Risk penalties: low=0.0, medium=2.0, high=4.5. Protected path adds +2.5.

## Multi-Reviewer Panel

| Reviewer | Focus | Risk Sensitivity |
|----------|-------|-----------------|
| structural | docs (5.0), reference (4.0) | 1.0x |
| conservative | guardrail (5.0), penalizes prompt (0.5) | 1.5x |
| user_advocate | workflow (4.0), prompt (3.0) | 0.8x |
| security_auditor | guardrail (5.0), tests (3.0) | 2.0x |

Cognitive labels: **CONSENSUS** (all agree) -> shared recommendation. **VERIFIED** (2+ agree) -> majority. **DISPUTED** (no majority) -> forced `hold`.

## LLM Judge

Evaluates 4 dimensions (0.0-1.0): clarity, specificity, consistency, safety.
Thresholds: approve >= 0.75, reject < 0.40, else conditional.

| Backend | Model | Key | Fallback |
|---------|-------|-----|----------|
| claude | claude-sonnet-4-20250514 | `ANTHROPIC_API_KEY` (supports `ANTHROPIC_BASE_URL`) | mock |
| openai | gpt-4o-mini | `OPENAI_API_KEY` | mock |
| mock | none | none | deterministic, confidence=0.5 |

## Blockers

`protected_target`, `executor_not_supported`, `not_auto_keep_category`, `risk_medium`/`risk_high`, `skill_level_insufficient_for_structural_change`, `evaluator_reject`, `llm_judge_reject`

## Output JSON Example

```json
{
  "run_id": "abc-123", "stage": "ranked", "critic_mode": "multi-reviewer-panel",
  "scored_candidates": [{
    "id": "cand-001", "score": 7.25, "recommendation": "accept_for_execution",
    "blockers": [], "judge_notes": ["低风险候选，可交给 executor。"],
    "panel": {
      "panel_reviews": [{"reviewer": "structural", "score": 8.5}, {"reviewer": "conservative", "score": 6.0}],
      "cognitive_label": "CONSENSUS", "aggregated_score": 7.25
    },
    "llm_verdict": {"score": 0.82, "decision": "approve",
      "dimensions": {"clarity": 0.85, "specificity": 0.80, "consistency": 0.80, "safety": 0.90}}
  }],
  "summary": {"accept_for_execution": 1, "hold": 0, "reject": 0}
}
```

<example>
Panel + LLM judge:
$ python3 scripts/score.py --input candidates.json --panel --llm-judge mock --output scored.json
</example>

<anti-example>
--panel and --llm-judge are NOT mutually exclusive. Each reviewer independently calls the LLM judge.
</anti-example>

## Related Skills

- **improvement-generator** -- produces candidates | **improvement-gate** -- keep/revert/reject
- **improvement-learner** -- structural 6-dim eval | **benchmark-store** -- frozen baselines
