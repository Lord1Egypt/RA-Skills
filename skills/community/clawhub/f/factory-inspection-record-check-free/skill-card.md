## Description:

食品出厂检验与留样台账逐批核对，免费版 6 项，批次检验覆盖、检验项目齐全性、留样期限与销毁日期、同一批次同一检验项目重复登记、合计行逐列复核、空白与日期数值状态非法。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Food production quality, inspection, and compliance staff use this skill to check tabular factory release-inspection and retention-sample ledgers before batch release, monthly quality reviews, audits, or regulator inspections. It reports batch-level issues with source line references and refuses to conclude when required table material is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a user-facing accuracy mismatch around one advertised totals check.

Mitigation: Manually verify batch-count totals and request a corrected version from the publisher before relying on that check for compliance decisions.

Risk: The skill checks ledger text and does not replace a complete food-safety or regulatory compliance review.

Mitigation: Use the output as a local screening aid and have qualified quality or compliance staff review source records, product standards, and audit evidence before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/factory-inspection-record-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON with findings, missing-input messages, executed checks, withheld checks, source line references, and batch identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; the free edition executes six checks and lists withheld checks without fabricating conclusions.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
