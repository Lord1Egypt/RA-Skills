## Description:

Checks pasted healthcare and pharmaceutical operations tables across eight reconciliation workflows, automatically routes the input to the matching check, and returns row-level findings with source references when the supplied columns are sufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare operations, finance, audit, and compliance users can paste exported table data to triage one of eight healthcare and pharmaceutical reconciliation checks and receive reproducible findings tied to source rows. The skill supports preliminary table consistency review and should not be treated as complete compliance certification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent local usage state and enforces a paid-use gate that the main skill documentation does not clearly disclose.

Mitigation: Review payment and usage-state behavior before installing, disclose it to users, and avoid deployment where hidden local state or paid-use gating is unacceptable.

Risk: Healthcare, reimbursement, audit, inventory, or appeal findings could be mistaken for complete compliance certification.

Mitigation: Treat outputs as preliminary table checks and independently verify conclusions with qualified reviewers and authoritative source systems.

Risk: Insufficient columns, ambiguous routing, or missing optional parameters can leave checks unexecuted or prevent conclusions.

Mitigation: Provide complete table headers and required parameters, inspect any missing-column or unexecuted-check notices, and do not interpret absence of findings as absence of issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-healthcare-pub)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON check results with row-level findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May list missing columns, ambiguous routing candidates, unexecuted checks, and source row references.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
