## Description: <br>
Deploys and manages an AI agent's onchain identity, reputation, task prices, metadata, and task-agent contracts on Avalanche using ERC-8004. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iJaack](https://clawhub.ai/user/iJaack) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to register an AI agent identity on Avalanche, deploy supporting ValidationRegistry and TaskAgent contracts, and update agent metadata, URI, and task pricing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a raw wallet private key and can spend real AVAX on Avalanche mainnet. <br>
Mitigation: Use a dedicated low-balance wallet and keep PRIVATE_KEY out of commits, logs, screenshots, and shell history. <br>
Risk: Deploy, metadata, URI, and price commands can make persistent public blockchain changes without an in-tool confirmation step. <br>
Mitigation: Verify the RPC network, chain ID, contract addresses, task prices, and agent metadata before running write commands. <br>
Risk: Deployment and update commands depend on external Avalanche RPC and explorer infrastructure. <br>
Mitigation: Confirm network availability and independently inspect resulting contract addresses and transaction hashes after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iJaack/erc8004-identity) <br>
- [ERC-8004 Spec](https://github.com/ava-labs/ERC-8004) <br>
- [Avalanche Docs](https://docs.avax.network) <br>
- [Publisher profile](https://clawhub.ai/user/iJaack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Blockchain transactions] <br>
**Output Format:** [Markdown guidance with CLI commands, JavaScript configuration, JSON deployment records, and onchain transaction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write config/agent.config.js and deployment.json, deploy contracts, and submit persistent Avalanche mainnet transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
