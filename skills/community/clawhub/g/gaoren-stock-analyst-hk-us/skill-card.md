## Description:

Provides stock quote lookup and technical/news-based analysis for Hong Kong, U.S., and A-share equities using Futu, Finnhub, and Tencent Finance data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request stock-code analysis and receive informational market snapshots, technical indicators, news sentiment, and trading-suggestion style reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present trading recommendations based on simulated or weakly grounded technical indicators.

Mitigation: Treat reports as informational only, disclose when historical market data is unavailable, and disable recommendation wording unless calculations use verified market data.

Risk: The artifact includes an exposed Finnhub API token.

Mitigation: Rotate or remove the embedded token and require credentials through a safe user-provided secret or environment variable.

Risk: The skill makes network requests to market and news data providers.

Mitigation: Disclose external data sources and require review before installation or execution in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/skills/gaoren-stock-analyst-hk-us)
- [Futu stock page example](https://www.futunn.com/stock/03998-HK)
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q=hk{code})
- [Finnhub quote endpoint](https://finnhub.io/api/v1/quote?symbol={code})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console-style text or Markdown analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational and may depend on network data sources and user-provided stock symbols.]

## Skill Version(s):

2.1.0 (source: server release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
