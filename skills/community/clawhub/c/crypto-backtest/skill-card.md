## Description:

Crypto Backtest helps agents run crypto futures backtests with built-in EMA, RSI, MACD, and Bollinger Band strategies, fetch OHLCV data from ccxt-supported exchanges, compare parameter sweeps, calculate win rate, PnL, and drawdown, and export results to JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyztj](https://clawhub.ai/user/sunnyztj)

### License/Terms of Use:


## Use Case:

Developers and quantitative trading practitioners use this skill to run crypto futures strategy backtests, compare parameter combinations, and export metrics for analysis or pipeline integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may pull unreviewed package versions.

Mitigation: Install dependencies in a virtual environment and pin reviewed versions of ccxt; remove numpy unless the release actually needs it.

Risk: JSON export can overwrite an existing local file.

Mitigation: Choose output paths deliberately and write results to a dedicated backtest output location.

Risk: Backtest results and historical strategy metrics can be mistaken for reliable future trading performance.

Mitigation: Treat outputs as analytical evidence only, review assumptions, and validate strategies with paper trading before live use.

## Reference(s):

- [Adding Custom Strategies](references/custom_strategy.md)
- [Strategy Notes](references/strategy_notes.md)
- [Crypto Backtest on ClawHub](https://clawhub.ai/sunnyztj/skills/crypto-backtest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; JSON backtest result files when the bundled scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backtest outputs include trades, win rate, PnL, drawdown, profit factor, balances, strategy parameters, and optional sweep rankings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
