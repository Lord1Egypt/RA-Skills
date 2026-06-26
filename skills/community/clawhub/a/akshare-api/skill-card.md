## Description: <br>
Use this skill when the user wants Chinese stock market data or analysis, including A-share行情、上证/深证/创业板指数、个股K线、涨跌停统计、资金流向、基本面、板块表现、港股美股行情、基金可转债、财经新闻和研报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyriswu](https://clawhub.ai/user/kyriswu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and summarize A-share, Hong Kong, and U.S. stock market data, including quotes, K-line data, fund flows, fundamentals, sector performance, financial news, and research reports in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-query text is sent to the hosted service at akshare.devtool.uk, and the security evidence notes a reachable local portfolio-management path. <br>
Mitigation: Use this skill for non-sensitive market-data questions, avoid holdings or portfolio-management prompts, and review execution before using it in workflows that may include private portfolio details. <br>


## Reference(s): <br>
- [AkShare stock data documentation](https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt) <br>
- [ClawHub skill page](https://clawhub.ai/kyriswu/akshare-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Chinese text or Markdown summaries derived from local command output and hosted API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise tables, key market figures, error messages, and one follow-up question when the stock symbol or market is ambiguous.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
