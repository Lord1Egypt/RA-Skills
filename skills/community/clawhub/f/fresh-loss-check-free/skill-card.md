## Description:

Checks fresh produce loss and stocktake tables for row-level arithmetic, totals, duplicate rows, blanks, and negative quantities, with findings tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, store operations, and inventory staff use this skill during closing, reconciliation, or stocktake review to recheck fresh produce loss tables before acting on the numbers. It is a local table-consistency checker and not an accounting, compliance, or fraud determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on arithmetic table checks as accounting, compliance, inventory policy, or fraud conclusions.

Mitigation: Treat results as table-consistency findings only and review them against internal accounting, stocktake, and loss-reporting procedures before taking action.

Risk: Incomplete or unrecognized table input can prevent the checker from producing a conclusion.

Mitigation: Provide the required table header and columns, review missing-input messages, and rerun after correcting the source table.

Risk: This free version omits some checks described as available only in the full product.

Mitigation: Confirm the executed checks and the not-run checks in the output match the intended review scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/fresh-loss-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON check results with row-referenced findings, summary counts, and listed checks that were not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a local Node.js CLI over copied table text or a JSON input file.]

## Skill Version(s):

1.0.50 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
