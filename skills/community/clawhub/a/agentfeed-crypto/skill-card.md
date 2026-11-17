## Description:

Guides agents in accessing paid AgentFeed market data, Solana pre-trade checks, sanctions screening, research tools, and fixed-purpose language services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seekdaseek](https://clawhub.ai/user/seekdaseek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide agents in retrieving live crypto market data, checking tokens or wallets, and invoking paid research or language tools. It explains how to review and approve per-call payments or use prepaid access without treating market results as trading advice.

### Deployment Geography for Use:

Global, subject to availability of individual language routes by location

## Known Risks and Mitigations:

Risk: Paid API requests or prepaid purchases may spend funds unexpectedly.

Mitigation: Obtain approval for each paid call or key purchase, check the current price, set a per-call maximum, and verify the payTo address from a fresh payment challenge before signing.

Risk: A leaked prepaid API key can be used to spend its balance.

Mitigation: Keep afk_ bearer keys out of chats and logs.

Risk: Live market results may be mistaken for trading advice.

Mitigation: Present results as data with their limits and leave trading decisions to the user.

## Reference(s):

- [AgentFeed API documentation](https://x402.ochinimus.app/openapi.json)
- [AgentFeed homepage](https://x402.ochinimus.app)
- [AgentFeed repository (publisher-listed link)](https://github.com/seekdaseek/agentfeed)
- [ClawHub skill listing](https://clawhub.ai/seekdaseek/skills/agentfeed-crypto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTTPS request examples; retrieved API responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payments require user approval; present market data with its limitations, not as trading advice.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
