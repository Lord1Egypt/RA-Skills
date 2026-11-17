## Description:

电商与平台结算专家 helps users paste e-commerce and platform settlement tables, routes the material to one of 11 local reconciliation checks, and returns line-by-line conclusions with source row references when the required columns are present.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business and finance users can use this skill to check e-commerce platform settlements, refund settlements, commissions, advertising fees, OTA, takeout, and insurance-related settlement tables. It is intended for pasted table text and reports missing columns or ambiguous routing instead of guessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a local trial-use counter for the five-use trial.

Mitigation: Review the local state behavior before deployment if a fully stateless tool is required.

Risk: Settlement conclusions depend on the pasted table headers and available columns.

Mitigation: Provide complete table headers and review missing-column, ambiguous-routing, and unexecuted-check notices before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-ecom-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or JSON reconciliation results, with markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include the selected sub-skill, missing-column notices, unexecuted-check notices, row-referenced findings, and locally computed reconciliation results.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
