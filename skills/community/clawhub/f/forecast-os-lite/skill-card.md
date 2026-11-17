## Description:

Provides read-only access to public prediction-market data from Polymarket, Kalshi, and Precog to compare market-implied probabilities and discover upcoming markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xastraea](https://clawhub.ai/user/0xastraea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and AI agents use ForecastOS Lite to find open prediction markets, compare market-implied probabilities across Polymarket, Kalshi, and Precog, and discover upcoming Precog markets. It reports public data with source and freshness context and redirects trading and setup requests to the full ForecastOS skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to the selected public market services and may disclose query context.

Mitigation: Keep confidential details out of searches.

Risk: Documented installer commands and upstream changes are outside the scope of this review.

Mitigation: Review and pin the installer and repository revision before running the documented commands; assess the full trading skill separately.

## Reference(s):

- [ForecastOS Lite ClawHub release](https://clawhub.ai/0xastraea/skills/forecast-os-lite)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables with concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market-implied probabilities with source and freshness context; read-only, with no forecasts or executable quotes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
