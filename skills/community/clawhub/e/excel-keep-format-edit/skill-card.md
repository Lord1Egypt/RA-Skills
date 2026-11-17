## Description:

Guides agents to edit values in a copy of a local Excel workbook while preserving its layout and checking financial statement totals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Accountants and analysts use this guidance to update values in copied legacy Excel financial statements without rebuilding their formatting, then check that totals and balances reconcile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editing the wrong workbook, sheet, or cell could change financial figures incorrectly.

Mitigation: Work on a copy and confirm the workbook, sheet, and labeled cell locations before writing values.

Risk: Recalculation may leave static totals unchanged or produce financially inconsistent statements.

Mitigation: Check whether totals contain formulas, update static totals as needed, verify balances, and review accounting assumptions before relying on the result.

## Reference(s):

- [Excel Keep Format Edit on ClawHub](https://clawhub.ai/lingyu9495-source/skills/excel-keep-format-edit)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for local Windows and Microsoft Excel; execution can produce an edited copy of a workbook.]

## Skill Version(s):

1.1.2 (source: server-resolved release metadata; embedded frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
