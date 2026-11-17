## Description:

Track lab equipment calibration dates and send maintenance reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanruoyu](https://clawhub.ai/user/shanruoyu)

### License/Terms of Use:

MIT-0

## Use Case:

Lab operations staff, facility teams, and developers use this skill to add equipment records, list calibration schedules, and check overdue or upcoming maintenance for lab equipment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Equipment records are stored in ~/.openclaw/equipment_log.json, which may be outside the expected workspace location.

Mitigation: Review or change the storage path and file permissions before entering sensitive lab or facility data.

Risk: Maintenance reminders are manual command output, not automatic notifications.

Mitigation: Run reminder checks on an appropriate cadence and do not rely on the skill alone for regulated maintenance workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shanruoyu/skills/equipment-maintenance-log)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs maintenance schedules, overdue alerts, and upcoming reminder summaries; records are stored in ~/.openclaw/equipment_log.json.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
