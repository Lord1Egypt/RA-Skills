## Description:

Set up daily countdown reminders for upcoming price-moving corporate events by resolving a company to its ticker, finding the event date, and scheduling daily price and fundamentals briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to create daily countdown reminders for upcoming corporate events such as earnings, AGMs, product launches, investor days, dividends, FDA decisions, splits, or M&A votes. The reminders deliver price and fundamentals briefings until the confirmed event date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent daily reminders that can run other skills.

Mitigation: Review the reminder schedule, delivery target, timezone, and event date before creating the reminder, and ensure the reminder cancels on the event day.

Risk: Reminder command text is assembled from ticker, company, and event values.

Mitigation: Validate ticker and event fields, constrain user-provided values, and review generated reminder commands before execution.

Risk: The skill depends on yfinance without a pinned version in the artifact.

Mitigation: Pin dependencies and review dependency behavior before production deployment.

## Reference(s):

- [Event Countdown Pro on ClawHub](https://clawhub.ai/youpele52/skills/event-countdown-pro)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent daily scheduled reminders after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
