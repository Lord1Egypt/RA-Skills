## Description:

Manage ATX on BSC with wallet creation, price and balance queries, PancakeSwap V3 swaps, liquidity operations, LP positions and holdings, and BNB/ERC20 transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentswapx](https://clawhub.ai/user/agentswapx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage an ATX wallet on BSC, refresh current balances and LP positions, preview ATX/USDT swaps or liquidity changes, and execute confirmed transfers or DeFi transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage a BSC wallet with real assets and submit swaps, transfers, and liquidity transactions.

Mitigation: Keep wallet balances limited, inspect each preview, and require explicit user confirmation before any write transaction.

Risk: Wallet credentials and encrypted keystore backups are sensitive even when the raw private key is not exposed.

Mitigation: Use a strong unique wallet password, prefer writing protected keystore exports to local files, and avoid sharing keystore material through uncontrolled channels.

Risk: Passing wallet passwords through non-interactive command-line arguments can expose them through shell history or process listings.

Mitigation: Use interactive password entry or protected local secret storage when available, and avoid placing wallet passwords in command-line arguments.

Risk: Network or RPC ambiguity during transfer submission could lead to duplicate sends if retried blindly.

Mitigation: After a transaction hash or ambiguous submission, inspect chain or wallet state before retrying and confirm whether the user intends a new transfer.

## Reference(s):

- [ATXSwap skill source](https://github.com/agentswapx/skills/tree/main/atxswap)
- [ATXSwap SDK on npm](https://www.npmjs.com/package/atxswap-sdk)
- [ATXSwap SDK source and docs](https://github.com/agentswapx/atxswap-sdk)
- [ATXSwap team introduction](https://docs.atxswap.com/guide/team)
- [ATXSwap team introduction (ZH)](https://docs.atxswap.com/zh/guide/team)
- [ClawHub skill page](https://clawhub.ai/agentswapx/skills/atxswap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live on-chain query summaries, transaction hashes, wallet metadata, and encrypted keystore backup material when explicitly requested by the user.]

## Skill Version(s):

0.0.31 (source: frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
