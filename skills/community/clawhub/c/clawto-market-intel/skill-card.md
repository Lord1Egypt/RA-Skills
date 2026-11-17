## Description:

Aggregates Chinese-localized market intelligence across fear-and-greed sentiment, equity index quotes, market news, economic calendar items, and cryptocurrency technical analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawto](https://clawhub.ai/user/clawto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to request concise market snapshots and cryptocurrency analysis in Chinese from public financial data sources. It supports quick sentiment checks, index quote reviews, market headline summaries, macro calendar lookups, and multi-timeframe crypto analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market outputs may be incomplete, delayed, or unsuitable as the sole basis for trading decisions.

Mitigation: Treat outputs as informational and verify trading or calendar-sensitive decisions against authoritative sources before acting.

Risk: The economic-calendar module includes static scheduled events that may become outdated.

Mitigation: Cross-check macro calendar events with current official or trusted financial-calendar sources before relying on them.

Risk: The skill makes outbound requests to public financial data providers.

Mitigation: Install only in environments where outbound requests to public market-data and news providers are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawto/skills/clawto-market-intel)
- [Crypto Analysis Framework](references/crypto-analysis.md)
- [Alternative.me Fear & Greed API](https://api.alternative.me/fng/?limit=1)
- [CNN Fear & Greed graph data](https://production.dataviz.cnn.io/index/fearandgreed/graphdata)
- [CNBC market news RSS](https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114)
- [MarketWatch top stories RSS](https://feeds.marketwatch.com/marketwatch/topstories)
- [Eastmoney quote API](https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&secids={symbols}&fields={fields}&ut=fa5fd1943c7b386f172d6893dbfba10b)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-localized text and Markdown reports with shell command outputs and JSON market-data blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; output depends on outbound public market-data requests and includes informational market commentary.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
