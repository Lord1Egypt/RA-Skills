## Description: <br>
Crypto tax compliance skill for AI agents. Covers 1099-DA reconciliation, cost basis methods (FIFO/HIFO/SpecID), multi-chain transaction reconstruction via Etherscan V2 API, Form 8949 generation, DEX gap analysis, staking/airdrop classification, bridge handling, and wash sale analysis. Use when an agent needs to handle crypto tax work, analyze transaction history, or generate tax forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and tax-focused agents use this skill to analyze crypto, NFT, and DeFi transaction history, reconcile 1099-DA records, reconstruct cost basis, and prepare federal crypto tax reporting deliverables. It supports reporting workflows and flags issues that need CPA, counsel, or specialist review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, exchange CSVs, transaction histories, API keys, and generated tax forms may expose sensitive financial records. <br>
Mitigation: Use user-approved storage, restrict disclosure to third-party APIs, limit retained data, and document client consent before processing or sharing records. <br>
Risk: Generated crypto tax positions or forms may be incomplete or unsuitable for filing without professional review. <br>
Mitigation: Have a qualified tax professional review final filings, bridge handling, LP treatment, wash sale analysis, and other uncertain positions before submission. <br>


## Reference(s): <br>
- [Crypto Tax Agent ClawHub release page](https://clawhub.ai/samledger67-dotcom/crypto-tax-agent) <br>
- [Etherscan V2 API endpoint](https://api.etherscan.io/v2/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown guidance with tax form, CSV, TXF export, reconciliation memo, transaction log, and audit note deliverable specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can involve sensitive wallet addresses, exchange CSVs, transaction histories, API keys, and generated tax forms.] <br>

## Skill Version(s): <br>
98.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
