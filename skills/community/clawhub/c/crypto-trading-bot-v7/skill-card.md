## Description:

Helps agents draft crypto trading bot and backtesting workflows for TradingView signals, Python/CCXT exchange integrations, arbitrage concepts, stop-loss and take-profit logic, risk controls, and V7 multi-strategy frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kriouerlia](https://clawhub.ai/user/kriouerlia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate or adapt crypto trading bot code, backtest routines, strategy modules, and configuration guidance for TradingView, exchange APIs, and multi-timeframe V7 strategies. Treat trading outputs as proposals that require review before paper trading or live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated exchange integration code or webhook automation could place real trades and cause financial loss.

Mitigation: Test in sandbox or paper-trading mode first, require explicit confirmation before live orders, and use API keys without withdrawal permission.

Risk: Backtest results and strategy parameters may not generalize to live markets.

Mitigation: Validate assumptions with fresh data, account for fees, slippage, and funding, and enforce position sizing, stop losses, daily loss limits, and volatility filters.

Risk: API credentials may be exposed or over-permissioned during exchange integration.

Mitigation: Store secrets outside prompts and source files, rotate keys regularly, and grant only the minimum trading permissions needed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/kriouerlia/skills/crypto-trading-bot-v7)
- [Binance Public Data](https://data.binance.vision)
- [V7 Strategy README](artifact/scripts/v7_strategy/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy code, backtest summaries, exchange integration steps, and risk-management guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
