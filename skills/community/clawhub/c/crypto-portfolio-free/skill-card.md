## Description:

加密组合跟踪 helps users track crypto portfolios across multi-chain wallets, centralized exchanges, and prediction-market positions, with structured analysis of balances, returns, and risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review crypto holdings across wallets, centralized exchanges, and prediction markets, then generate portfolio, return, and risk summaries. It should be treated as analytical assistance, especially when financial actions or sensitive account data are involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trade execution and broad command or file capabilities could enable unintended financial or system actions.

Mitigation: Do not provide exchange trading keys, wallet-signing access, or command authority unless the deployment enforces explicit confirmation for every trade and file or system change.

Risk: Crypto portfolio analysis can involve sensitive account, wallet, and market-position data.

Mitigation: Use least-privilege API access, keep secrets in environment-managed storage, avoid private-key access, and review outputs for sensitive data before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/crypto-portfolio-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Markdown or JSON with structured portfolio-analysis results and execution status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request or process crypto portfolio inputs and API-backed market data; outputs should avoid exposing secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
