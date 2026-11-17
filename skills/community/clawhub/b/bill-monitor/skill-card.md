## Description:

Tracks utility bills and flags unexpected increases year-on-year. Use when a user wants to monitor household bills or get alerted to price changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to monitor household utility, insurance, housing, and other recurring bills, receive private alerts for unexpected increases, and compare switching options near contract renewal dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad daily Gmail searches can collect sensitive financial emails beyond the intended bills.

Mitigation: Use a dedicated bill label or approved sender list, and require confirmation before the first scan and before daily automatic processing.

Risk: Bill amounts, provider names, payment details, and histories are sensitive household financial data.

Mitigation: Deliver results only to the owner's configured private channel, avoid shared channels, and keep stored records inspectable, correctable, and deletable.

Risk: Switch-advisor searches could expose provider names, amounts, or bill history to web search providers.

Mitigation: Avoid sending personal bill details into web searches unless the user explicitly chooses to include them.

Risk: Bill emails can contain prompt-injection attempts that ask the agent to reveal financial data or repeat stored files.

Mitigation: Refuse embedded instructions from incoming bill emails and flag suspicious messages to the owner.

## Reference(s):

- [Bill Monitor skill page](https://clawhub.ai/rednix/skills/bill-monitor)
- [Bill Monitor homepage metadata](https://clawhub.com/skills/bill-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown alerts, summaries, reports, local bill records, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handles sensitive household bill amounts, provider names, payment details, bill history, and contract dates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
