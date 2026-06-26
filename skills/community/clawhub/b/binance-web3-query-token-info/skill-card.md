## Description: <br>
Binance Query Token Info gives agents read-only token search, metadata, market data, and OHLCV candlestick lookups by keyword, symbol, or contract address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer token research and market questions across Ethereum, BSC, Base, and Solana, including token discovery, metadata, live market data, holder and liquidity context, and chart candles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token symbols, chain IDs, contract addresses, intervals, and kline time-window parameters may be sent to Binance Web3 endpoints and a separate kline data host. <br>
Mitigation: Avoid using the skill for private wallet analysis or sensitive trading research unless those external requests are acceptable. <br>
Risk: Market data responses may require careful parsing because numeric market values can be string-encoded and kline results are returned as indexed candle arrays. <br>
Mitigation: Convert numeric strings before arithmetic and parse kline candles by the documented array indexes. <br>


## Reference(s): <br>
- [CLI reference](references/cli.md) <br>
- [ClawHub skill page](https://clawhub.ai/binance-skills-hub/binance-web3-query-token-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [CLI invocation guidance and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only token lookup; numeric market values may be string-encoded, and kline returns a 2D candle array.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
