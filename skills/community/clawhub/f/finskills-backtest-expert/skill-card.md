## Description: <br>
Design, execute, and evaluate quantitative trading strategies using historical price data and Fama-French factor attribution via the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, quantitative analysts, and trading strategy researchers use this skill to turn strategy hypotheses into historical backtest reports with performance metrics, benchmark comparison, factor attribution, walk-forward validation, and stress tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive FINSKILLS_API_KEY credential. <br>
Mitigation: Store the key as a secret, avoid pasting it into chats or public files, and confirm plan or billing limits before use. <br>
Risk: Generated backtests can be mistaken for investment advice or live-trading recommendations. <br>
Mitigation: Treat the report as analytical support only and have qualified reviewers assess assumptions, risk, and suitability before any financial decision. <br>
Risk: Historical backtests can be affected by survivorship bias, missing slippage, delayed factor data, or overfitting. <br>
Mitigation: Review data assumptions, include realistic costs and slippage where possible, and use walk-forward and out-of-sample checks before relying on results. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/finskills/finskills-backtest-expert) <br>
- [Finskills Backtest Expert homepage](https://github.com/finskills/backtest-expert) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills registration](https://finskills.net/register) <br>
- [Historical OHLCV endpoint](https://finskills.net/v1/stocks/history/{SYMBOL}?period=5y&interval=1d) <br>
- [Fama-French factor endpoint](https://finskills.net/v1/free/market/fama-french) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Structured Markdown backtest report with metrics, attribution, validation, stress-test results, and a strategy verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require FINSKILLS_API_KEY to retrieve Finskills market and factor data; generated backtests should be treated as analysis, not investment advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
