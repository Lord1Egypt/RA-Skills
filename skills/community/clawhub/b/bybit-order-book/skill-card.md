## Description:

Download, process, and backtest ByBit derivatives historical order book data using Selenium-assisted downloads, order book snapshot processing, and built-in trading strategy backtests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidm413](https://clawhub.ai/user/davidm413)

### License/Terms of Use:


## Use Case:

Developers and quantitative trading researchers use this skill to download ByBit order book snapshots, process them into backtest-ready datasets, and compare order-book-based trading strategies. The skill is intended for historical data preparation and performance reporting, not live trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation against a Cloudflare-protected ByBit page.

Mitigation: Review whether this automation is acceptable for the intended use case, prefer manual download or an official source when available, and run the downloader only in an isolated environment.

Risk: The installation guidance uses broad Python package installation with --break-system-packages.

Mitigation: Install dependencies in an isolated virtual environment or disposable container, avoid running as root, and restrict the skill to dedicated data and report directories.

Risk: Historical backtest reports can be mistaken for live trading advice or performance guarantees.

Mitigation: Treat generated results as historical analysis only and require human review before using any strategy output for financial decisions.

## Reference(s):

- [ByBit derivatives historical data](https://www.bybit.com/derivatives/en/history-data)
- [ByBit public trading data endpoint](https://public.bybit.com/trading/{SYMBOL}/{SYMBOL}{YYYY-MM-DD}.csv.gz)
- [ByBit order book data reference](artifact/bybit_data_format.md)
- [Strategy reference](artifact/strategies.md)
- [ClawHub skill page](https://clawhub.ai/davidm413/skills/bybit-order-book)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts can produce ZIP files, Parquet datasets, JSON reports, and Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backtest outputs include strategy comparison metrics, equity curves, PnL, Sharpe ratio, win rate, max drawdown, and related performance statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
