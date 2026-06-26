## Description: <br>
Crypto futures backtesting engine with built-in EMA, RSI, MACD, and Bollinger Band strategies that fetches OHLCV data from ccxt-supported exchanges, runs multi-strategy sweeps, calculates win rate, PnL, and drawdown, and exports results to JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunnyztj](https://clawhub.ai/user/Sunnyztj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, quantitative trading users, and agent operators use this skill to backtest crypto futures strategies, compare parameter combinations, and generate machine-readable simulation results before considering live trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data requests are sent to the selected exchange. <br>
Mitigation: Review the exchange, symbol, timeframe, and network environment before running the scripts. <br>
Risk: Result output paths can overwrite existing local files. <br>
Mitigation: Choose output paths intentionally and inspect the destination before enabling JSON output. <br>
Risk: Backtest results are simulations and may not predict live trading performance. <br>
Mitigation: Treat results as analysis only, validate assumptions independently, and use paper trading before any live workflow. <br>
Risk: The scripts depend on third-party Python packages. <br>
Mitigation: Install dependencies in a virtual environment and verify package sources before execution. <br>


## Reference(s): <br>
- [Adding Custom Strategies](references/custom_strategy.md) <br>
- [Strategy Notes](references/strategy_notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and optional JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backtest and sweep scripts can print metrics to the terminal and save JSON results to caller-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
