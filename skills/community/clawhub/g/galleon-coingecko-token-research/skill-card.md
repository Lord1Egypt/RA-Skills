## Description:

Resolve CoinGecko token identity, distinguish native and bridged assets, and produce a timestamped price, market cap and liquidity evidence card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and token researchers use this skill to resolve a token by chain and contract, then prepare a dated evidence card for price, market data and available liquidity. It also helps compare provider observations with a DEX quote while keeping identity, freshness and execution limits explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because a local path-like reference in SKILL.md could not be resolved.

Mitigation: Review the unresolved local reference and the skill before installation; the benign verdict has medium confidence and is not a guarantee of safety.

Risk: Live workflows make requests to CoinGecko, an external service.

Mitigation: Use the skill only if CoinGecko requests are acceptable for the task; the scan does not confirm whether any request was made.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/galleonlabs/skills/galleon-coingecko-token-research)
- [CoinGecko contract address lookup](https://docs.coingecko.com/demo/reference/coins-contract-address)
- [CoinGecko token price endpoint](https://docs.coingecko.com/demo/reference/simple-token-price)
- [CoinGecko onchain top pools](https://docs.coingecko.com/reference/top-pools-contract-address)
- [CoinGecko API changelog](https://docs.coingecko.com/changelog)
- [Request and identity guidance](references/requests.md)
- [Dated official sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [A concise conclusion with a structured token evidence card, typically in JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes contract identity, timestamped provider observations, freshness and identity status, and whether an execution quote was obtained. Missing or unsupported values remain explicit.]

## Skill Version(s):

0.8.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
