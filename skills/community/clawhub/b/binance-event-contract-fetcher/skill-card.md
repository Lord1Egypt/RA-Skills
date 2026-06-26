## Description: <br>
Fetches Binance BTCUSDT and ETHUSDT Event Contract market data, including K-lines, liquidity, spot index prices, and contract rule data for downstream agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acwxpunh](https://clawhub.ai/user/acwxpunh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to collect Binance public BTC/ETH market data on a recurring schedule for strategy signal calculation, liquidity checks, and risk-control workflows. It is intended for public market-data retrieval only, not trading authority or private account access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for continuous background polling of Binance public market data. <br>
Mitigation: Confirm how the agent starts, stops, and disables the recurring task before deployment. <br>
Risk: The artifact uses strong accuracy wording for market data. <br>
Mitigation: Treat outputs as market-data retrieval results, not as a trading guarantee or investment advice. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/acwxpunh/binance-event-contract-fetcher) <br>
- [Binance API base endpoint](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured market-data examples and shell installation command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs describe public Binance BTCUSDT and ETHUSDT data retrieval, verification, retry, cache fallback, and alert behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
