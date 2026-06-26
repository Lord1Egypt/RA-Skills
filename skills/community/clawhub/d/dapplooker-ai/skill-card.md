## Description: <br>
DeFi intelligence suite for token metrics, perp trading data, technical analysis, smart money flows, staking yields, and AI-powered market research across Base, Solana, and 10+ perp DEXs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dapplooker](https://clawhub.ai/user/dapplooker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use DappLooker AI to retrieve paid DeFi market intelligence, token analytics, smart-money and staking signals, perp DEX data, and AI-generated market research across supported chains and DEXs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make paid USDC API calls for DeFi intelligence. <br>
Mitigation: Confirm the endpoint, cost, payment network, and remaining session budget before each paid call, and do not retry failed paid calls without approval. <br>
Risk: Prompts and parameters may reveal token interests, contract addresses, market questions, strategy prompts, or trading context to DappLooker. <br>
Mitigation: Avoid sending private portfolio details, proprietary trading strategies, or other sensitive information unless the user explicitly accepts that disclosure. <br>
Risk: AI-generated market and perp strategy recommendations may be incomplete, stale, or unsuitable for a user's risk profile. <br>
Mitigation: Present recommendations as informational analysis and ask the user to independently verify the data before making financial decisions. <br>


## Reference(s): <br>
- [DappLooker API documentation](https://docs.dapplooker.com/products/api-endpoints) <br>
- [ClawHub skill release page](https://clawhub.ai/dapplooker/dapplooker-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown and text summaries with API-backed market data and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 API calls require user confirmation, disclose per-call cost, and use a default session spending cap unless the user raises it.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
