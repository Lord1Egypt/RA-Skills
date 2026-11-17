## Description:

固定资产盘点表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations employees use this skill during month-end close, reconciliation, or inventory counts to check fixed-asset inventory tables for arithmetic inconsistencies, totals, duplicate asset IDs, blank fields, and unsupported inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker is limited to the disclosed free fixed-asset consistency checks and does not perform full accounting, tax, or ERP validation.

Mitigation: Use it as a local consistency aid, and have qualified finance staff review outputs and separately validate policy, tax, ERP, and checks outside the free scope.

Risk: The skill processes fixed-asset inventory data using a local Node script.

Mitigation: Run it only in an environment where local processing of that data is acceptable and review the input file before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/fixed-asset-count-check-free)
- [ClawHub publisher profile: chenqg618](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or JSON results with findings, scope, summaries, and cited evidence fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over a user-provided fixed-asset table; insufficient input returns missing fields instead of conclusions.]

## Skill Version(s):

1.0.52 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
