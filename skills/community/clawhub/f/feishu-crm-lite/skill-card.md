## Description:

Helps agents manage lightweight CRM workflows for Feishu-oriented customer records, follow-ups, reminders, sales funnel tracking, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and small teams can use this skill to track customers, log follow-ups, set reminders, review sales funnel status, and generate simple CRM reports where local plaintext storage is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer and follow-up data may be stored as local plaintext JSON under data/feishu-crm, while the documentation describes Feishu Bitable storage.

Mitigation: Run from a private workspace, avoid regulated or highly sensitive customer data, and confirm the storage model before operational use.

Risk: The documentation describes Feishu Bitable synchronization and integration that the security evidence says is not implemented.

Mitigation: Treat Feishu sync as unavailable until verified, and do not rely on it as the source of record.

Risk: Delete and bulk import/export workflows can affect customer records.

Mitigation: Require explicit confirmation and backups before deleting records or performing bulk import/export.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/skills/feishu-crm-lite)
- [ClawHub publisher profile](https://clawhub.ai/user/daimingvip-a11y)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with example prompts and CLI output, including JSON for CRM records and reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores customer, follow-up, and reminder data as local JSON files under data/feishu-crm.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
