## Description: <br>
GhostBot ACLM helps agents manage Uniswap v4 concentrated-liquidity positions on Ethereum Sepolia by checking status, adding liquidity, viewing positions, inspecting oracle signals, and reviewing pool statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AqilJaafree](https://clawhub.ai/user/AqilJaafree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate and inspect a Sepolia testnet Uniswap v4 automated concentrated-liquidity manager from an agent chat workflow. It supports liquidity-position setup, oracle-signal review, and pool-health reporting for the GhostBot ACLM contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts require a wallet private key and can submit wallet-signed blockchain transactions. <br>
Mitigation: Use only a throwaway Sepolia wallet with no valuable assets, and never provide a mainnet or production private key. <br>
Risk: Liquidity and oracle commands can mint tokens, approve contracts, add liquidity, or post signals once executed. <br>
Mitigation: Review the RPC network, wallet address, contract addresses, token amounts, approvals, tick ranges, autoRebalance setting, and slippage implications before running any transaction command. <br>
Risk: The security verdict is suspicious due to weak safeguards around blockchain transaction execution. <br>
Mitigation: Install and run the skill only after manual review, and treat every generated command as a proposal that requires user confirmation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AqilJaafree/ghostbot-aclm) <br>
- [GhostBot ACLM Architecture](references/architecture.md) <br>
- [Deployed Contracts Reference](references/contracts.md) <br>
- [OpenClawACLMHook on Sepolia Etherscan](https://sepolia.etherscan.io/address/0xbD2802B7215530894d5696ab8450115f56b1fAC0) <br>
- [OpenClawOracle on Sepolia Etherscan](https://sepolia.etherscan.io/address/0x300Fa0Af86201A410bEBD511Ca7FB81548a0f027) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise transaction or status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Sepolia Etherscan transaction links, contract addresses, position tables, oracle signal summaries, and pool statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
