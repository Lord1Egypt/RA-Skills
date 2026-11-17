## Description:

Fetches real-time Huobi market data and historical K-line data for major cryptocurrency spot trading pairs with configurable intervals and record counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u91win](https://clawhub.ai/user/u91win)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-data users can ask an agent to retrieve recent Huobi K-line records for cryptocurrency spot pairs such as btcusdt, ethusdt, or solusdt. The skill is useful for quick command-line checks of public OHLCV market data over common intervals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Node script makes outbound HTTPS requests to Huobi for public market data.

Mitigation: Install only in environments where outbound access to Huobi is acceptable and review network policy before use.

Risk: Symbol shorthand such as BTC may be rejected by the API even though examples mention major coins.

Mitigation: Use full Huobi spot trading pair symbols such as btcusdt, ethusdt, or solusdt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/u91win/skills/crypto-kline-data)
- [Huobi public kline API endpoint](https://api.huobi.pro/market/history/kline)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text with tabular K-line data and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and outbound HTTPS access to Huobi's public API.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
