## Description:

外贸与出口专家 covers six export-trade review workflows, routes pasted table data to the matching sub-skill, and returns row-level conclusions with source-line support while declining to conclude when required columns are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Trade, export-operations, finance, and compliance reviewers can paste tabular materials for export declaration, foreign-exchange collection, tax-refund documentation, monthly self-checks, and settlement reconciliation. The skill helps route the material to the relevant checklist and produce reproducible, source-linked review output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes pasted business tables locally and may handle sensitive trade, tax, settlement, or reconciliation data.

Mitigation: Review the package before installation, run it in an appropriate local environment, and avoid supplying unnecessary confidential data.

Risk: A persistent local five-use counter and subscription prompt are under-disclosed in the listing evidence.

Mitigation: Inform users that the skill can write a counter at ~/.trade-expert/uses and may stop after five free uses.

Risk: Tax, customs, settlement, and reconciliation findings may be incomplete or outside the skill's declared checks.

Mitigation: Treat output as review assistance only, confirm conclusions against official records and qualified human review, and check reported missing columns or unexecuted checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-trade-pub)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or plain text, with optional JSON output from the command-line interface]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include the selected sub-skill, row-level findings, missing-column notices, and non-executed checks when inputs are incomplete.]

## Skill Version(s):

1.0.10 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
