---
name: improvement-generator
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
- 把上次失败的 trace 注入下一轮（trace-aware reflection）
- 根据 trace 自动降低上次失败类别的候选优先级
- 结合 memory 和 feedback 多源信号生成高优先级候选
- 批量生成多个 skill 的候选列表供 discriminator 打分
- 在 autoloop 场景下由 orchestrator 自动调用，注入历史 trace
- 手动调试单个 skill 的改进方向时作为独立工具使用
- 对比有/无 trace 生成结果来验证 trace 注入是否生效

## When NOT to Use

- **给候选打分** → use `improvement-discriminator`
- **评估 skill 结构** → use `improvement-learner`
- **全流程** → use `improvement-orchestrator`
- **执行已批准的变更** → use `improvement-executor`
- **门禁验证** → use `improvement-gate`

## Why Trace-Aware Generation Matters

**问题**: 没有 trace 注入时，LLM 每次都从零开始生成候选。如果上一轮在 accuracy 维度失败了，下一轮很可能再次生成相同类别的候选 — 因为 LLM 不知道上次失败了。实测中无 trace 重试的重复失败率高达 60-70%。

**Tradeoff**: trace 注入增加了 prompt 长度（约 200-500 tokens），但大幅降低了重复失败率。Because trace 包含失败维度、失败原因、已尝试策略三个关键信号，generator 可以在生成阶段就避开已知死路，而不是等到 discriminator 打分后才发现。这比 "生成 → 打分 → 发现重复 → 重新生成" 的循环节省 1-2 轮迭代。

## Trace-Aware Generation

```
Previous failure on "accuracy" dimension
  → deprioritize candidates of the same category as the failed one
  → prioritize other dimensions' improvements instead
  → if same category failed ≥2 times, skip entirely and try adjacent dimensions
```

<example>
正确: 第一次失败后注入 trace 重试
$ python3 scripts/propose.py --target /path/to/skill --trace failure_trace.json --output candidates.json
→ 生成的候选会自动避开上次失败的 accuracy 维度策略
</example>

<anti-example>
错误: 失败后不注入 trace 直接重试
→ 没有 trace 信息，generator 无法降低失败类别的优先级，容易重复生成同类候选
→ 失败 ≥3 次的自动跳过逻辑在 improvement-learner 中，不在 generator
</anti-example>

## Trace JSON Structure

trace 文件记录上一轮失败的完整上下文，generator 解析后调整候选优先级：

```json
{
  "iteration": 2,
  "failed_dimension": "accuracy",
  "failed_category": "add_code_examples",
  "failure_reason": "code example added but not syntactically valid",
  "attempted_strategies": ["append_bash_example", "append_python_snippet"],
  "scores_before": {"accuracy": 0.67, "coverage": 0.85},
  "scores_after": {"accuracy": 0.63, "coverage": 0.85}
}
```

generator 收到这个 trace 后会：(1) 把 add_code_examples 类别的优先级降到最低，(2) 从 coverage/trigger_quality 等未失败维度寻找候选，(3) 如果 accuracy 下的其他类别（如 add_output_artifacts）未尝试过则仍可生成。

## CLI

```bash
# Basic generation
python3 scripts/propose.py --target /path/to/skill --output candidates.json

# With failure trace (retry loop)
python3 scripts/propose.py --target /path/to/skill --trace failure.json --output candidates.json

# With memory/feedback sources
python3 scripts/propose.py --target /path/to/skill --source memory.json --output candidates.json
```

## Output Artifacts

| Request | Deliverable |
|---------|------------|
| Generate | JSON array of ranked candidates with category, risk_level, execution_plan |
| With trace | Same format, priorities adjusted based on failure analysis |
| With memory | Candidates informed by historical patterns and past successes |
| With feedback | Candidates prioritized by user correction hotspots |

每个候选的 JSON 结构包含 category（改进类别）、risk_level（low/medium/high）、execution_plan（具体修改步骤）、priority_score（0-1 综合优先级）、trace_adjusted（是否被 trace 调整过优先级）。

## Related Skills

- **improvement-discriminator**: Scores the candidates this skill produces
- **improvement-orchestrator**: Calls generator as stage 1
- **improvement-learner**: Provides evaluation data that informs candidate selection
- **improvement-executor**: Executes the top-ranked candidate approved by gate
- **session-feedback-analyzer**: Generates feedback.jsonl that feeds into candidate prioritization
