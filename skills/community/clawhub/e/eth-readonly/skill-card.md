## Description: <br>
Read-only Ethereum blockchain queries for blocks, transactions, balances, contracts, logs, RPC endpoints, and Etherscan APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apexfork](https://clawhub.ai/user/apexfork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to inspect Ethereum blockchain state, transactions, balances, contracts, event logs, gas data, and Etherscan responses without wallet access or transaction signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address, transaction, contract, and timing queries may be visible to the configured RPC or Etherscan provider. <br>
Mitigation: Use trusted providers, avoid pasting sensitive API keys into chat, and prefer private or organization-approved endpoints for sensitive investigations. <br>
Risk: Broad event-log or history queries can exhaust provider rate limits or quotas. <br>
Mitigation: Keep log filters narrow by contract and block range, and use paid or local infrastructure for high-volume lookups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apexfork/eth-readonly) <br>
- [Publisher profile](https://clawhub.ai/user/apexfork) <br>
- [Skill homepage](https://github.com/Fork-Development-Corp/openclaw-web3-skills/tree/master/eth-readonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cast or curl for queries; Etherscan API usage requires a user-provided API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
