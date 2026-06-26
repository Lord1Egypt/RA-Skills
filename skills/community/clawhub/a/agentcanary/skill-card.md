## Description: <br>
AgentCanary helps agents retrieve cross-asset market intelligence, including macro regimes, risk scores, trading signals, whale alerts, derivatives data, DeFi intelligence, options flow, and AI market briefs through an external API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrcerq](https://clawhub.ai/user/mrcerq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill when an agent needs market-regime context, risk assessment, position-sizing guidance, market-structure data, derivatives positioning, whale monitoring, news sentiment, DeFi intelligence, options flow, or institutional positioning. The skill guides API-only access to AgentCanary data and does not provide financial advice, place orders, or replace execution logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires external AgentCanary market-data calls and may consume paid API credits. <br>
Mitigation: Install and use it only when paid AgentCanary API access is intended, and monitor tier limits, credit usage, and endpoint access before broad agent deployment. <br>
Risk: Wallet-based setup and stablecoin deposits can expose users to payment mistakes. <br>
Mitigation: Keep API keys out of chat and logs where possible, and manually verify every wallet address, token, and chain before sending funds. <br>
Risk: Market intelligence and signals may be mistaken for investment advice or execution authority. <br>
Mitigation: Treat responses as informational risk context only; require separate trading logic, human review where appropriate, and independent validation before financial decisions. <br>


## Reference(s): <br>
- [AgentCanary ClawHub listing](https://clawhub.ai/mrcerq/agentcanary) <br>
- [AgentCanary API base URL](https://api.agentcanary.ai/api) <br>
- [AgentCanary API docs](https://api.agentcanary.ai/api/docs) <br>
- [AgentCanary app](https://app.agentcanary.ai) <br>
- [AgentCanary website](https://agentcanary.ai) <br>
- [AgentCanary prediction track record data](https://agentcanary.ai/record/data/predictions.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with HTTP endpoint examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API usage may require wallet-based authentication, deposited credits, tier-specific rate limits, and manual verification of wallet addresses, tokens, and chains before payment.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
