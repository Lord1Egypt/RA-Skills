## Description:

Backtests crypto dollar-cost averaging against a same-capital lump-sum strategy using CoinGecko historical daily prices and reports invested capital, ending value, percent return, and the better performer for the selected window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto traders, investors, and developers use this skill to compare weekly DCA against a lump-sum entry strategy before allocating capital. It helps evaluate historical outcomes for CoinGecko-listed coins over a selected lookback window up to 365 days.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CoinGecko requests may reveal queried coin IDs and lookback windows to a public third-party API.

Mitigation: Use the skill only when that public API disclosure is acceptable, and avoid entering sensitive strategy details as coin identifiers or parameters.

Risk: Historical return comparisons can be mistaken for financial advice or predictive signals.

Mitigation: Treat output as historical analysis only; review assumptions before acting and do not use it as a recommendation to buy, sell, or hold crypto assets.

Risk: The backtest omits fees, slippage, exchange spreads, volatility-adjusted returns, and maximum drawdown.

Mitigation: Supplement the output with separate cost, liquidity, and risk analysis before using it for allocation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/crypto-dca-backtester)
- [CoinGecko API](https://api.coingecko.com/api/v3)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON backtest results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact CoinGecko's public API for historical prices; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
