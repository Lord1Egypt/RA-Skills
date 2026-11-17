## Description:

Tracks lab equipment calibration dates, maintenance reminders, date validation, and update/delete operations for pipettes, balances, centrifuges, and other instruments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Lab staff, compliance teams, and developers use this skill to maintain local calibration records, check overdue or upcoming equipment maintenance, and generate audit-ready compliance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local equipment records can be permanently deleted when delete operations are requested.

Mitigation: Keep backups for audit-sensitive logs and confirm deletion requests before running the packaged script.

Risk: Bad or extreme interval values may corrupt maintenance schedules because range validation is not documented as present.

Mitigation: Use trusted interval values and review the local JSON log after changes until range validation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/equipment-maintenance-log-1)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON compliance reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the packaged script is run, it reads and writes a local JSON equipment log.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
