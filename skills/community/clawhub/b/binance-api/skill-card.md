## Description:

Fetch live and historical cryptocurrency market data, including prices, candlesticks, order books, trades, 24h statistics, futures funding rates, and open interest, using Binance public market-data APIs without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanookai](https://clawhub.ai/user/nanookai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to answer cryptocurrency market-data questions and produce API requests or code snippets for Binance spot, futures, WebSocket, and bulk-history data sources.

### Deployment Geography for Use:

Global, subject to Binance service availability and regional restrictions.

## Known Risks and Mitigations:

Risk: Generic cryptocurrency price requests may be answered using Binance data when a different exchange or index is intended.

Mitigation: Specify the desired market-data source or compare results against the exchange or index that matches the task.

Risk: Optional Python WebSocket examples require an additional runtime dependency.

Mitigation: Run examples in a pinned virtual environment and review dependencies before use.

Risk: Binance endpoints may be unavailable or restricted in some regions.

Mitigation: Handle HTTP 451 or connection failures as service availability constraints and use an appropriate regional data source when needed.

## Reference(s):

- [Binance API Skill](https://clawhub.ai/nanookai/skills/binance-api)
- [Binance Spot API Docs](https://github.com/binance/binance-spot-api-docs)
- [Binance Public Data](https://github.com/binance/binance-public-data)
- [Binance WebSocket Streams](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)
- [Spot REST endpoint reference](references/endpoints.md)
- [Futures market-data reference](references/futures.md)
- [WebSocket market streams](references/websocket-streams.md)
- [Bulk data archive](references/bulk-data.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with API examples, JSON shapes, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public market-data endpoints only; no account access, trading authority, persistence, or hidden execution behavior is indicated by security evidence.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
