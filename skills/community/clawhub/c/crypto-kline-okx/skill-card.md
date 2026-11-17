## Description:

Fetches historical OKX cryptocurrency K-line candlestick data for BTC and other spot pairs, with interval selection and timestamp-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u91win](https://clawhub.ai/user/u91win)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to retrieve OKX historical cryptocurrency candlestick data for spot trading pairs such as BTC-USDT, select intervals, and paginate by millisecond timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to OKX for public market data, so outputs depend on OKX availability and returned candle data.

Mitigation: Use it only where live OKX access is acceptable, and review market data before relying on it for trading or business decisions.

Risk: Untrusted http_proxy or https_proxy environment variables could tamper with returned candle data.

Mitigation: Run with trusted proxy settings or clear proxy environment variables before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/u91win/skills/crypto-kline-okx)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and tabular console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and live network access to OKX; public market data only.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
