## Description:

Track lab equipment calibration dates and send maintenance reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Lab staff, operations teams, and developers use this skill to add equipment records, list tracked assets, and check upcoming or overdue calibration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent equipment records are written under ~/.openclaw/equipment_log.json, which may surprise users expecting workspace-scoped output.

Mitigation: Review before installing, document the data path, and run only where home-directory persistence is acceptable or after changing the storage path.

Risk: File creation and writes have weak safety controls according to the security summary.

Mitigation: Harden file creation and writes, and prefer a user-chosen workspace path before routine deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/equipment-maintenance-log-2)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Command-line text output with maintenance schedules, overdue alerts, and upcoming reminders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores equipment records as local JSON for later checks.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
