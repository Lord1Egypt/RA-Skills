## Description: <br>
Crypto Radar helps users check cryptocurrency prices, market capitalization, trading volume, and related market signals using public market data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve public cryptocurrency quotes and summarize market context for BTC, ETH, SOL, BNB, XRP, DOGE, ADA, and related assets. The output is informational market data and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance, CoinGecko, and Binance to retrieve public market data. <br>
Mitigation: Use it only in environments where outbound requests to those public finance APIs are acceptable. <br>
Risk: Market data and interpretation can be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational only and review them before making trading or investment decisions. <br>


## Reference(s): <br>
- [Crypto Radar on ClawHub](https://clawhub.ai/gold3bear/crypto-radar) <br>
- [Yahoo Finance chart endpoint](https://query2.finance.yahoo.com/v8/finance/chart/BTC-USD?interval=1d&range=1d) <br>
- [CoinGecko markets endpoint](https://api.coingecko.com/api/v3/coins/markets) <br>
- [Binance 24hr ticker endpoint](https://api.binance.com/api/v3/ticker/24hr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown summary with market data and concise interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market data APIs; outputs should be reviewed before financial decisions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
