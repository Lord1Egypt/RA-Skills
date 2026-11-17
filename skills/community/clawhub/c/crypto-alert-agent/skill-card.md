## Description:

A proactive agent that monitors cryptocurrency prices, tracks your portfolio, and sends alerts via Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitja1988](https://clawhub.ai/user/vitja1988)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor cryptocurrency prices, track portfolio holdings, and receive Telegram alerts when configured price conditions are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram notifications may send crypto alert activity and possible portfolio value information outside the local environment.

Mitigation: Install and configure the skill only if Telegram delivery is acceptable for this information.

Risk: The referenced run.sh implementation was not included in the inspected package.

Mitigation: Review the actual script before running it manually or placing it on a cron schedule.

## Reference(s):

- [Crypto Alert Agent on ClawHub](https://clawhub.ai/vitja1988/skills/crypto-alert-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and cron command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include cryptocurrency price checks, portfolio summaries, alert-management commands, and Telegram notification guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
