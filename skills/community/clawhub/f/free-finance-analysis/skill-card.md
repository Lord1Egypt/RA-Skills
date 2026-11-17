## Description:

Analyzes stocks, ETFs, indexes, and commodities using public market data, technical indicators, sentiment signals, and financial news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT

## Use Case:

External users and analysts use this skill to produce structured market analysis reports for equities, ETFs, indexes, and commodities. It is intended for informational analysis, risk framing, and stop-profit or stop-loss planning, not for trade execution or professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's market-analysis output could influence real investment decisions even though it is informational.

Mitigation: Treat outputs as non-professional analysis, verify data independently, and apply the user's own risk tolerance or a licensed adviser before making trades.

Risk: Public web data used by the skill may be delayed, incomplete, inaccurate, or unavailable.

Mitigation: Require explicit data-completeness reporting, label failed data pulls, and avoid replacing missing facts with assumptions.

Risk: Suggested thresholds, position sizing examples, and stop-profit or stop-loss ranges may not fit a user's financial situation.

Mitigation: Use thresholds as planning prompts only and review them against portfolio context, liquidity, volatility, and loss tolerance.

## Reference(s):

- [Free Finance Analysis on ClawHub](https://clawhub.ai/ucsdzehualiu/skills/free-finance-analysis)
- [Data Sources](references/data-sources.md)
- [Technical Analysis](references/technical-analysis.md)
- [Fundamental Analysis](references/fundamental-analysis.md)
- [Stop-Profit and Stop-Loss Strategy](references/stop-profit-loss.md)
- [CNBC Quote Pages](https://www.cnbc.com/quotes/{SYMBOL})
- [Benzinga Quote Pages](https://www.benzinga.com/quote/{SYMBOL})
- [CNN Fear and Greed Index](https://www.cnn.com/markets/fear-and-greed)
- [Current Market Valuation](https://www.currentmarketvaluation.com/)
- [Jin10 Market News](https://www.jin10.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown market-analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include data-completeness notes, market indicators, technical and fundamental analysis, sentiment context, risk points, and stop-profit or stop-loss ranges.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
