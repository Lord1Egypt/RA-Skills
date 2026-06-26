## Description: <br>
加密货币投资研究 - 当用户询问加密货币价格、行情、趋势、新闻时触发 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgx2010](https://clawhub.ai/user/wgx2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research cryptocurrency prices, market rankings, short-term market movement, and related market prompts. The bundled scripts query CoinGecko for prices, 24-hour change, market capitalization, top coins, and coin search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cryptocurrency lookup terms are sent to CoinGecko. <br>
Mitigation: Use the skill only when sharing those lookup terms with CoinGecko is acceptable. <br>
Risk: Market data may be mistaken for financial advice or used for trading decisions. <br>
Mitigation: Treat outputs as informational market data only and do not use the skill for trades, wallets, private keys, or account-management tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wgx2010/crypto-research-wgx) <br>
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price) <br>
- [CoinGecko markets endpoint](https://api.coingecko.com/api/v3/coins/markets) <br>
- [CoinGecko search endpoint](https://api.coingecko.com/api/v3/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON or formatted text returned by shell/Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CoinGecko market-data lookups; no API key is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
