## Description: <br>
Guides agents in fetching, organizing, and validating A-share market data including stock basics, trading calendars, prices, financials, trading status, sectors, capital flows, announcements, and professional market-data source guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alanwu2024](https://clawhub.ai/user/alanwu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to prepare A-share market datasets, compare market-data sources, document field definitions, and surface reliability limits before using data for research, backtesting, or market review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data may come from providers with different authority levels, licensing terms, delays, or field definitions. <br>
Mitigation: Confirm which providers the agent will contact, use paid or licensed feeds only with permission, and report source, timestamp, units, and field definitions with the output. <br>
Risk: Financial data can be incomplete, conflicting, delayed, or unsuitable for trading, investment, or compliance decisions without independent checks. <br>
Mitigation: Cross-check key fields against authoritative or commercial sources and clearly mark conflicts, missing data, and unavailable official data before relying on results. <br>


## Reference(s): <br>
- [AKShare stock data documentation](https://akshare.akfamily.xyz/data/stock/stock.html) <br>
- [AKShare data dictionary](https://akshare.akfamily.xyz/data/index.html) <br>
- [CNINFO](http://www.cninfo.com.cn/) <br>
- [Shenzhen Stock Exchange disclosure notices](https://www.szse.cn/marketServices/deal/disclosure/notice/index.html) <br>
- [Shanghai Stock Exchange market data products](https://english.sse.com.cn/markets/dataservice/products/) <br>
- [Choice Quant API manual](https://quantapi.eastmoney.com/Manual?from=web) <br>
- [Reference documentation for Ashare Market Data Fetcher](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with tables and optional code or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes data-source, timestamp, field-definition, and limitation metadata when market data is reported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
