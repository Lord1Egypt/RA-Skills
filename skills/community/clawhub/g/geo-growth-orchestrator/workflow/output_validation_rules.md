# Output Validation Rules

Every orchestration stage must validate expected outputs before the final report is generated.

## Stage Status Values

| Status | Meaning |
|---|---|
| `success` | All required outputs exist and pass minimum content checks |
| `partial` | Some outputs exist, but at least one expected output is missing or incomplete |
| `failed` | The stage could not produce usable output |
| `skipped` | The stage was intentionally skipped with a valid reason |
| `manual` | The stage requires manual work because no callable Skill exists |
| `future_skill` | The platform or action is planned for a future Skill |

## Required Validation Behavior

For each stage:

1. Read the registry or workflow definition for `expected_outputs`.
2. Check whether each expected artifact exists or has been provided by the user.
3. If any required output is missing, do not mark the stage as `success`.
4. Record missing artifacts in `orchestrator_run_summary.missing_outputs`.
5. Produce a fallback artifact or fallback instruction.
6. Reflect the stage status in both the internal audit report and final delivery package.

## Missing Output Handling

If an output is missing:

- Do not pretend the Skill ran successfully.
- Mark the stage as `failed` or `partial`.
- Name the missing file or artifact.
- Explain what can still be delivered.
- Provide a next-step remediation action.
- In the customer report, express this as “尚未完成 / 建议补充 / 下一步补救动作”.
- In the internal report, keep exact missing filenames, status values, evidence level, and failure details.

## Customer Report Wording

Use customer-friendly wording:

- `blocked` -> “建议补充资料后发布”
- `manual_check` -> “建议人工确认”
- `inferred_estimate` -> “基于当前资料的初步判断”
- `failed` -> “该阶段尚未完成”
- `partial` -> “已完成基础版本，仍需补齐部分资料”

Do not expose API configuration, schema validation, stack traces, or internal debug text in customer-facing reports.

## Internal Report Requirements

The internal audit report must preserve:

- Exact stage status.
- Missing file paths.
- Evidence level.
- Risk and compliance notes.
- API and runtime availability.
- Schema validation results.
- Fallback behavior.
- Version and debug details when relevant.

## Final Report Gate

The Orchestrator must not end with only:

> 已完成，文件在某目录。

The final answer or generated final report must include:

1. 老板能看懂的 3 句话结论。
2. 本次调用或建议调用了哪些相邻 Skill。
3. 每个 Skill 的执行状态。
4. 核心 GEO 盲区。
5. 已生成或应生成的内容资产。
6. 建议发布顺序。
7. 30 天复测计划。
8. 完整文件路径清单。
9. 如果某些相邻 Skill 未能调用或输出缺失，明确说明。
