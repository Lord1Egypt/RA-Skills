## Description: <br>
Query real-time cryptocurrency prices, market data, and trends across major exchanges (Binance, Coinbase, Kraken). Supports BTC, ETH, and major altcoins with price, 24h change, market cap, and volume data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can ask an agent to fetch and format public cryptocurrency quotes, market-cap data, volume, and short-term price movement from public exchange APIs for price checks, portfolio tracking, market overviews, and alert monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live cryptocurrency market output can be mistaken for financial advice or connected to trading actions without review. <br>
Mitigation: Use the output as informational market data only, and require separate human or system review before any trading decision or automated action. <br>
Risk: Third-party public API limits, outages, or source differences can produce missing, delayed, or inconsistent quotes. <br>
Mitigation: Handle rate limits and API errors, compare sources where accuracy matters, and avoid treating a single response as authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/crypto-market-quotes) <br>
- [Binance 24hr ticker endpoint](https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT) <br>
- [CoinGecko markets endpoint](https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1&sparkline=false) <br>
- [Kraken ticker endpoint](https://api.kraken.com/0/public/Ticker?pair=XBTUSD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands, formatted quote summaries, and market tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public cryptocurrency market-data APIs through curl; no API key is required for the documented basic queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
