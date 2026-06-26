## Description: <br>
CN Stock Analyst generates stock analysis reports for A-share, Hong Kong, and U.S. equities by fetching public market data, interpreting technical indicators, and summarizing fundamentals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce structured stock-analysis reports for Chinese A-shares, Hong Kong stocks, U.S. stocks, indexes, and ETFs. It is intended for market research workflows that need public price data, technical-indicator interpretation, fundamental-analysis summaries, and explicit risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces ratings, target prices, stop-loss suggestions, and other investment-oriented guidance that may be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis only, ask the agent to confirm ambiguous finance questions before using the skill, and do not rely on its conclusions as investment advice. <br>
Risk: The skill fetches public market data from third-party finance sites that may be delayed, incomplete, blocked, or inconsistent across sources. <br>
Mitigation: Cross-check important figures against authoritative market data, note missing data in the report, and prefer qualitative analysis when source data is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanlee-gemini/cn-stock-analyst) <br>
- [Stock analysis report template](references/report-template.md) <br>
- [Eastmoney quote example](https://quote.eastmoney.com/SH600519.html) <br>
- [Yahoo Finance chart API example](https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=3mo) <br>
- [Xueqiu quote example](https://xueqiu.com/S/SH600519) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown stock analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes data-source attribution, market snapshot tables, technical and fundamental analysis, a rating, key prices, and risk disclosures when data is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
