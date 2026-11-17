## Description:

BTC contract scanner that uses EMA, MACD, RSI, Bollinger Band, and volume signals across 1H and 4H timeframes, includes backtest data, and outputs LONG, SHORT, or HOLD decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to obtain BTC/USDT contract trend signals and a compact JSON summary of recent backtest metrics. It is intended as trading-signal guidance, not as financial advice or a complete trading system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals and backtest metrics may be incomplete, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as informational signals only, review the assumptions and recent market context, and do not rely on the skill alone for trading decisions.

Risk: External OKX market data or proxy availability can affect signal freshness and reliability.

Mitigation: Confirm the data source, network path, and latest price independently before taking action based on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/skills/btc-contract-scanner-free)

## Skill Output:

**Output Type(s):** [analysis, json, guidance]

**Output Format:** [JSON and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes price, market regime, long and short scores, decision, last backtest date, 7-day win rate, and 7-day PnL.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
