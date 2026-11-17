## Description:

A local Node.js skill that checks construction output value and progress confirmation tables for calculation consistency, totals, duplicate rows, blank placeholders, and negative amounts, with findings tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, commercial teams, and finance staff use this skill before monthly construction output or progress confirmation to recalculate table values, check totals, and identify missing or inconsistent entries. It supports review of user-provided table text or JSON, but does not replace contract, finance, cost-estimation, or site-supervision judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks construction accounting table consistency, but its results could be mistaken for contract, finance, cost-estimation, or site-supervision approval.

Mitigation: Use the output as a review aid and have qualified project, finance, or supervision staff confirm contract interpretation and final decisions.

Risk: Incomplete or malformed table input can prevent reliable checks or omit relevant issues.

Mitigation: Provide the full table with headers and review any missing-material guidance before relying on the result.

Risk: The free version intentionally omits several checks available in the full tool.

Mitigation: Review the listed withheld checks and run additional review when those checks are relevant to the project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/construction-output-value-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON results from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing-material guidance instead of a conclusion.]

## Skill Version(s):

1.0.53 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
