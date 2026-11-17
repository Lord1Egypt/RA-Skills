## Description:

Crypto tax compliance skill for AI agents covering 1099-DA reconciliation, cost basis methods, multi-chain transaction reconstruction, Form 8949 generation, DEX gap analysis, staking and airdrop classification, bridge handling, and wash sale analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External tax professionals, developers, and agent operators use this skill to analyze cryptocurrency, NFT, and DeFi transaction history, reconcile broker reports, compute cost basis, and prepare federal tax reporting artifacts. It is intended for reporting and documentation workflows, with specialist review for legal, tax, or sanctions-sensitive issues.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Wallet addresses and tax records may be exposed through third-party blockchain or pricing services.

Mitigation: Confirm client consent before querying external services and avoid sharing API keys, private keys, or unnecessary personal data with the agent.

Risk: Crypto tax positions can depend on current law and uncertain treatment of bridge events, LP activity, privacy coins, sanctions exposure, or current-year law changes.

Mitigation: Have a CPA or tax attorney review uncertain or high-risk positions before filing or giving final advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/crypto-tax-agent)
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom)
- [Etherscan V2 API endpoint](https://api.etherscan.io/v2/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with structured tax form tables, CSV/TXF export guidance, transaction logs, and audit notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include normalized transaction classifications, Form 8949, Schedule D, TXF deliverables, reconciliation memos, and on-chain proof links.]

## Skill Version(s):

98.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
