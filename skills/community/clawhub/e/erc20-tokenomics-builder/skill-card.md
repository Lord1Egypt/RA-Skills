## Description:

Design and model ERC20 tokenomics with vesting schedules, allocation tables, Uniswap liquidity math, and investor documentation for new token launches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and token launch teams use this skill to plan ERC20 allocations, vesting schedules, Uniswap liquidity, launch valuation, and investor-facing token documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vesting deployment examples may create contracts and transfer real treasury tokens.

Mitigation: Treat deployment code as illustrative, test on a testnet first, and require explicit confirmation before broadcasting transactions or transferring tokens.

Risk: Incorrect chain IDs, token addresses, beneficiary addresses, schedules, balances, allowances, or token decimals can cause irreversible token allocation errors.

Mitigation: Verify chain ID and addresses, read token decimals with parseUnits, confirm balances and allowances, and validate every beneficiary and vesting schedule before execution.

Risk: Token transfer examples may omit defensive transfer handling.

Mitigation: Use SafeERC20 or equivalent checked transfer logic before adapting examples for production deployment.

## Reference(s):

- [ERC20 Tokenomics Builder on ClawHub](https://clawhub.ai/samledger67-dotcom/skills/erc20-tokenomics-builder)
- [VestingWallet Factory - Batch Deployment](references/vesting-factory.md)
- [Uniswap v2/v3 Liquidity Math](references/uniswap-math.md)
- [Token Allocation Templates by Project Type](references/allocation-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, formulas, Solidity and JavaScript examples, JSON examples, and shell-oriented deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include illustrative vesting deployment code and token transfer workflows that require user review before use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
