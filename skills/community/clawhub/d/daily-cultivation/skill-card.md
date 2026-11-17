## Description:

人格修行系统 Daily Cultivation helps an agent generate scheduled morning wisdom prompts and evening reflection templates for virtue practice, quote rotation, and optional local journaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opc8838-hub](https://clawhub.ai/user/opc8838-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure recurring daily self-cultivation prompts, rotate a weekly virtue focus, manage a small quote library, and produce evening reflection records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring reminders may continue sending messages after setup.

Mitigation: Confirm the timezone, morning and evening schedules, destination channels, and how to disable cron jobs before enabling the skill.

Risk: Evening reflections may contain sensitive journal content that is sent to a channel or saved locally.

Mitigation: Use private destinations, avoid group chats for personal reflections, and review the vault path and auto-save setting before use.

Risk: Archived notes can persist after the skill is disabled.

Mitigation: Decide where archived notes are stored and document how to delete them if they are no longer wanted.

## Reference(s):

- [Configuration Guide](artifact/references/config-guide.md)
- [Franklin Virtues Reference](artifact/references/franklin-virtues.md)
- [ClawHub Release Page](https://clawhub.ai/opc8838-hub/skills/daily-cultivation)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reminders and reflection templates with YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May schedule recurring messages and optionally save personal reflection notes to a configured local vault.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
