## Description: <br>
Query Radix DLT blockchain data including wallet balances and performance, token prices and market movers, validator staking info, transaction history, network statistics, ecosystem news, DeFi yield pools, XRD trading venues, dApp directory, and developer resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MAvRemu](https://clawhub.ai/user/MAvRemu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Radix users, DeFi participants, and developers use this skill to query Radix mainnet wallet, token, validator, transaction, ecosystem, and developer-resource data through Emily. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing the mcporter package from npm and connecting to a remote Emily service. <br>
Mitigation: Install only if you are comfortable with that package and remote service, and review the configured MCP endpoint before use. <br>
Risk: Wallet addresses, .xrd domains, token IDs, and market queries are sent to Emily and its listed data providers. <br>
Mitigation: Avoid querying addresses or domains you consider sensitive unless you trust those services and their data handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MAvRemu/emily-radix-assistant) <br>
- [Emily](https://www.ineedemily.com) <br>
- [Radix Gateway API](https://docs.radixdlt.com/docs/network-apis) <br>
- [Astrolescent](https://astrolescent.com) <br>
- [CoinMarketCap](https://coinmarketcap.com) <br>
- [Attos Earn](https://earn.attos.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the mcporter CLI to connect to the Emily MCP service; service responses may include blockchain, market, ecosystem, and developer-resource data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
