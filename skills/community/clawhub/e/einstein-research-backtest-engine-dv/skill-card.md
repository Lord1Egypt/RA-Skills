## Description:

Programmatic backtesting framework for trading strategies that runs backtests with historical price data (yfinance or CSV), supports momentum/mean-reversion/factor/signal-based strategies, walk-forward optimization, out-of-sample testing, transaction cost modeling, regime-aware splits, and full performance metrics (Sharpe, Sortino, Calmar, max drawdown, CAGR, win rate, profit factor).

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to run historical trading-strategy backtests, compare built-in or custom strategies, and review performance metrics before further research. It is a testing and reporting tool, not a live trading or broker-execution system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom strategy files are Python programs and can execute local code.

Mitigation: Use built-in strategies or trusted, reviewed strategy files, run the tool in an isolated virtual environment, and avoid exposing secrets or sensitive workspace files.

Risk: Backtest reports can be mistaken for live trading advice.

Mitigation: Present results as historical testing output only and keep the skill's stated limitations visible: it does not provide live trade recommendations, connect to brokers, or guarantee profitable results.

## Reference(s):

- [Backtest Pitfalls & How the Engine Avoids Them](artifact/references/backtest_pitfalls.md)
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-backtest-engine-dv)
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Natural language with shell commands; generated backtest reports are JSON and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files to the selected output directory when the engine script is executed]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
