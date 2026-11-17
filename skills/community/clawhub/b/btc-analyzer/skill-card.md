## Description:

Fetches live BTCUSDT 15-minute candles from Binance's public API and analyzes market direction as UP, DOWN, or SKIP using EMA20 and RSI14.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newbienodes](https://clawhub.ai/user/newbienodes)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve live BTC market data, run the analyzer, and present BTCUSDT direction, confidence, price, and indicator context. It is for market analysis support and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces BTC trading direction signals that could be mistaken for financial advice.

Mitigation: Present results as market-analysis support only, include confidence and reasoning, and avoid recommending trades, position sizing, or financial decisions.

Risk: The analyzer is executed from a mutable global install path and the reviewed artifact did not include the Python script.

Mitigation: Install only from a trusted source, verify the referenced analyzer script contents and permissions before execution, and run it with least privileges.

Risk: Live Binance API calls can fail or return unavailable market data.

Mitigation: Show the actual script error or SKIP result and do not fabricate prices, indicators, timestamps, or direction signals.

## Reference(s):

- [ClawHub BTC Analyzer Skill Page](https://clawhub.ai/newbienodes/skills/btc-analyzer)
- [Publisher Profile: newbienodes](https://clawhub.ai/user/newbienodes)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Strict JSON from the analyzer followed by concise human-facing text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes UP, DOWN, or SKIP decision, confidence, reason, last close, EMA20, RSI14, and timestamp when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
