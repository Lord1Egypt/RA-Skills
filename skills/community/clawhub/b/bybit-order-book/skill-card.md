## Description: <br>
Downloads, processes, and backtests ByBit derivatives historical order book data, including top-depth filtering, built-in order-book trading strategies, and performance report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidm413](https://clawhub.ai/user/davidm413) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative trading researchers use this skill to acquire ByBit order book snapshots, convert them into analysis-ready Parquet data, run built-in order-book strategies, and compare backtest performance metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated ByBit downloads may bypass Cloudflare protection or violate site terms for some use cases. <br>
Mitigation: Confirm automated access is permitted, respect rate limits, and prefer manual or officially supported data access when appropriate. <br>
Risk: Installing dependencies with --break-system-packages can modify the system Python environment. <br>
Mitigation: Install and run the skill in an isolated virtual environment or container. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidm413/bybit-order-book) <br>
- [ByBit derivatives history data](https://www.bybit.com/derivatives/en/history-data) <br>
- [ByBit Order Book Data Reference](bybit_data_format.md) <br>
- [Strategy Reference](strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated JSON or Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backtest reports include PnL, Sharpe ratio, win rate, drawdowns, equity curves, and strategy comparisons.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
