## Description: <br>
Integrate DeFi protocols on Celo. Use when building swaps, lending, or liquidity applications with Uniswap, Aave, Ubeswap, or other DeFi protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[san-npm](https://clawhub.ai/user/san-npm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill as reference guidance for building Celo DeFi integrations, including swaps, lending and borrowing, liquidity provision, and token approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or stale DeFi contract addresses could route users to the wrong protocol contracts. <br>
Mitigation: Verify contract addresses against primary protocol documentation before use, especially before mainnet transactions. <br>
Risk: Swap, approval, borrowing, and lending examples can cause irreversible transactions or unexpected financial loss when used with real funds. <br>
Mitigation: Test on Alfajores or a simulation first, use bounded slippage and exact allowances, and require explicit wallet confirmations. <br>
Risk: Borrowing and lending integrations can expose users to liquidation and interest-rate risk. <br>
Mitigation: Explain borrow, liquidation, approval, and irreversible-transaction risks clearly in any user-facing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/san-npm/celo-defi) <br>
- [Celo DeFi contract addresses](references/contract-addresses.md) <br>
- [Uniswap Celo deployments](https://docs.uniswap.org/contracts/v3/reference/deployments/celo-deployments) <br>
- [Celo Uniswap contracts](https://docs.celo.org/tooling/contracts/uniswap-contracts) <br>
- [Ubeswap contract addresses](https://docs.ubeswap.org/code-contracts/contract-addresses) <br>
- [Aave address book](https://github.com/bgd-labs/aave-address-book) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with TypeScript and JSON code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes contract-address reference material and transaction-oriented DeFi examples.] <br>

## Skill Version(s): <br>
1.0.2011 (source: ClawHub release evidence; artifact frontmatter metadata.version is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
