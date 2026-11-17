## Description:

A customer-management helper for cloud account managers that organizes customer information, records follow-up history, and generates customer profile documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyuanyuan1](https://clawhub.ai/user/guyuanyuan1)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud computing account managers use this skill to maintain customer records, capture visit and communication history, classify accounts by business attributes, and prepare customer profile documents and summary reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer records can contain sensitive business and contact information.

Mitigation: Scope the agent to the intended customer directory or Feishu workspace, avoid broad business data access, and review generated records before sharing.

Risk: Generated customer profiles or follow-up summaries may contain incorrect or outdated account details.

Mitigation: Validate generated records against source notes, meeting records, or approved customer data before relying on them for outreach or reporting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guyuanyuan1/skills/customer-management)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown customer profiles, follow-up notes, customer summaries, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive customer information and should be reviewed before sharing or syncing to external documents.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
