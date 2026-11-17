## Description:

加密货币投资研究 - 当用户询问加密货币价格、行情、趋势、新闻时触发

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgx2010](https://clawhub.ai/user/wgx2010)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up cryptocurrency prices, market capitalization, 24-hour movement, and coin search results through CoinGecko. It supports lightweight market-data research rather than complete investment advice or news analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cryptocurrency lookup queries are sent to CoinGecko.

Mitigation: Use the skill only when sharing the queried coin or search term with CoinGecko is acceptable.

Risk: Users may treat market-data lookup output as complete investment research or advice.

Mitigation: Present results as price and market data, and direct users to independently verify information before making financial decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wgx2010/skills/crypto-research-wgx)
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price)
- [CoinGecko coins markets endpoint](https://api.coingecko.com/api/v3/coins/markets)
- [CoinGecko search endpoint](https://api.coingecko.com/api/v3/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON or formatted terminal output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries CoinGecko endpoints; no API key required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
