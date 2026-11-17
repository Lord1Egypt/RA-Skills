## Description:

DeFi intelligence suite - token metrics, perp trading data, technical analysis, smart money flows, staking yields, and AI-powered market research across Base, Solana, and 10+ perp DEXs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dapplooker](https://clawhub.ai/user/dapplooker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request DappLooker DeFi market intelligence, including token metrics, perpetuals data, technical analysis, smart money flows, staking yields, and AI-generated market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls can incur USDC charges when users approve requests.

Mitigation: Keep per-call confirmation, no-retry, and default session budget controls enabled.

Risk: API keys supplied in an api_key URL parameter may be exposed in logs, browser history, or shared traces.

Mitigation: Prefer x402 payment or a safer header-based credential flow, and avoid placing API keys in URLs.

Risk: Market intelligence and AI-generated trading strategies can be incomplete, stale, or unsuitable for a user's risk profile.

Mitigation: Present outputs as decision-support information and require user review before acting on trading recommendations.

## Reference(s):

- [DappLooker API documentation](https://docs.dapplooker.com/products/api-endpoints)
- [ClawHub skill page](https://clawhub.ai/dapplooker/skills/dapplooker-ai)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, JSON, guidance]

**Output Format:** [Markdown and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 API calls require user confirmation and are subject to the skill's per-call pricing and session budget guidance.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
