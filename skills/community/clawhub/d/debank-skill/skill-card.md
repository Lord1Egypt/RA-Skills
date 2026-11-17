## Description:

Query blockchain wallet data, including balances, DeFi positions, tokens, NFTs, transaction history, gas prices, and token approvals across EVM chains through the DeBank API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lolieatapple](https://clawhub.ai/user/lolieatapple)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect EVM wallet portfolios, token balances, DeFi positions, NFTs, approvals, transaction history, gas prices, and DeBank account usage from natural language or direct CLI-style requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a globally available, unpinned debank-cli package.

Mitigation: Review before installing, avoid sudo or administrator installation, and use a pinned, locally installed debank-cli version where possible.

Risk: Wallet addresses, ENS names, transaction history, approvals, and portfolio queries are financial metadata sent to DeBank.

Mitigation: Treat requested wallet data as sensitive financial metadata and use a dedicated DeBank API key.

Risk: A saved DeBank API key can persist after the skill is no longer needed.

Mitigation: Remove the key with debank config remove-key when access is no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lolieatapple/skills/debank-skill)
- [DeBank Pro API](https://cloud.debank.com/)
- [debank-cli repository](https://github.com/lolieatapple/debank-cli)
- [debank-skill repository](https://github.com/lolieatapple/debank-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial metadata returned by DeBank, such as wallet balances, token holdings, approvals, and transaction history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
