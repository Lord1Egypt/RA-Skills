## Description: <br>
Use when writing a strategy that captures short-squeeze setups on Hyperliquid perps by going long when funding APR is deeply negative and price has started rising, then exiting on funding normalization or a time stop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy builders use this skill to draft and tune a Freqtrade strategy for Hyperliquid perpetual futures short-squeeze setups. It provides entry, exit, configuration, backtest framing, and parameter guidance for negative-funding rallies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included futures and cross-margin strategy configuration can lose real money if used live without validation. <br>
Mitigation: Review the generated strategy and configuration, run backtests and paper trading, and size any live deployment conservatively. <br>
Risk: Long-only squeeze setups can perform poorly in structural downtrends, as shown by the included negative BTC backtest window. <br>
Mitigation: Add a higher-timeframe trend filter or multi-pair scan before relying on the strategy in live markets. <br>
Risk: The skill provides trading-strategy guidance but does not guarantee profitable execution. <br>
Mitigation: Treat outputs as strategy drafts for expert review rather than financial advice or an automated trading decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/funding-squeeze) <br>
- [Publisher profile](https://clawhub.ai/user/superior-ai) <br>
- [Freqtrade DataProvider documentation](https://www.freqtrade.io/en/stable/strategy-customization/) <br>
- [Alpha scan improvement plan](https://github.com/Superior-Trade/superior-turborepo/blob/main/docs/alpha-scan-improvement-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces strategy-writing guidance for an agent; it does not execute trades by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
