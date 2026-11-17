## Description:

GhostBot ACLM helps agents manage Uniswap v4 concentrated liquidity on Ethereum Sepolia by adding liquidity, checking positions and pool statistics, monitoring oracle signals, and posting authorized rebalance or fee recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqiljaafree](https://clawhub.ai/user/aqiljaafree)

### License/Terms of Use:


## Use Case:

External DeFi developers and testnet operators use this skill to inspect and manage automated liquidity positions, pool state, and oracle-driven rebalance or fee signals for a Sepolia Uniswap v4 hook deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts include a default signing key and RPC endpoint for Sepolia transaction flows.

Mitigation: Use a dedicated testnet key with no mainnet funds, override DEPLOYER_PRIVATE_KEY and RPC_URL, and rotate or replace the embedded demo key before relying on the skill.

Risk: Liquidity actions can mint test tokens, approve hook spending, and create persistent Sepolia positions.

Mitigation: Review token allowances and transaction parameters before execution, keep usage on Sepolia, and inspect emitted Etherscan transaction links.

Risk: The dependency declaration uses an unpinned viem version range.

Mitigation: Install in an isolated workspace and prefer a release with pinned dependencies or a reviewed lockfile before operational use.

## Reference(s):

- [GhostBot ACLM Architecture](references/architecture.md)
- [Deployed Contracts Reference](references/contracts.md)
- [OpenClawACLMHook on Sepolia Etherscan](https://sepolia.etherscan.io/address/0xbD2802B7215530894d5696ab8450115f56b1fAC0)
- [OpenClawOracle on Sepolia Etherscan](https://sepolia.etherscan.io/address/0x300Fa0Af86201A410bEBD511Ca7FB81548a0f027)
- [ClawHub Skill Page](https://clawhub.ai/aqiljaafree/skills/ghostbot-uniswap-v4hooks-testnet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and transaction or status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Sepolia transaction links, position tables, pool statistics, token balances, and oracle signal summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
