## Description:

This skill performs local checks on Chinese-language construction material requirement-versus-consumption tables, recalculating loss quantity and loss rate, comparing caps, reconciling totals, and flagging duplicate or incomplete rows with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project material staff, construction managers, cost accountants, and budget reviewers use this skill to check construction material requirement-versus-consumption tables before monthly inventory, cost collection, or limited-material settlement. It helps identify arithmetic inconsistencies, excess consumption indicators, duplicate rows, missing required fields, and insufficient input without making legal, contractual, or on-site factual determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs arithmetic and table consistency checks, not legal, contractual, quota, accounting-policy, or on-site factual verification.

Mitigation: Review findings against contracts, construction quotas, material ledgers, return records, and site evidence before using them for settlement, penalties, or formal decisions.

Risk: Inputs outside the intended Chinese-language construction material comparison table workflow may be incomplete or misinterpreted.

Mitigation: Use the documented required columns and sample table shape; when the skill reports insufficient input, provide the missing headers and source rows instead of relying on default assumptions.

Risk: A clean scan does not remove the need to review generated conclusions before operational use.

Mitigation: Run the skill locally as intended and manually review the row-level formulas, source-line references, and summary before acting on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/construction-material-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Chinese-language plain text or JSON check report with row-level findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include status, missing-input advice, summary totals, executed check scope, row references, formulas, and local/no-network scope indicators.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
