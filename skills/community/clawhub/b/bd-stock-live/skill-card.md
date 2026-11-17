## Description:

Bangladesh stock market data and analytics for DSE (Dhaka Stock Exchange) - prices, signals, EMA channels, Fibonacci levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rashed-mamoon](https://clawhub.ai/user/rashed-mamoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and market analysts use this skill to retrieve Dhaka Stock Exchange prices, market summaries, news, historical data, and tier-gated trading analytics from StockAI Live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an API key and may access portfolio data tied to the StockAI Live account.

Mitigation: Install only when the StockAI Live service and account are trusted, keep STOCKAI_API_KEY private, and limit use to accounts with appropriate data access.

Risk: Overriding STOCKAI_API_BASE can create API-key transport risk if an insecure http URL is used.

Mitigation: Use the default HTTPS endpoint or set STOCKAI_API_BASE only to a trusted HTTPS stock-ai.live URL.

Risk: Command outputs include promotional CTA fields in addition to requested market data.

Mitigation: Treat fields such as _cta as promotional metadata and separate them from market data used for analysis or decisions.

Risk: Trading signals, EMA channels, Fibonacci levels, and portfolio outputs may be mistaken for investment advice.

Mitigation: Use the outputs as informational analytics and require human review before trading or portfolio decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rashed-mamoon/skills/bd-stock-live)
- [StockAI Live homepage](https://stock-ai.live)
- [StockAI Live documentation](https://stock-ai.live/docs)
- [StockAI Live API keys](https://stock-ai.live/api-keys)
- [StockAI Live pricing](https://stock-ai.live/pricing)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON objects printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STOCKAI_API_KEY; responses include requested market data or analytics and may include promotional CTA fields.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
