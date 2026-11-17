## Description:

Creates and tracks batches of audience identity-linking tasks through the Mingri DMP Open API using spreadsheet or JSON inputs, then summarizes audience names, IDs, and outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

DMP operators and developers use this skill to create and monitor batches of cross-device audience-linking tasks, then review a consolidated account of completed and failed audiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DMP API credentials are sensitive and may remain in the workspace.

Mitigation: Install only in a trusted workspace and rotate or remove credentials when finished.

Risk: Scheduled monitoring automatically advances batches and can create additional audiences.

Mitigation: Confirm the batch plan, failure policy, and scheduled progression meet organizational approval requirements before starting.

Risk: The authentication helper may discover other local skills.

Mitigation: Review the helper dependency and avoid untrusted sibling skills.

Risk: The workflow checks for an unrelated task logger that may record project and audience details.

Mitigation: Confirm logging is permitted by your data policy before enabling it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mingri26/skills/dmp-bulk-integration-segmentation)
- [API reference](references/api_reference.md)
- [Monitoring rules](references/监控规则与禁用项.md)
- [Credential setup guide](references/凭证获取指南.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown status summaries and a local JSON project record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports audience names, IDs, status, counts, and failures by batch.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
