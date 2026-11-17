## Description:

Provides token search, metadata, real-time market data, and OHLCV candlestick lookups by keyword, symbol, or contract address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query token information across supported chains, including token search results, static metadata, market metrics, holder and liquidity data, and candlestick series for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token query parameters passed to the CLI are sent to Binance Web3 endpoints, and kline requests are sent to dquery.sintral.io.

Mitigation: Pass only the token lookup fields required for the requested query, and do not include API keys, wallet secrets, private notes, or unrelated context in the JSON parameters.

## Reference(s):

- [CLI Reference](artifact/references/cli.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses include token data from Binance Web3 endpoints and kline data from dquery.sintral.io.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
