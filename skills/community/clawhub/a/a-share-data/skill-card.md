## Description:

A data-layer skill for A-share market quotes, financials, sectors, fund flows, and candlestick data with fallback across AkShare, Eastmoney, Sina, Tencent, and other sources.

This skill is for research and development only.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve A-share market data, financial data, sector data, fund-flow data, index data, cross-market prices, and FX data for downstream analysis workflows. It is a data access layer and does not provide investment advice or trading judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned finance data dependencies or provider API changes may change data availability or returned fields.

Mitigation: Install in an isolated Python environment, pin and review dependency versions, and validate provider responses before relying on outputs.

Risk: Market watchlists or compliance-sensitive research could expose confidential interests to third-party data providers.

Mitigation: Avoid confidential watchlists and confirm that the listed data providers are acceptable before use.

Risk: Data-access snippets could be mistaken for investment guidance in downstream workflows.

Mitigation: Keep downstream responses limited to source-attributed data with timestamps and separate any analysis or trading decisions from this skill.

## Reference(s):

- [Sina Finance quote endpoint](https://hq.sinajs.cn/list=sh600519)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q=sh600519)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes data-source attribution and timestamp guidance; outputs are guidance and code snippets rather than fetched market data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
