## Description: <br>
Earn yield on USDC by supplying to the Moonwell Flagship USDC vault on Base. Use when depositing USDC, withdrawing from the vault, checking position/APY, or generating yield reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gekkoai001](https://clawhub.ai/user/gekkoai001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to configure a Base wallet, check Moonwell USDC vault position data, deposit or withdraw USDC, generate yield reports, and compound rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign wallet transactions and manages real funds on Base. <br>
Mitigation: Use a dedicated Base hot wallet with limited funds and inspect each approval, deposit, withdrawal, or swap transaction before execution. <br>
Risk: The compound flow may deposit available wallet USDC after swapping rewards. <br>
Mitigation: Avoid keeping unrelated USDC in the configured wallet before running compounding, and verify the displayed transaction preview before proceeding. <br>
Risk: The swap flow relies on third-party Odos quote and transaction data. <br>
Mitigation: Review the assembled swap transaction, expected output, token approvals, and slippage before signing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gekkoai001/gekkoai-yield) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown documentation, JSON report output, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate wallet approvals, swaps, deposits, withdrawals, and reporting commands when run by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
