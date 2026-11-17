## Description:

固定资产台账逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, warehouse, and operations staff use this skill to locally check fixed-asset depreciation ledgers during monthly closing, payroll, reconciliation, or inventory review. It verifies arithmetic relationships, totals, duplicates, and blank placeholders, and cites source lines for findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic findings as accounting, audit, tax, policy, or physical asset verification advice.

Mitigation: Use the skill as a local ledger arithmetic checker only, and have qualified staff review accounting policies, audit conclusions, tax positions, impairment questions, and physical asset existence.

Risk: The free version omits several checks, including over-depreciation, accumulated depreciation caps, zero-depreciation anomalies, and residual-rate range validation.

Mitigation: Review the listed omitted checks before relying on results, and run additional controls or the appropriate full workflow when those checks are required.

Risk: Missing or unrecognized ledger input can otherwise lead to misleading reassurance.

Mitigation: The skill reports insufficient input instead of issuing a no-finding conclusion; users should provide a ledger with recognizable headers and source rows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenqg618/skills/depreciation-check-free)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text or JSON with line-cited depreciation check findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally; reports insufficient input instead of drawing conclusions when required ledger material is missing.]

## Skill Version(s):

1.0.51 (source: evidence.json release.version and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
