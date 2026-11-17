## Description:

Automation Dedup Guard helps WorkBuddy users detect and clean duplicate automation tasks while keeping the newest task in each same-name group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vic276344-dotcom](https://clawhub.ai/user/vic276344-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy operators use this skill to preview or remove duplicate automation database records, especially when repeated same-name tasks cause task list bloat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup script can permanently delete WorkBuddy automation records and related run history.

Mitigation: Run with --dry-run first, back up the database, and execute cleanup only after confirming the previewed records are true duplicates.

Risk: Duplicate detection uses same-name grouping, which can remove distinct automations that share a name.

Mitigation: Review each same-name group before deletion and use a custom database path only after verifying it points to the intended WorkBuddy database.

Risk: Recurring setup can run cleanup unattended.

Mitigation: Avoid scheduled execution unless the operator accepts automatic permanent cleanup and has monitoring or backups in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vic276344-dotcom/skills/automation-dedup-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of a Python script that reports duplicate WorkBuddy automations and can delete database records when not run in dry-run mode.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
