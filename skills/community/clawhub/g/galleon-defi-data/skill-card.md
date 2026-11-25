## Description:

Connect official CoinGecko, DefiLlama and AIXBT data tools and evaluate prices, protocol metrics, crypto narratives and yield evidence. Use when configuring data access, researching DeFi markets, or reconciling source identity, freshness and coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and DeFi analysts use this skill to connect official market data tools, research markets and protocols, and assess whether price, metric, and yield claims are supported by source identity, freshness, and methodology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence; one of 15 components was not fully inspected, and static analysis of the included script was degraded.

Mitigation: Review the included diagnostic script and consider whether the external data providers are acceptable before use; treat the verdict as incomplete evidence, not a safety guarantee.

## Reference(s):

- [Galleon DeFi Data on ClawHub](https://clawhub.ai/galleonlabs/skills/galleon-defi-data)
- [Provider setup and access tiers](references/providers.md)
- [Data interpretation and provenance](references/methodology.md)
- [Public price diagnostic](references/diagnostic.md)
- [Product diligence](references/diligence.md)
- [Evidence across DeFi primitives](references/primitive-evidence.md)
- [AIXBT crypto research](references/aixbt.md)
- [Onchain agent evidence sources](references/onchain-agents.md)
- [Worked evidence examples](references/worked-examples.md)
- [CoinGecko AI integrations](https://docs.coingecko.com/docs/ai-agents-llm-apps)
- [DefiLlama API documentation](https://api-docs.defillama.com/)
- [AIXBT API v3 overview](https://docs.aixbt.tech/developers/v3)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions, Shell commands, JSON]

**Output Format:** [Markdown responses; the optional public price diagnostic emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source identity, observation and retrieval times, and material limitations; it does not authorize paid access or transactions.]

## Skill Version(s):

0.8.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
