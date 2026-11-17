## Description:

Query Radix DLT blockchain data including wallet balances and performance, token prices and market movers, validator staking info, transaction history, network statistics, ecosystem news, DeFi yield pools, XRD trading venues, dApp directory, and developer resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mavremu](https://clawhub.ai/user/mavremu)

### License/Terms of Use:


## Use Case:

External users, Radix community members, and developers use this skill to query Radix mainnet wallet, token, staking, DeFi, ecosystem, and developer-resource data through Emily's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, token queries, and timing or IP metadata may be sent to the Emily MCP service and its listed data providers.

Mitigation: Use the skill only with data the user is comfortable exposing to those remote services, and avoid sensitive network contexts where this metadata should remain internal.

Risk: The skill depends on the mcporter npm package for setup and execution.

Mitigation: Pin, mirror, or separately review the mcporter package before deployment in sensitive environments.

Risk: Market, DeFi, and ecosystem responses may reflect provider freshness, caching, or rate limits.

Mitigation: Check source freshness and avoid treating generated responses as the sole basis for financial or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mavremu/skills/emily-radix-assistant)
- [Publisher profile](https://clawhub.ai/user/mavremu)
- [Emily](https://www.ineedemily.com)
- [Emily MCP service endpoint](https://www.ineedemily.com/api/mcp/mcp)
- [Radix Gateway API](https://docs.radixdlt.com/docs/network-apis)
- [Astrolescent](https://astrolescent.com)
- [CoinMarketCap](https://coinmarketcap.com)
- [Attos Earn](https://earn.attos.world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live or cached blockchain, market, DeFi, ecosystem, and wallet data from Emily MCP service data providers.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
