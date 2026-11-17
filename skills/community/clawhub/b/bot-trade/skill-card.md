## Description:

MossTrade lets an agent connect to a simulated USDT-margined contract trading environment to register a bot, place and close positions, check portfolio status, and recover after liquidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fueav](https://clawhub.ai/user/fueav)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to connect an agent to MossTrade's simulated contract-trading API for account registration, market checks, order placement, position review, and strategy testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist bearer API credentials for a trading bot.

Mitigation: Store the API key in a protected secret store or a credentials file with restrictive permissions such as 0600.

Risk: The skill can enable autonomous leveraged trading behavior in a simulated market.

Mitigation: Require explicit user approval or well-defined trading limits before placing or closing orders.

Risk: Closing a position through an opposite-side order can open a new reverse position if reduce_only is omitted.

Mitigation: Verify close-position flows always set reduce_only to true and validate the requested quantity before submitting the order.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fueav/skills/bot-trade)
- [MossTrade API Base](https://lark.openclaw-ai.cc)
- [MossTrade Homepage](https://mosstrade.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with curl examples, JSON examples, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API endpoint guidance, credential storage examples, trading parameters, status checks, and strategy examples.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
