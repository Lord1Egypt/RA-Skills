## Description: <br>
Monitors cryptocurrency funding-rate and basis-arbitrage signals for ETH perpetual contracts across exchanges such as Gate.io, Binance, and OKX, then returns buy, watch, or risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcy891](https://clawhub.ai/user/pcy891) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto analysts use this skill to request arbitrage-monitoring reports for ETH funding rates, estimated annualized yield, exchange comparisons, and risk signals. The output is research-oriented market analysis and does not execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-signal reports may be acted on as financial advice or with stale market data. <br>
Mitigation: Treat outputs as research only; verify live exchange data, fees, position sizing, and account risk before taking any action. <br>
Risk: The skill could be invoked for general crypto discussion where arbitrage monitoring is not intended. <br>
Mitigation: Use it only for explicit funding-rate, arbitrage, or exchange-rate monitoring requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcy891/crypto-arbitrage-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with exchange comparison tables, ratings, strategy notes, and risk reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses current market-search summaries when available; does not request credentials, persist data, or execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
