## Description:

Manages a local CSV-based CRM with pipeline tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Sales operators and small business teams use this skill to maintain a local CSV CRM, track deal stages, and review follow-up reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer, contact, and deal information may be stored in a plaintext crm.csv file in the workspace.

Mitigation: Keep the workspace private, avoid shared or cloud-synced folders for sensitive CRM data, and install only when plaintext local storage is acceptable.

Risk: The skill can change local CRM records, including contact details, deal stages, notes, and follow-up dates.

Mitigation: Review proposed changes before broad updates and keep dated backups before bulk operations.

Risk: Pipeline health checks and follow-up reminders depend on accurate CSV dates and complete next-action fields.

Mitigation: Review missing or overdue next_action_date values and correct stale records before relying on summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1kalin/skills/afrexai-crm-updater)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries with local CSV file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update crm.csv and crm-backup-YYYY-MM-DD.csv in the workspace.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
