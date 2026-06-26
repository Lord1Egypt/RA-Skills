## Description: <br>
A股数据分析 (AkShare) helps agents retrieve and summarize A-share, Hong Kong, and U.S. stock quotes, historical prices, financial data, sector data, capital-flow data, IPO information, margin-trading data, and limit-up/limit-down market data through AkShare. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[awsl1414](https://clawhub.ai/user/awsl1414) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to guide AkShare-based market-data queries for research workflows covering quotes, historical K-lines, financial statements, sectors, capital flows, IPOs, and margin-trading data. The skill is informational and should not be used as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and uses the AkShare Python dependency and may make network requests to third-party market-data sources. <br>
Mitigation: Install it only in environments where that dependency and outbound market-data requests are approved. <br>
Risk: Returned financial data may be incomplete, delayed, unavailable, or unsuitable for trading decisions. <br>
Mitigation: Treat outputs as informational research material and verify important figures against authoritative market-data sources. <br>
Risk: Some full-market or real-time AkShare calls can be slow or return large datasets. <br>
Mitigation: Prefer single-symbol interfaces for stock-specific questions and limit large result sets with slicing or head-style previews. <br>


## Reference(s): <br>
- [AkShare stock API reference](artifact/references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/awsl1414/akshare-a-stock) <br>
- [Third-party publisher profile](https://clawhub.ai/user/awsl1414) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; the bundled CLI prints JSON records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on network access to third-party market-data sources and AkShare response availability.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
