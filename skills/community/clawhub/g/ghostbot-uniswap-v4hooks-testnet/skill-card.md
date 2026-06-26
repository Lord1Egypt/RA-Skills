## Description: <br>
GhostBot ACLM helps agents manage Uniswap v4 concentrated liquidity on Ethereum Sepolia by checking status, adding liquidity, viewing positions, reading oracle signals, and posting authorized oracle updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AqilJaafree](https://clawhub.ai/user/AqilJaafree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and DeFi operators use this skill to inspect and manage Sepolia testnet Uniswap v4 liquidity positions, pool stats, dynamic fee signals, and authorized oracle actions from chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes transaction scripts with an embedded fallback private key. <br>
Mitigation: Remove the hardcoded fallback key and require DEPLOYER_PRIVATE_KEY or an external signer before any state-changing command is run. <br>
Risk: State-changing scripts can approve tokens, mint test tokens, add liquidity, or post oracle data. <br>
Mitigation: Require a dry run and explicit user confirmation before executing commands that change blockchain state. <br>
Risk: The deployed workflow is intended for Sepolia testnet contracts and test tokens. <br>
Mitigation: Use only on Sepolia or an isolated local fork unless the contracts, configuration, and operational safeguards have been reviewed for another network. <br>


## Reference(s): <br>
- [GhostBot ACLM Architecture](artifact/references/architecture.md) <br>
- [Deployed Contracts Reference](artifact/references/contracts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AqilJaafree/ghostbot-uniswap-v4hooks-testnet) <br>
- [OpenClawACLMHook on Sepolia Etherscan](https://sepolia.etherscan.io/address/0xbD2802B7215530894d5696ab8450115f56b1fAC0) <br>
- [OpenClawOracle on Sepolia Etherscan](https://sepolia.etherscan.io/address/0x300Fa0Af86201A410bEBD511Ca7FB81548a0f027) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Sepolia Etherscan transaction links and contract addresses when commands interact with deployed contracts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
