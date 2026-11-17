# Research Retrospective Protocol

Use this protocol when the user asks whether a completed research run was good, weak, shallow, or worth improving.

The goal is to turn a real output into a small improvement loop, not to defend the previous answer.

## Inputs

Use any available combination:

- the user's original research request.
- the delivered research output.
- the method stack that was used or implied.
- evidence gaps, source list, or browsing constraints.
- the user's reaction, such as "too shallow", "good but not official enough", or "can this be better?"

If the prior output is not available in context, evaluate from the visible summary and state the limitation.

## Scorecard

Score from 1-10, with one-sentence evidence for each score. For ship / revise / rerun decisions, use [report-quality-rubric.json](report-quality-rubric.json).

- `question-fit`: did the output answer the user's actual decision or understanding need?
- `method-fit`: did the chosen method stack match the object type and stakes?
- `evidence-strength`: were sources authoritative, current, independent, and traceable?
- `formal-status-clarity`: when official status matters, did the output separate final, applicable, draft, political-agreement, voluntary, trial, and institution-specific claims?
- `depth-and-mechanism`: did the output explain causes, transitions, tradeoffs, and why it matters?
- `dissent-and-gaps`: did it name contrary evidence, weak spots, and reversal conditions?
- `actionability`: did it give useful next steps, monitoring signals, or reusable assets?
- `composition-quality`: did the output use the right blocks without overfilling a fixed template?

## Diagnosis

Classify each issue as:

- `missing-method`: a method should have been added.
- `weak-source`: source quality, freshness, or independence was insufficient.
- `thin-analysis`: facts were present but mechanism or implication was shallow.
- `scope-drift`: the output answered an adjacent question.
- `over-templated`: blocks appeared because the template had them, not because they changed the answer.
- `under-composed`: a needed block was missing.
- `unsupported-claim`: a load-bearing claim lacked citation traceability.
- `status-confusion`: a draft, political agreement, voluntary code, trial, or institution rule was phrased as final or generally applicable.

## Improvement Plan

Produce a compact plan:

1. What to keep.
2. What to fix next.
3. Which method or block to add.
4. Which evidence to collect or re-check.
5. Whether the skill itself needs a rule, asset, eval, or only better execution.

Do not rewrite the whole research report unless the user asks. The retrospective should identify the next highest-leverage change.

## Skill Improvement Feedback

The retrospective output must include a structured `skill_improvement_feedback` section. This closes the loop between retrospective diagnosis and skill iteration.

```yaml
skill_improvement_feedback:
  # 最高杠杆改进项
  top_fix: "一句话描述最该改什么"

  # 改进类型：rule（改 references 规则）、asset（改 assets 模板/模块）、eval（改 evals）、execution（仅执行层，不改 skill）
  fix_type: "rule | asset | eval | execution"

  # 具体改进建议
  suggestion: "具体到文件和字段的改进描述"

  # 预期影响：改进后哪个评分维度会提升
  expected_dimension_improvement: "evidence-strength | depth-and-mechanism | ..."

  # 是否建议重跑 evals 验证改进效果
  rerun_evals: true | false

  # 可选：建议重跑的 eval ID
  rerun_eval_ids: [1, 9, 13]
```

### 迭代闭环

当 `rerun_evals = true` 时，使用自动化脚本执行改进闭环：

1. 将 `skill_improvement_feedback` 写入 `.skill-iterations/` 工作区（JSON 格式，文件名 `{timestamp}-{short-description}.json`）。
2. 运行 `python scripts/iterate_skill.py --list` 查看待处理的改进项。
3. 为 LLM 型研究输出准备一个行为评测命令，并运行：
   `python scripts/iterate_skill.py --apply <file> --behavior-command 'python /path/to/judge.py --phase {phase} --skill {skill_dir} --output {output}'`。
   评测命令必须写出 `{"executed": true, "items": [{"id": 1, "passed": true}]}` 形状的 JSON；`{phase}` 会分别替换为 `baseline` 与 `post`，`{eval_ids}` 可用于接收逗号分隔的目标 ID。每个目标 ID 必须且只能出现一次：指定 `--eval-ids` 时须精确覆盖该子集，未指定时须覆盖完整 eval 语料；缺失、重复或越界 ID 都会 fail closed。未提供可执行行为评测时，脚本会在结构 benchmark 之后中止，不会把结构合法性计成行为分数。
   - 脚本先运行结构 benchmark，再运行基线行为评测
   - 提示应用改进到对应的 skill 文件（references / assets / evals）
   - 运行改进后结构 benchmark 与行为评测并对比
   - 输出 GO / HOLD / NO-GO 建议
4. 如果 benchmark 分数提升（GO），更新 VERSION 并标记为可提交。
5. 如果分数未提升（NO-GO），回退改进；脚本自动记录到 `.skill-iterations/_history.json`。
6. 同一改进项最多尝试 3 次（`--max-iterations`，默认 3），超限后强制停止。

可使用 `--eval-ids 1,9,13` 只关注特定 eval 的结果变化。行为评测命令应对相同 eval 集合保持稳定；脚本会在读入证据后再按 ID 过滤。

这样 retrospective 不再是一次性文本输出，而是可持久化、可验证、可迭代的自改进 loop。
