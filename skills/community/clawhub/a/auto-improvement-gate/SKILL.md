---
name: improvement-gate
category: review
description: "当执行完变更需要验证是否应保留、候选被标记 pending 需要人工审批、或想查看待审队列时使用。7 层机械门禁: Schema→Compile→Lint→Regression→Review→Doubt→HumanReview，任一 required 层失败即拒绝。不用于打分（用 improvement-discriminator）或执行变更（用 improvement-executor）。"
license: MIT
triggers:
  - quality gate
  - validate candidate
  - gate check
  - human review
  - 门禁验证
  - 待审批
version: 0.1.0
author: OpenClaw Team
---

# Improvement Gate

7-layer mechanical quality gate: any required layer fail = reject/revert.

## When to Use

- 验证已执行的候选是否应保留（gate.py）
- 管理人工审核队列（review.py --list）
- 完成待审批项（review.py --complete）

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`
- **执行文件变更** → use `improvement-executor`
- **评估 skill 结构** → use `improvement-learner`

## 7-Layer Gate

| Layer | Gate | Required | Pass Condition |
|-------|------|----------|---------------|
| 0 | **SchemaGate** | Yes | Candidate has id, category, risk_level, execution_plan |
| 1 | **CompileGate** | Yes | Modified .py files pass `py_compile`; non-Python files auto-pass |
| 2 | **LintGate** | No (advisory) | No lines >120 chars, no mixed tabs/spaces in diff |
| 3 | **RegressionGate** | Yes | Evaluator verdict != "reject" (checks `evaluator_evidence`) |
| 4 | **ReviewGate** | Yes | Discriminator recommendation=accept AND panel not DISPUTED AND LLM judge != reject |
| 5 | **DoubtGate** | Yes | Candidate text has < threshold hedging words (threshold varies by category: docs=2, prompt=4, code=3) |
| 6 | **HumanReviewGate** | No (advisory) | Flags `needs_human=true` for medium/high risk or prompt/workflow/tests/code categories |

**Gate execution**: layers run sequentially. First required-layer failure stops execution and triggers revert (if file was modified) or reject.

## CLI — gate.py

```bash
python3 scripts/gate.py \
  --ranking ranking.json \         # REQUIRED: ranking artifact from discriminator
  --execution execution.json \     # REQUIRED: execution artifact from executor
  --state-root /path/to/state \    # default: lib/state_machine.DEFAULT_STATE_ROOT
  --evaluation eval.json \         # optional: evaluator artifact (forwarded by orchestrator)
  --layers schema,compile,review \ # optional: run only these layers (default: all 7)
  --output receipt.json            # default: auto-generated path
```

| Param | Default | When to change |
|-------|---------|---------------|
| `--layers` | all 7 | Use `schema,compile` for fast structural checks only |
| `--evaluation` | None | Orchestrator passes this automatically when evaluator ran |

## CLI — review.py (Human Review Queue)

```bash
# List pending human reviews
python3 scripts/review.py --state-root /path/to/state --list

# Complete a review
python3 scripts/review.py --state-root /path/to/state \
  --complete review-cand-01-docs \
  --decision approve \             # approve | reject
  --reason "低风险文档变更，LGTM" \
  --reviewer engineer-name         # default: cli-user
```

## 4-Way Decision Logic (after all required layers pass)

| Condition | Decision | Action |
|-----------|----------|--------|
| `accept_for_execution` + low-risk docs/reference/guardrail + success | **keep** | File stays modified |
| `recommendation=reject` | **revert** | Restore backup, append to veto log |
| `recommendation=hold` OR non-auto-keep-eligible | **pending_promote** | Restore backup, create review request |
| `execution.status=unsupported` | **reject** | No file change, log reason |

如果 HumanReviewGate 标记 `needs_human=true`，即使 keep eligible 也会升级为 `pending_promote`。

<example>
正确: gate 返回 pending_promote → 查审批队列 → 人工批准
$ python3 scripts/review.py --state-root ./state --list
→ ID: review-cand-01-docs  Category: docs  Risk: low  Since: 2025-01-15T10:00:00Z
$ python3 scripts/review.py --state-root ./state --complete review-cand-01-docs --decision approve --reason "confirmed safe"
→ Review review-cand-01-docs completed: approve
</example>

<anti-example>
错误: gate 返回 revert 后仍然保留文件变更
→ revert 时 gate 自动调用 restore_backup()，原文件已恢复。不要手动跳过。
</anti-example>

## Output — Gate Receipt

```json
{"decision": "keep", "reason": "low-risk docs candidate executed successfully",
 "gate_layers": {"all_passed": true, "layers_run": 7, "layer_results": [...]},
 "rollback": {"attempted": false}, "next_step": "propose_candidates", "next_owner": "proposer"}
```

## Related Skills

- **improvement-discriminator**: ReviewGate checks its panel consensus + LLM verdict
- **improvement-executor**: Gate validates executor output; reverts via `rollback_pointer`
- **improvement-evaluator**: RegressionGate checks evaluator verdict when `--evaluation` provided
- **improvement-orchestrator**: Calls gate as stage 5, forwards evaluator artifact
- **benchmark-store**: Pareto front data consumed by RegressionGate
