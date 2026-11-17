## Description:

Autonomous full-time SaaS operations manager for Creem.io stores. Monitors heartbeat, handles failed payments, churn, revenue digests, and answers natural language queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vayospot](https://clawhub.ai/user/vayospot)

### License/Terms of Use:

MIT-0

## Use Case:

SaaS founders and developers who use Creem as their payment processor use this skill to monitor store health, summarize revenue and subscriber status, detect failed payments or churn, and prepare operational follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create winback discounts and generate billing links as part of payment-account workflows.

Mitigation: Require explicit confirmation before billing links, discounts, customer outreach, or any live store mutation.

Risk: The skill may post revenue, subscriber, and milestone updates to Discord.

Mitigation: Enable Discord posting only after destinations, group allowlists, and approval rules are configured.

Risk: The skill requires access to a Creem API key for store monitoring and operations.

Mitigation: Use a narrowly scoped read-only Creem key for monitoring whenever possible.

## Reference(s):

- [Creem Agent ClawHub listing](https://clawhub.ai/vayospot/skills/creem-agent)
- [Creem skill reference](https://creem.io/SKILL.md)
- [Creem heartbeat reference](https://creem.io/HEARTBEAT.md)
- [Creem documentation for agents](https://docs.creem.io/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and occasional JSON heartbeat output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output HEARTBEAT_OK when no store changes need attention.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
