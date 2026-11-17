## Description:

Calls a configured daily_stock_analysis service to analyze stock tickers and summarize trends, trading guidance, and price levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and analysts use this skill to request stock analysis by ticker and read a concise summary of trends, suggested actions, and available trading levels from their configured DSA service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-analysis requests and optional chat messages are sent to the configured DSA service.

Mitigation: Use only a trusted DSA service and avoid including sensitive personal or account information in prompts.

Risk: Chinese company names may resolve ambiguously to stock tickers.

Mitigation: Confirm the intended ticker before requesting or acting on an analysis.

Risk: Trading guidance and price levels may be unsuitable for an individual decision.

Mitigation: Independently review the analysis and current market information before making a trade.

## Reference(s):

- [daily_stock_analysis project documentation](https://github.com/ZhuLinsen/daily_stock_analysis)
- [OpenClaw skill integration guide](https://github.com/ZhuLinsen/daily_stock_analysis/blob/main/docs/openclaw-skill-integration.md)
- [ClawHub skill listing](https://clawhub.ai/liberalchang/skills/dsa-stock-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trend predictions, operation advice, and buy, stop-loss, or take-profit levels when the service returns them.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
