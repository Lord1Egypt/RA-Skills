## Description: <br>
Query real-time and historical cryptocurrency market data via CoinGecko through AIsa, including prices, coin details, historical charts, OHLC candles, token prices by contract address, market-cap rankings, exchange data, categories, trending searches, and crypto news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users can use this skill for read-only cryptocurrency market research, token lookup, price tracking, market-cap screening, and exchange or category analysis through AIsa CoinGecko endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends cryptocurrency market-data queries, including contract addresses or exchange IDs, to AIsa using an API key. <br>
Mitigation: Use an appropriate AIsa API key, avoid including unnecessary sensitive context in queries, and install only where sending these queries to AIsa is acceptable. <br>
Risk: The skill is read-only market data and is not intended for trading actions, wallet balances, transfers, gas traces, equities, dividends, or traditional finance analysis. <br>
Mitigation: Use it only for crypto pricing and research workflows, and route trading, wallet, or non-crypto finance requests to a suitable dedicated tool. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/crypto-market-data-aisa) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference) <br>
- [AIsa CoinGecko Simple Price](https://aisa.one/docs/api-reference/coingecko/simple-price) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; bundled CLI commands print JSON market-data payloads to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; outputs are read-only market-data responses from AIsa CoinGecko endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
