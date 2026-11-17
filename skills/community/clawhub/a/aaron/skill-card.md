## Description:

Persistent receptionist/orchestrator agent for CFO dental appointments that manages scheduling, reminders, pre-appointment prep, post-appointment follow-up, and insurance coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or personal operations agents use Aaron to manage dental appointment scheduling, reminders, treatment follow-up, and insurance coordination for a CFO workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive dental, insurance, identity, appointment, and commute details may be stored in plaintext local files and logs.

Mitigation: Use the skill only when local persistence is acceptable, verify restrictive file permissions, and define a deletion plan before storing personal or insurance data.

Risk: Insurance member or group identifiers could be entered into persistent records.

Mitigation: Avoid recording insurance identifiers unless the storage location is protected and retention requirements are clear.

Risk: External cron reminders may expose appointment or health-related details through the reminder channel.

Mitigation: Review any cron setup and notification destination before enabling scheduled reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ironiclawdoctor-design/skills/aaron)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status reports and reminders with JSON records and JSONL logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists dental appointment, treatment, dentist, and insurance details in local files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
