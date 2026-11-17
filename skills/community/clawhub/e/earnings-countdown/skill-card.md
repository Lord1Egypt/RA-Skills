## Description:

Sets up a daily earnings countdown reminder for a stock by resolving a company to a ticker, fetching the next earnings date, and scheduling recurring briefings with price and fundamentals checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to schedule recurring countdown briefings before a public company's upcoming earnings date. The skill is intended for earnings reminders that combine reminder scheduling, ticker resolution, earnings-date lookup, stock price checks, and fundamentals checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent reminders that can run stock-related tools daily in a chat.

Mitigation: Install only if the publisher is trusted, and confirm the reminder destination, schedule, timezone, and cancellation behavior before use.

Risk: Ticker and company values are placed into shell-style command templates.

Mitigation: Validate ticker symbols and company names before scheduling, and prefer structured subprocess arguments or a safer reminder API where available.

Risk: Earnings dates may be missing, unsupported, or unavailable from the finance data source.

Mitigation: Confirm the resolved ticker and earnings date before creating a reminder; stop scheduling when the lookup returns an error.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youpele52/skills/earnings-countdown)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent daily reminder configuration when executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
