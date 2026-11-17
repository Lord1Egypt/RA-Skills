## Description:

AgentCanary provides API-based cross-asset market intelligence for AI agents, including macro regime context, risk signals, derivatives data, DeFi metrics, sentiment, and scheduled market briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrcerq](https://clawhub.ai/user/mrcerq)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use AgentCanary to fetch read-only market intelligence for risk assessment, market structure monitoring, signal confirmation, and informational portfolio context before deciding on strategy execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may appear in prompts, visible URLs, logs, or transcripts if users paste funded keys or URL examples containing keys.

Mitigation: Treat the AgentCanary API key as a secret, avoid pasting funded keys into prompts or visible URLs when possible, monitor usage, and rotate the key if exposure is suspected.

Risk: The skill relies on an external market-intelligence API, so responses depend on service availability, tier limits, billing status, and endpoint freshness.

Mitigation: Install only if external AgentCanary API usage is acceptable, monitor rate limits and billing status, and design agents to handle unavailable or stale responses.

Risk: Market signals and briefs may be mistaken for financial advice or deterministic predictions.

Mitigation: Use AgentCanary results as informational risk context only, and keep trading or portfolio decisions under user-approved strategy and review.

## Reference(s):

- [AgentCanary ClawHub skill page](https://clawhub.ai/mrcerq/skills/agentcanary)
- [AgentCanary API documentation](https://api.agentcanary.ai/api/docs)
- [AgentCanary application](https://app.agentcanary.ai)
- [AgentCanary website](https://agentcanary.ai)
- [AgentCanary public prediction track record data](https://agentcanary.ai/record/data/predictions.json)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON API responses and concise text guidance derived from API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only external API output may include market data, risk signals, sentiment, briefs, and informational intelligence; it does not execute trades.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
