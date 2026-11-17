## Description:

Query Radix DLT blockchain data including wallet balances and performance, token prices and market movers, validator staking info, transaction history, network statistics, ecosystem news, DeFi yield pools, XRD trading venues, dApp directory, and developer resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mavremu](https://clawhub.ai/user/mavremu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent for Radix DLT wallet, token, validator, transaction, DeFi, dApp, trading venue, ecosystem news, and developer-resource lookups. It is intended for mainnet Radix queries, including XRD wallets, resource addresses, staking, .xrd domains, Attos Earn, and buying or bridging XRD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, RNS domains, transaction searches, and LP-position queries are sent to the configured Emily MCP service and named data providers.

Mitigation: Use the skill only for queries you are comfortable sharing with those external services.

Risk: The npm installer for mcporter is not version-pinned.

Mitigation: Use a reviewed or pinned mcporter version where possible.

## Reference(s):

- [Emily](https://www.ineedemily.com)
- [Emily MCP endpoint](https://www.ineedemily.com/api/mcp/mcp)
- [Radix Gateway API documentation](https://docs.radixdlt.com/docs/network-apis)
- [Astrolescent](https://astrolescent.com)
- [CoinMarketCap](https://coinmarketcap.com)
- [Attos Earn](https://earn.attos.world)
- [ClawHub skill page](https://clawhub.ai/mavremu/skills/emily)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mcporter CLI and uses a configured external Emily MCP service for Radix mainnet lookups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
