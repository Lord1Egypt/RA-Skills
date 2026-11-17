## Description:

Real-time Bitcoin trading intelligence API providing market data, AI trade signals, derivatives flow, liquidation heatmaps, live crypto news, economic calendar, historical OHLCV, and 50+ data sources for AI-driven trade decisions and automated trading bots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricklaughhunn](https://clawhub.ai/user/ricklaughhunn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading-system builders use this skill to query BTC Signals Pro for Bitcoin market snapshots, signals, derivatives flow, news, macro calendar data, historical OHLCV, and trade setup analysis through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives aggressive financial decision support that could lead an agent to open, modify, or close positions without strong user-control guardrails.

Mitigation: Keep it disconnected from exchange, broker, wallet, and order-placement tools unless trading automation is intentionally enabled and every order, modification, or close action requires explicit confirmation.

Risk: The skill requires a BTC Signals Pro API key for paid API access.

Mitigation: Store BTC_SIGNALS_API_KEY only in the agent configuration, pass it via the X-API-Key header, and do not print or share the full key.

## Reference(s):

- [BTC Signals Pro API Reference](references/api-reference.md)
- [BTC Signals Pro API](https://api.btcsignals.pro/v1)
- [BTC Signals Pro Pricing](https://btcsignals.pro/pricing)
- [ClawHub Skill Page](https://clawhub.ai/ricklaughhunn/skills/btc-signals-pro)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON API response summaries and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BTC_SIGNALS_API_KEY and a BTC Signals Pro data plan; API calls are rate limited to 60 requests per minute.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
