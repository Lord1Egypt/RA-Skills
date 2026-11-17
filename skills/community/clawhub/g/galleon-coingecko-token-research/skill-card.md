## Description:

Resolves CoinGecko token identity by chain and contract, then reports timestamped market evidence and relevant pool liquidity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and token researchers use this skill to verify a token's chain and contract, assess dated CoinGecko price and market observations, and distinguish those observations from executable DEX quotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token identifiers may be sent to CoinGecko or an existing approved quote provider.

Mitigation: Use the skill only when sharing the researched identifiers with those providers is acceptable.

Risk: An API key could be exposed through insecure request configuration.

Mitigation: Use protected credential configuration; do not put keys in URLs, shell history, or output artifacts.

Risk: Aggregate prices or market metrics could be mistaken for executable quotes or trading advice.

Mitigation: Report source and freshness, check pool depth and trade size when sellability matters, and do not treat the evidence card as trading or wallet/PnL advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/galleonlabs/skills/galleon-coingecko-token-research)
- [Request and identity guidance](references/requests.md)
- [Official sources](references/sources.md)
- [CoinGecko contract identity API](https://docs.coingecko.com/demo/reference/coins-contract-address)
- [CoinGecko token price API](https://docs.coingecko.com/demo/reference/simple-token-price)
- [CoinGecko top pools API](https://docs.coingecko.com/reference/top-pools-contract-address)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON evidence card with a brief written conclusion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes chain, contract, currency, source, observation and retrieval times, and identity and freshness status; unavailable metrics remain unknown.]

## Skill Version(s):

0.6.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
