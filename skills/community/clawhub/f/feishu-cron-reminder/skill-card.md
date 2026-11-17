## Description:

Creates and manages scheduled reminders through a Feishu bot, supporting one-time and recurring reminders sent to Feishu users or groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzqsama066](https://clawhub.ai/user/zzqsama066)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with OpenClaw and a configured Feishu bot to create reminder jobs for meetings, recurring tasks, workday notices, and group notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder jobs can send accidental outbound messages to Feishu users or groups if the recipient, schedule, timezone, or message is wrong.

Mitigation: Confirm the recipient, schedule, timezone, and exact reminder text before creating or announcing a cron job.

Risk: Shell-command templates can create command-injection exposure when reminder text, names, descriptions, or destination IDs contain untrusted content.

Mitigation: Use structured argument passing or robust escaping for all user-controlled fields instead of building raw shell strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzqsama066/skills/feishu-cron-reminder)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw cron command templates for Feishu user or group reminder destinations.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
