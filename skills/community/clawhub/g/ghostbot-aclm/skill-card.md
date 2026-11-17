## Description:

GhostBot Uniswap v4 helps agents manage Sepolia testnet Uniswap v4 concentrated liquidity positions through scripts for status checks, liquidity actions, position views, oracle signals, and pool statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqiljaafree](https://clawhub.ai/user/aqiljaafree)

### License/Terms of Use:


## Use Case:

Developers and DeFi users use this skill to inspect and operate a Sepolia testnet Uniswap v4 automated concentrated liquidity manager from an agent chat workflow. It supports liquidity provisioning, position monitoring, oracle signal review, and pool statistics for the deployed GhostBot ACLM contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign blockchain transactions and handle private keys.

Mitigation: Use a dedicated low-value Sepolia key that is not reused elsewhere and review transaction details before running write commands.

Risk: The scripts require a private key even for read-only queries.

Mitigation: Provide only a testnet key for the intended Sepolia deployment and avoid using wallets that hold real funds.

Risk: Approvals and zero-slippage liquidity defaults need review before reuse beyond the testnet deployment.

Mitigation: Treat approval amounts and slippage settings as review items before adapting this pattern outside Sepolia.

## Reference(s):

- [GhostBot ACLM Architecture](references/architecture.md)
- [Deployed Contracts Reference](references/contracts.md)
- [OpenClawACLMHook on Sepolia Etherscan](https://sepolia.etherscan.io/address/0xbD2802B7215530894d5696ab8450115f56b1fAC0)
- [OpenClawOracle on Sepolia Etherscan](https://sepolia.etherscan.io/address/0x300Fa0Af86201A410bEBD511Ca7FB81548a0f027)
- [ClawHub skill page](https://clawhub.ai/aqiljaafree/skills/ghostbot-aclm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and blockchain transaction links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run Node.js scripts that read from or write to Ethereum Sepolia contracts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
