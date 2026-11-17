## Description:

Manages a local CSV-based CRM with pipeline tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Employees, founders, sales operators, and other external users use this skill to maintain a lightweight local CRM, track contacts through pipeline stages, and identify overdue follow-ups from a workspace CSV file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM contacts, notes, phone numbers, emails, and deal values are stored in a plaintext workspace CSV file.

Mitigation: Install only when plaintext local storage is acceptable for the CRM data, review crm.csv before bulk changes, and keep backups for important customer data.

Risk: Bulk CRM changes can affect many local records at once.

Mitigation: Back up the CSV before bulk operations and review the proposed changes before applying them.

## Reference(s):

- [CRM Manager ClawHub listing](https://clawhub.ai/1kalin/skills/crm-manager)
- [Context packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown summaries and tables with local CSV file reads, writes, and backups.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates crm.csv in the workspace and may create crm-backup-YYYY-MM-DD.csv before bulk operations.]

## Skill Version(s):

1.0.0 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
