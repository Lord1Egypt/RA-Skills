## Description: <br>
Borrow from Aave via credit delegation. Agent self-funds by borrowing against delegator collateral. Supports borrow, repay, health checks. Works on Aave V2/V3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjmars](https://clawhub.ai/user/aaronjmars) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to give an agent a constrained Aave credit-delegation workflow for checking delegation status, borrowing, repaying, and monitoring health-factor safety before on-chain actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real on-chain borrowing and repayment authority through Aave credit delegation. <br>
Mitigation: Install only with a dedicated low-balance agent wallet, set small per-asset delegation limits, manually review borrow and repay actions, and revoke delegation when idle. <br>
Risk: Private-key handling may expose the agent wallet if secrets are stored in plaintext configuration. <br>
Mitigation: Prefer environment variables or a secret manager, restrict configuration file permissions, and never use the delegator's main private key in the agent workspace. <br>
Risk: Borrowing can reduce the delegator's Aave health factor and create liquidation exposure. <br>
Mitigation: Use conservative health-factor thresholds, test on testnet first, monitor the Aave position externally, and keep per-transaction borrow caps small. <br>


## Reference(s): <br>
- [Agent Credit ClawHub page](https://clawhub.ai/aaronjmars/agent-credit) <br>
- [Aave V3 Docs](https://docs.aave.com/developers) <br>
- [Aave Credit Delegation Guide](https://docs.aave.com/developers/guides/credit-delegation) <br>
- [Aave DebtToken Reference](https://docs.aave.com/developers/tokens/debttoken) <br>
- [Foundry Book](https://book.getfoundry.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operational guidance for Aave credit delegation workflows; on-chain transactions require user-provided configuration and wallet authority.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
