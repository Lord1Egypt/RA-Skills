## Description:

Identifies A-share and Hong Kong stock candidates using three technical trading patterns: high-open momentum, N-shaped breakouts, and one strong bullish candle after three bearish candles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, short-term traders, and technical-analysis users can ask an agent for stock-screening signals and candidate summaries for A-share or Hong Kong markets. Outputs are informational and require independent financial review before any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release advertises paid real-time stock signals, but evidence says the packaged service returns hard-coded mock recommendations.

Mitigation: Treat outputs as unverified examples unless the publisher provides real data integration, timestamps, methodology, and current-market validation.

Risk: The stated x402 payment gate is not confirmed by the security evidence.

Mitigation: Do not rely on payment enforcement or paid-data access claims until the publisher demonstrates payment verification and dependency pinning.

Risk: Stock picks, targets, and stop-loss values can be incorrect or outdated.

Mitigation: Use the skill only as informational screening support and require independent financial analysis and risk controls before trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinboh68-prog/skills/a-stock-trading-signals)
- [Published API endpoint](https://a-stock-signals.vercel.app/s)
- [Published API base URL](https://a-stock-signals.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or structured text containing stock candidates, prices, percentage changes, capital inflow, signal strength, stop-loss levels, and target levels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require x402 payment for service access; review evidence indicates packaged behavior is not a verified real-time market-analysis source.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter shows 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
