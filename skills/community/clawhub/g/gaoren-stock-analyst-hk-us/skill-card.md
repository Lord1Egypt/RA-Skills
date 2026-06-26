## Description: <br>
智能股票分析系统 v2.1 - 港股/美股/A股实时行情 + 富途数据源 + 技术指标 + 综合报告(7大板块) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoren36-arch](https://clawhub.ai/user/gaoren36-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve HK, US, and A-share market data and generate stock analysis reports with technical indicators, news sentiment, and trading-oriented suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols and related queries may be sent to third-party market and news APIs. <br>
Mitigation: Use only with symbols and context that may be shared with those services, and document the external services before deployment. <br>
Risk: Some technical indicators or suggestions may be generated from simulated or incomplete market data. <br>
Mitigation: Treat outputs as informational, verify against authoritative market data, and do not rely on them as financial advice. <br>
Risk: Artifact files include exposed API tokens or token fallbacks. <br>
Mitigation: Remove or rotate exposed tokens and require secrets to be provided through environment variables or approved secret storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaoren36-arch/gaoren-stock-analyst-hk-us) <br>
- [Publisher profile](https://clawhub.ai/user/gaoren36-arch) <br>
- [Futu HK stock pages](https://www.futunn.com/stock/{code}-HK) <br>
- [Tencent Finance quote API](https://qt.gtimg.cn/q={market}) <br>
- [Finnhub quote API](https://finnhub.io/api/v1/quote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style stock analysis report with inline command examples and plain-text market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market quotes, technical indicators, news sentiment, analyst-style ratings, and risk or action suggestions.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
