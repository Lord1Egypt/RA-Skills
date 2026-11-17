## Description:

Stock market data query skill for China A-shares, Hong Kong, and US markets. Uses Tencent Finance HTTP API by default (lightweight, no install needed), with optional adata SDK for more comprehensive data. Supports real-time quotes, K-line history, order book analysis, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacksing](https://clawhub.ai/user/hacksing)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to retrieve stock quotes, historical K-line data, order book signals, and optional A-share market datasets for China A-shares, Hong Kong, and US markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols and query activity may be sent to third-party data providers.

Mitigation: Use the skill only when sharing queried symbols with those providers is acceptable.

Risk: Some quote examples use unencrypted HTTP market-data requests.

Mitigation: Do not rely on those responses for trading or other high-stakes decisions without checking against a trusted HTTPS source.

Risk: The optional adata install is shown without a pinned package version.

Mitigation: Install adata in an isolated environment and pin the package version before use.

Risk: Market data may be delayed and invalid symbols can return placeholder error values.

Mitigation: Check data freshness, handle invalid-code responses, and avoid high-frequency requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hacksing/skills/allstock-data)
- [Tencent Finance quote endpoint](http://qt.gtimg.cn/q=sh600519)
- [Tencent Finance K-line endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration]

**Output Format:** [Markdown with inline bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide an agent to call third-party market-data endpoints and optionally install and use the adata Python SDK.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
