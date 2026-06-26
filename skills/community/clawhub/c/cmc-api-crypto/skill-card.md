## Description: <br>
API reference for CoinMarketCap cryptocurrency endpoints including quotes, listings, OHLCV, trending, and categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to choose CoinMarketCap cryptocurrency API endpoints, understand required parameters and response shapes, and draft API calls for price data, listings, metadata, OHLCV history, trending assets, market pairs, and categories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated API examples may include placeholders for CoinMarketCap credentials or commands that contact provider endpoints. <br>
Mitigation: Review generated curl commands before execution and provide API keys through environment variables or a secret store instead of prompts or logs. <br>
Risk: CoinMarketCap API calls may consume plan credits or hit subscription-specific restrictions. <br>
Mitigation: Confirm the endpoint, parameters, and plan limits before running requests, especially historical or high-volume queries. <br>


## Reference(s): <br>
- [CoinMarketCap Skill Source](https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap) <br>
- [Categories API Reference](references/categories.md) <br>
- [Info API Reference](references/info.md) <br>
- [Listings API Reference](references/listings.md) <br>
- [Map API Reference](references/map.md) <br>
- [Market Pairs API Reference](references/market-pairs.md) <br>
- [OHLCV API Reference](references/ohlcv.md) <br>
- [Price Performance API Reference](references/price-performance.md) <br>
- [Quotes API Reference](references/quotes.md) <br>
- [Trending API Reference](references/trending.md) <br>
- [Use Cases](references/use-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API endpoint descriptions, parameter tables, JSON examples, and curl command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CoinMarketCap API request examples that require the user's own API key and may consume provider credits.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
