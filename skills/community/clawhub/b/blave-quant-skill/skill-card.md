## Description: <br>
Blave Quant Skill helps agents retrieve Blave market alpha data, Taiwan and futures market data, and prepare guarded trading workflows across major crypto exchanges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blave-wei](https://clawhub.ai/user/blave-wei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through market-data retrieval, screening, backtesting support, and exchange trading tasks. State-changing exchange actions are framed as proposals requiring explicit user confirmation before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent using live trading credentials across exchanges. <br>
Mitigation: Use least-privilege, exchange-specific API keys, disable withdrawals unless required, enable IP allowlisting, and review each state-changing action before replying CONFIRM. <br>
Risk: Marketplace or shared strategy code may be downloaded and run locally. <br>
Mitigation: Review strategy code before execution and run it only in an isolated environment with no ambient secrets. <br>
Risk: Market analysis and trading workflows can produce financial losses if treated as advice or automated without supervision. <br>
Mitigation: Treat outputs as decision support, keep the skill confirmation gate in place, and independently verify trade parameters and risk exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blave-wei/blave-quant-skill) <br>
- [Blave homepage](https://blave.org) <br>
- [Blave API reference](references/blave-api.md) <br>
- [Blave indicator guide](references/blave-indicator-guide.md) <br>
- [Hyperliquid API reference](references/hyperliquid-api.md) <br>
- [TradingView stream reference](references/tradingview-stream.md) <br>
- [TWSE skill guide](references/twse-skill.md) <br>
- [Marketplace reference](references/marketplace.md) <br>
- [BitMart futures guide](references/bitmart-futures-skill.md) <br>
- [OKX guide](references/okx-skill.md) <br>
- [Bybit guide](references/bybit-skill.md) <br>
- [Binance guide](references/binance-skill.md) <br>
- [KuCoin guide](references/kucoin-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, API-call examples, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Blave credentials for market data and optional exchange-specific credentials for trading workflows.] <br>

## Skill Version(s): <br>
1.10.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
