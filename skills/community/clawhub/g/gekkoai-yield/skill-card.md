## Description:

Earn yield on USDC by supplying to the Moonwell Flagship USDC vault on Base. Use when depositing USDC, withdrawing from the vault, checking position/APY, or generating yield reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gekkoai001](https://clawhub.ai/user/gekkoai001)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to manage USDC yield activity on Base, including setup, deposits, withdrawals, position checks, APY reporting, and reward compounding for the Moonwell Flagship USDC vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage real funds from a configured wallet.

Mitigation: Use a dedicated hot wallet with limited balances and keep only the funds needed for the intended Base transactions.

Risk: The auto-compound command relies on Odos and may sign a third-party-built swap transaction before depositing available USDC into the vault.

Mitigation: Avoid running compound.ts unless the assembled transaction and intended deposit amount have been independently reviewed.

Risk: Deposits, withdrawals, approvals, swaps, and compounding require wallet signing and network interaction on Base.

Mitigation: Review transaction previews, verify contract addresses, and confirm gas and asset balances before approving execution.

## Reference(s):

- [Gekko Yield ClawHub skill page](https://clawhub.ai/gekkoai001/skills/gekkoai-yield)
- [gekkoai001 ClawHub publisher profile](https://clawhub.ai/user/gekkoai001)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output with inline shell commands, plus optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and wallet configuration before executing scripts that interact with Base.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
