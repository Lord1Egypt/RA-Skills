## Description:

Analyze BigQuery query patterns and storage to dramatically reduce the #1 surprise GCP cost driver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, data engineers, and cloud cost owners use this skill to analyze exported BigQuery query, storage, and billing data and identify practical cost-reduction opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported BigQuery query, user, storage, and billing metadata can contain sensitive project, account, customer, or workload information.

Mitigation: Review exports locally before sharing and redact full SQL literals, user or service-account emails, project and dataset names, billing account identifiers, customer data, tokens, keys, and other sensitive values.

Risk: Cost recommendations depend on the completeness and accuracy of the user-provided BigQuery data.

Mitigation: Provide recent query, storage, and billing exports when possible, and treat recommendations as reviewable guidance before changing production query patterns or reservations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/skills/bigquery-optimizer)
- [Publisher Profile](https://clawhub.ai/user/anmolnagpal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with cost analysis sections, query examples, and plain-English recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; uses user-provided exported BigQuery, storage, or billing data and does not access GCP accounts directly.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
