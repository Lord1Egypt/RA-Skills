## Description:

管理并计算生日提醒，支持阳历与农历生日、每条记录覆盖全局默认值、提前多次提醒和本地通知分发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[905583906](https://clawhub.ai/user/905583906)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create and maintain local birthday reminder configurations, validate due reminders, and send reminders through configured notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birthday records and reminder messages can contain personal information.

Mitigation: Store birthday JSON files locally with appropriate access controls and minimize personal details in messages sent to notification services.

Risk: Webhook URLs, bot tokens, chat IDs, and notification endpoints can expose credentials or delivery targets.

Mitigation: Protect notification credentials, avoid committing real secrets, and use dry-run checks before enabling live delivery.

Risk: File output can write reminder text to shared or sensitive paths.

Mitigation: Use explicit, private file paths for file notifications and avoid shared locations for logs containing personal reminders.

## Reference(s):

- [Birthday Config Schema](references/config-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/905583906/skills/birthday-reminder-cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSON configuration guidance and command-line reminder checks; notification text may be sent only through user-configured channels.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
