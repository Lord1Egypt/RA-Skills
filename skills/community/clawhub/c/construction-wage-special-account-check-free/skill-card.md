## Description:

建筑工人工资专户发放核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External construction payroll, labor-management, and finance users can run local checks before monthly special-account wage payouts. The skill reviews a provided construction worker wage special-account table for arithmetic, totals, duplicate rows, blanks, placeholders, and negative values, while citing the source text for findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release can produce a no-issue result even though special-account payout-total reconciliation is listed as not run.

Mitigation: Treat checks_not_run as out of scope, manually compare net_total and payout_total, or use a version that explicitly implements that reconciliation.

Risk: The input may contain sensitive wage and identity data.

Mitigation: Run the checker only in an environment approved for payroll data and avoid uploading source materials to untrusted systems.

Risk: Incomplete or unrecognized table input prevents a reliable conclusion.

Mitigation: Provide the wage special-account table with headers and source rows; treat insufficient-input output as no conclusion rather than clearance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/construction-wage-special-account-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or structured JSON findings with source-cited payroll reconciliation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without network access; exits with insufficient-input status instead of producing a no-issue conclusion when required table content is missing.]

## Skill Version(s):

1.0.53 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
