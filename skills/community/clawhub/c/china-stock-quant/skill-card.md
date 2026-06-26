## Description: <br>
A-share quantitative analysis toolkit for fetching China A-share and ETF market data, calculating technical indicators, backtesting grid, moving-average, and Bollinger strategies, and assessing portfolio risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miio-jinglin](https://clawhub.ai/user/miio-jinglin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to prepare A-share and ETF market data, compute common technical indicators, run simple strategy backtests, and summarize risk metrics for China-market quantitative research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals or backtest results may be incorrect, stale, or unsuitable for real capital allocation. <br>
Mitigation: Treat outputs as analysis only and verify financial conclusions independently before acting on them. <br>
Risk: Python dependencies and market-data retrieval behavior may change across environments. <br>
Mitigation: Install dependencies in an isolated Python environment and consider pinning package versions. <br>
Risk: External market-data calls may return empty, delayed, or changed data. <br>
Mitigation: Validate returned dataframes, date ranges, and symbols before using generated indicators or backtest results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/miio-jinglin/china-stock-quant) <br>
- [akshare API Quick Reference](references/api-reference.md) <br>
- [ETF Day-Trading Strategies](references/strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis guidance and reusable Python snippets; bundled scripts can return pandas DataFrames, backtest summaries, risk dictionaries, and signal tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
