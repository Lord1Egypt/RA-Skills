## Description:

Runs a walk-forward Bull Put Spread backtest with and without a FearScore entry signal, returning side-by-side performance metrics, trade ledgers, equity curves, and a plain-language takeaway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate Bull Put Spread parameters on US, Hong Kong, or China tickers and compare a FearScore-filtered strategy against a no-signal control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ticker, date range, and strategy parameters to the AlphaGBM service and may spend an option-analysis credit for an uncached call.

Mitigation: Use it only when sharing those inputs with AlphaGBM and spending the credit is intended; confirm ticker and strategy parameters before the request.

Risk: Backtest results rely on reconstructed FearScore and historical-volatility option pricing proxies, so results may differ from live option-chain behavior.

Mitigation: Treat the output as research support, compare the signal and control results, and review the trade ledger and drawdown metrics before using results in trading decisions.

## Reference(s):

- [AlphaGBM](https://alphagbm.com)
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-bps-backtest)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON results with text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns separate with-signal and no-signal backtest passes, including KPIs, trade ledger, equity curve, P&L histogram, exit reasons, and bilingual summary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
