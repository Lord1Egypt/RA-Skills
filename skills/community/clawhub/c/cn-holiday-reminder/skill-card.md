## Description:

Provides Chinese statutory holiday and adjusted-workday lookups, proactive holiday reminders, and relationship anniversary, birthday, custom date, and romantic holiday reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironmanc2014](https://clawhub.ai/user/ironmanc2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer China holiday, workday, next-holiday, annual-calendar, anniversary, birthday, and romantic-reminder questions, and to configure scheduled reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores partner names, birthdays, anniversaries, and custom relationship dates in a plaintext local file.

Mitigation: Use it on a private machine or account and restrict permissions for ~/agent-memory/love.json.

Risk: Reminder content may be sent through Feishu when automated reminder delivery is enabled.

Mitigation: Use a private Feishu destination or avoid Feishu delivery for sensitive reminders.

Risk: Some holiday dates are predicted until official schedules are updated.

Mitigation: Treat predicted dates as provisional and update the bundled holiday data after official announcements are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ironmanc2014/skills/cn-holiday-reminder)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Holiday data is embedded locally; relationship reminder data may be stored in ~/agent-memory/love.json.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
