## Description:

递延所得税台账逐项核对，逐行复算暂时性差异、递延所得税资产与负债余额、本期变动，复核合计行并检测重复与空缺，每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, tax, and audit users use this skill to check deferred-tax ledgers during quarterly and annual close work. It recomputes temporary differences, deferred tax balances, period movements, total rows, duplicate items, and missing fields from user-supplied workpapers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic and internal-consistency checks as a full tax or audit opinion.

Mitigation: Use the output as a review aid only and require qualified finance, tax, or audit review before relying on the workpaper.

Risk: The free edition omits checks such as tax-rate consistency, loss carryforward eligibility, income-tax expense tie-out, and excess deferred tax asset confirmation.

Mitigation: Rely only on the declared free checks and run separate review for withheld checks before making tax or audit decisions.

Risk: Incomplete or malformed input can prevent the checker from reaching a conclusion.

Mitigation: Provide a complete tabular deferred-tax ledger with the expected headers and treat insufficient-input responses as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/deferred-tax-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable CLI text or JSON results with source-line findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on supplied deferred-tax ledger text or JSON; insufficient input produces no conclusion.]

## Skill Version(s):

1.0.55 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
