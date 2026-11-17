## Description:

Get a daily pre-session crypto market brief with BTC bias, Korean exchange flows, whale activity, Fear & Greed index, and macro context valid for 24 hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokoju007](https://clawhub.ai/user/kokoju007)

### License/Terms of Use:

MIT-0

## Use Case:

Portfolio agents, trading bots, and orchestrators use this skill to request a daily crypto market snapshot before a trading session. The brief summarizes market bias and context for agent workflows that need a same-day baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market signals may be incomplete, stale, or unsupported by trusted market data in the calling agent.

Mitigation: Treat outputs as informational context unless the agent has trusted market-data sources and independent validation.

Risk: The skill includes a paid Orion ACP upgrade path.

Mitigation: Require explicit user confirmation before using ACP or any external service that costs money.

## Reference(s):

- [Daily Desk - Orion on ClawHub](https://clawhub.ai/kokoju007/skills/daily-desk-orion)
- [Orion ACP listing](https://app.virtuals.io/virtuals/1809)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown market brief with optional structured JSON for the paid Orion ACP workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily snapshot is described as valid for 24 hours and may include a paid-upgrade prompt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
