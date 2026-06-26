## Description: <br>
Monitors Ethereum wallet and contract activity, detects simple risk flags, and summarizes balances, transactions, and ERC-20 token transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinu4you](https://clawhub.ai/user/jinu4you) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and external users can monitor an Ethereum address with Etherscan-backed balance, transaction, and token-transfer checks, then receive risk flags and a short LLM-generated Markdown summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and transaction context may be sent to Etherscan and configured LLM providers. <br>
Mitigation: Use only with wallet metadata that is acceptable to share with those services, and treat transaction context as potentially sensitive. <br>
Risk: Running npm start launches a sample monitoring job automatically. <br>
Mitigation: Review the configured payload and logs before running in shared or production environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jinu4you/agent-onchain-watch) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Analysis] <br>
**Output Format:** [JSON job result containing wallet data, risk flags, and a short Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Ethereum address input and API keys for live Etherscan and LLM-provider calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
