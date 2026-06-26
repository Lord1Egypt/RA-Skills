## Description: <br>
Deploy ERC20 tokens on Base using Clanker SDK. Create tokens with built-in Uniswap V4 liquidity pools. Supports Base mainnet and Sepolia testnet. Requires PRIVATE_KEY in config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spirosrap](https://clawhub.ai/user/spirosrap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy ERC20 tokens on Base mainnet or Base Sepolia and to inspect token, deployer, and transaction status information through Clanker-related commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles raw wallet private keys and can read them from local configuration. <br>
Mitigation: Use a fresh low-balance wallet, avoid storing a funded mainnet private key in the config file, and keep keys outside version control. <br>
Risk: Mainnet deployment can submit irreversible Base transactions that spend ETH. <br>
Mitigation: Test on Sepolia first and manually review token parameters, gas, ETH value, and network selection before any mainnet deployment. <br>
Risk: Incorrect or stale Clanker contract addresses can cause failed or unintended interactions. <br>
Mitigation: Verify Clanker contract addresses from official sources before deploying or interacting with contracts. <br>


## Reference(s): <br>
- [Clanker SDK Reference](references/clanker-sdk.md) <br>
- [Clanker Official Website](https://clanker.world) <br>
- [Clanker Documentation](https://docs.clanker.world) <br>
- [ClawHub Skill Page](https://clawhub.ai/spirosrap/clanker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples, wallet configuration guidance, transaction hashes, token metadata, and deployment status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
