## Description:

本技能本地核对中文预算执行表，执行逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and operations staff use this skill during monthly close, reconciliation, or inventory checkpoints to check whether budget execution table arithmetic and rollups are internally consistent. It is a local deterministic checker, not a full audit or budget reasonableness review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release omits disclosed checks, including execution-rate, cumulative-actual, negative-value, range, and sign-direction checks.

Mitigation: Review the disclosed withheld checks and use a complete workflow or manual finance review before relying on results for month-end or management decisions.

Risk: Findings depend on user-provided table text and required headers being present.

Mitigation: Provide the budget execution table with headers; treat an insufficient-input result as no conclusion rather than as a clean result.

Risk: The skill checks deterministic arithmetic and table consistency, not audit completeness or business reasonableness.

Mitigation: Have a qualified finance reviewer verify material decisions against the source table and applicable accounting process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/budget-variance-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON report with cited budget-table findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports insufficient input instead of fabricating conclusions; the free version lists checks it did not run.]

## Skill Version(s):

1.0.58 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
