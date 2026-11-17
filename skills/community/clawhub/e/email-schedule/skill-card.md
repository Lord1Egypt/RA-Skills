## Description:

从 macOS 邮件应用检索指定范围的邮件，提取邮件中的会议或活动时间，并通过提醒事项创建提前 2 小时的本地提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yfwill](https://clawhub.ai/user/yfwill)

### License/Terms of Use:

MIT-0

## Use Case:

External macOS users use this skill to review recent, unread, or date-scoped Apple Mail messages and create Reminders entries for future events detected in the subject or summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Apple Mail sender, subject, and summary data for the selected range.

Mitigation: Use the narrowest useful range, such as today or unread, and avoid all unless the broader review is necessary.

Risk: The skill creates reminders in the user's default Reminders list through remindctl.

Mitigation: Review the reminder results after execution and confirm the remindctl Homebrew tap before installing or using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yfwill/skills/email-schedule)
- [ClawHub publisher profile](https://clawhub.ai/user/yfwill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown or plain text summary with optional shell commands and JSON mail records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports checked email count, created reminder count, and reminder titles with event times when reminders are created.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
