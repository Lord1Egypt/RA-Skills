## Description:

A股和港股股票数据分析工具，优先使用Tushare数据，Tushare不可用时自动回退到AKShare获取行情、财务指标，支持基本面分析和技术分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh40](https://clawhub.ai/user/zh40)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve A-share and Hong Kong stock data, inspect company basics and financial indicators, and calculate common technical indicators with Tushare preferred and AKShare fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts contact Tushare or AKShare and may use a TUSHARE_TOKEN environment variable.

Mitigation: Install and run the skill in an isolated Python environment, set TUSHARE_TOKEN only when comfortable using Tushare, and expect outbound market-data requests.

Risk: Dependency version ranges may resolve to package versions that differ from those reviewed at release time.

Mitigation: Prefer a reviewed, pinned requirements file or lock file before production use.

Risk: Stock data, financial metrics, and technical indicators can be unavailable, delayed, or incomplete from either data source.

Mitigation: Validate important outputs against trusted market-data sources before relying on them for financial decisions.

## Reference(s):

- [Tushare API 常用接口](references/tushare-api.md)
- [Tushare](https://tushare.pro/)
- [ClawHub skill page](https://clawhub.ai/zh40/skills/a-h-stock-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, terminal tables, and optional CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TUSHARE_TOKEN when configured; otherwise falls back to AKShare where available.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
