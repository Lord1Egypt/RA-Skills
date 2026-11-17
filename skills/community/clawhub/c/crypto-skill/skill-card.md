## Description:

Provides current cryptocurrency prices, gas estimates, trending tokens, wallet balances, name resolution, and token details for OpenClaw agents without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to retrieve current crypto market and on-chain information, including prices, gas, token data, and public wallet balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto symbols, public wallet addresses, names, and lookup timing can be disclosed to external data providers.

Mitigation: Only submit public identifiers you are comfortable sharing with Spraay, public resolvers, DexScreener-backed services, and public RPC providers.

Risk: Crypto market data and trending lists can be mistaken for investment recommendations.

Mitigation: Present results as informational data, verify relevant details independently, and never share private keys or seed phrases.

## Reference(s):

- [Spraay free-tier catalog](https://gateway.spraay.app/free)
- [Spraay documentation](https://docs.spraay.app)
- [DexScreener API documentation](https://docs.dexscreener.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with prices, balances, gas estimates, and lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups; data may be cached and lookup requests are rate-limited.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
