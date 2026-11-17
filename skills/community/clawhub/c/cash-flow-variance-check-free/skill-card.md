## Description:

现金流预测与实际差异表逐项核对（净流量复算、差异复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and treasury users use this skill before monthly cash meetings or rolling forecast reviews to check arithmetic consistency in cash-flow forecast-versus-actual variance tables. It focuses on table-level recalculation, totals, duplicates, blanks, and cited findings, not business-cause validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output could be mistaken for broader financial validation or approval.

Mitigation: Use it only for the arithmetic and table-consistency checks it lists, and have finance reviewers assess variance causes, forecasting methods, thresholds, and reporting decisions separately.

Risk: The free-version scope and negative inflow/outflow wording may be confusing.

Mitigation: Review the listed checks, checks not run, and out-of-scope notes before relying on results; treat omitted full-version checks as not performed.

Risk: Cash-flow tables may contain sensitive business data.

Mitigation: Run the local Node-based checker in an approved environment and avoid sharing input files or generated findings outside the intended review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cash-flow-variance-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable console text or structured JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include cited row references, executed free-version checks, checks not run, insufficient-input messages, and local execution status.]

## Skill Version(s):

1.0.54 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
