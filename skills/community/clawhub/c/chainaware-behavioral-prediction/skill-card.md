## Description: <br>
ChainAware Behavioral Prediction helps agents evaluate blockchain wallets, smart contracts, tokens, liquidity pools, and AI agent wallets for fraud risk, rug-pull risk, behavioral intent, creditworthiness, community quality, and trustworthiness using ChainAware's remote MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chainaware](https://clawhub.ai/user/chainaware) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, DeFi teams, compliance analysts, and agent builders use this skill to screen wallets and contracts, personalize DeFi interactions, rank token communities, and support lending or onboarding decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, contract or LP addresses, network identifiers, and the ChainAware API key are sent to ChainAware's remote service. <br>
Mitigation: Use a restricted API key where possible, keep keys in environment variables, and avoid submitting private keys, seed phrases, or off-chain personal data. <br>
Risk: Predictive fraud, rug-pull, behavioral, or credit scores can be incomplete or incorrect if used as the sole basis for financial, compliance, onboarding, or investment decisions. <br>
Mitigation: Treat results as decision support, review supporting signals, and add human or compliance review before taking high-impact action. <br>
Risk: Unsupported network and tool combinations can lead to failed or misleading requests. <br>
Mitigation: Confirm the address type and network before calling tools, and use only the documented network support for each capability. <br>


## Reference(s): <br>
- [ChainAware Behavioral Prediction MCP](https://github.com/ChainAware/behavioral-prediction-mcp) <br>
- [ChainAware MCP Server Endpoint](https://prediction.mcp.chainaware.ai/sse) <br>
- [ChainAware Privacy Policy](https://chainaware.ai/privacy) <br>
- [Fraud Detection Accuracy](https://chainaware.ai/scam-db) <br>
- [Rug Pull Detection Accuracy](https://chainaware.ai/resources/rugpull-verification) <br>
- [ChainAware Pricing and API Key](https://chainaware.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown or plain text summaries with risk scores, recommendations, and MCP result interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CHAINAWARE_API_KEY for predictive and scoring calls; batch workflows use job_id and signature for result retrieval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
