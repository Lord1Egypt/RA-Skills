## Description:

供应商对账表逐项核对，执行逐行算术、合计勾稽、重复与空缺检测，并为每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, warehouse, and operations staff use this skill during month-end, payroll, reconciliation, or inventory checkpoints to verify supplier AP reconciliation tables. It checks supplier-level ending payable arithmetic, counterpart reconciliation amounts, non-zero differences, totals, duplicate suppliers, and blank or placeholder cells.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier reconciliation tables can include sensitive accounting data.

Mitigation: Run the skill only on necessary pasted or exported table text, and avoid providing unrelated confidential contracts or legal materials.

Risk: The free version intentionally omits several accounting checks, including payment-direction anomalies and difference-rate thresholds.

Mitigation: Treat results as coverage for the listed free checks only, and review withheld checks separately before relying on the reconciliation.

Risk: Insufficient or malformed input can make the tool unable to reach a conclusion.

Mitigation: Provide supplier reconciliation text with headers and required amount columns; when input is insufficient, use the returned missing-field guidance instead of treating the run as clean.

Risk: The tool checks arithmetic and reconciliation consistency but does not determine whether supplier statements are authentic or whether payment should be approved.

Mitigation: Use the output as a reconciliation aid and keep payment approval, authenticity checks, audit, tax, and legal review in the responsible business process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ap-reconciliation-free)

## Skill Output:

**Output Type(s):** [analysis, json, markdown, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON containing reconciliation findings, summaries, executed checks, withheld checks, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows when input is sufficient; insufficient input returns missing requirements instead of a clean result.]

## Skill Version(s):

1.0.61 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
