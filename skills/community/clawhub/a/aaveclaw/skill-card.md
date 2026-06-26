## Description: <br>
aaveclaw helps agents interact with Aave V3 on Base Sepolia to deposit WETH collateral, borrow or repay USDC, withdraw collateral, check account health, and mint test tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chainyoda](https://clawhub.ai/user/chainyoda) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage a Base Sepolia Aave V3 testnet lending position through agent-run shell commands. It supports checking health factor, minting test tokens, depositing collateral, borrowing, repaying, and withdrawing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a raw wallet private key and can sign blockchain transactions. <br>
Mitigation: Use a dedicated disposable Base Sepolia testnet wallet, avoid mainnet or valuable keys, and prefer environment-based key handling or tightly permissioned config files. <br>
Risk: Deposit, borrow, repay, withdraw, faucet, and token approval commands change wallet or Aave testnet state. <br>
Mitigation: Confirm token amounts, network, and contract addresses before execution, and run the health check before and after state-changing operations. <br>
Risk: Borrowing against collateral can create liquidation risk if the health factor becomes too low. <br>
Mitigation: Keep a collateral buffer, warn when health factor is below 1.5, and use Aave's revert behavior as a final guard rather than the primary safety check. <br>
Risk: The scripts may grant large token allowances to the Aave pool. <br>
Mitigation: Review allowances after use and revoke or limit approvals when the testnet workflow is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chainyoda/aaveclaw) <br>
- [Base Sepolia RPC endpoint](https://sepolia.base.org) <br>
- [Base Sepolia explorer](https://sepolia.basescan.org) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain-text transaction summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Base Sepolia wallet private key through X402_PRIVATE_KEY or x402-config.json; state-changing commands may sign testnet blockchain transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
