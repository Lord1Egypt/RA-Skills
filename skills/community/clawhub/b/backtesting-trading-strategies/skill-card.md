## Description:

Backtest crypto and traditional trading strategies against historical data with performance metrics, equity curves, and parameter optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:

MIT

## Use Case:

Developers, quantitative analysts, and traders use this skill to fetch historical market data, simulate trading strategies, compare performance and risk metrics, and tune parameters before making decisions outside the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts market-data providers and saves cached data plus generated reports locally.

Mitigation: Install it in a dedicated virtual environment, consider pinning dependencies, and review configured data and report directories before execution.

Risk: Backtest outputs can be mistaken for trading instructions or overstate real-world performance.

Mitigation: Treat results as analysis only, account for assumptions such as slippage and commissions, and review any trading decision outside the agent.

## Reference(s):

- [Error Handling Reference](references/errors.md)
- [Backtesting Examples](references/examples.md)
- [Implementation Guide](references/implementation.md)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [TA-Lib](https://ta-lib.org/)
- [QuantStats](https://github.com/ranaroussi/quantstats)
- [CoinGecko Market Chart API](https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus locally saved text, CSV, and PNG report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads market data, caches data locally, and writes generated analysis reports under the configured output directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
