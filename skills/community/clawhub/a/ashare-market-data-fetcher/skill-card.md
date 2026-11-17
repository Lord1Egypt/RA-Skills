## Description:

Provides workflows for collecting and validating A-share market data, including stock basics, trading calendars, historical and intraday prices, adjustment data, suspensions, financial statements, market themes, capital flows, announcements, and professional data-source guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanwu2024](https://clawhub.ai/user/alanwu2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to collect, explain, and validate A-share market data for research, review, backtesting preparation, and market-data quality checks. It emphasizes source hierarchy, field definitions, timestamps, and cross-source validation before drawing conclusions from the data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data may be unsuitable for trading or investment decisions if source permissions, latency, and field definitions are not independently verified.

Mitigation: Verify data-source permissions, latency, field definitions, and usage rights before relying on outputs; use official or licensed providers for Level-2, tick, and trading-critical workflows.

Risk: Free, open-source, and public web data can diverge from official or licensed market-data feeds.

Mitigation: Label every source, retrieval time, adjustment basis, unit, and unresolved conflict, and cross-check key fields against official disclosures or licensed market-data sources.

## Reference(s):

- [AKShare Stock Data Documentation](https://akshare.akfamily.xyz/data/stock/stock.html)
- [AKShare Data Dictionary](https://akshare.akfamily.xyz/data/index.html)
- [CNINFO](http://www.cninfo.com.cn/)
- [Shenzhen Stock Exchange Information Disclosure Notices](https://www.szse.cn/marketServices/deal/disclosure/notice/index.html)
- [Shanghai Stock Exchange Market Data Products](https://english.sse.com.cn/markets/dataservice/products/)
- [Choice Quant API Manual](https://quantapi.eastmoney.com/Manual?from=web)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with structured tables, source and field metadata, validation notes, and optional code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state data source, retrieval time, field definitions, adjustment basis, units, and unresolved conflicts or limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
