## Description:

从零抓取 A 股当日盘面，按指数、广度、成交、板块、情绪、领涨股顺序重建临时全市场工作包。

This skill is ready for commercial/non-commercial use.

## Publisher:

[minguncle](https://clawhub.ai/user/minguncle)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, analysts, and market-review agents use this skill to reconstruct the current A-share session from live market evidence, including indices, breadth, sector strength, leading stocks, risks, and watchlists. It supports intraday review, closing summaries, theme scanning, and preparation for later stock-selection work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market and trading-framework outputs can become stale or reflect incomplete live data.

Mitigation: Verify timestamps, source data, and current market conditions independently before acting on the output.

Risk: Trading-oriented summaries may be mistaken for personalized financial advice.

Mitigation: Treat the output as informational market analysis and apply independent suitability, risk, and compliance review before making trades.

## Reference(s):

- [Sweep Order](references/sweep-order.md)
- [ClawHub Skill Page](https://clawhub.ai/minguncle/skills/a-share-market-sweep)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown sections covering the market conclusion, key evidence, temporary market database, trading framework, risk list, and watchlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-sensitive market analysis; outputs are informational and require independent verification before trading.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
