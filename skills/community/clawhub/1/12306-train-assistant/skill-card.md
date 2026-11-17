## Description:

Helps agents use a Python CLI to query China Railway 12306 train availability, routes and transfers, manage login status, inspect orders and passengers, submit or cancel standby requests, book tickets, and retrieve payment links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myxtype](https://clawhub.ai/user/myxtype)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent assist with China Railway 12306 ticket search, route planning, standby ticket management, booking preparation, and payment-link retrieval through the bundled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a user's 12306 account, passenger records, ticket orders, payment workflow, and cached session cookies.

Mitigation: Install only after review, avoid exposing passwords in visible command lines, and protect or clear the cookie cache after use.

Risk: Booking, cancellation, standby ticket, and payment-related commands can affect real travel purchases.

Mitigation: Require the agent to present proposed actions for manual confirmation before running any booking, cancellation, or payment command.

Risk: The CLI supports overriding the 12306 base URL, which could send account or order data to an untrusted destination.

Mitigation: Do not use a custom base URL unless the destination is fully controlled and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myxtype/skills/12306-train-assistant)
- [China Railway 12306 service](https://kyfw.12306.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to text output for readability; JSON output is used when explicitly requested.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
