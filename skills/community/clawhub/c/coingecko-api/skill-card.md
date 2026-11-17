## Description:

Use for any crypto market or onchain data request, even if CoinGecko isn't named: coin and token prices, market cap, volume, OHLC and historical charts, supply, categories, top gainers and losers, trending coins, new listings, global market stats; exchanges, tickers, derivatives and funding rates; NFT floor prices; public company and government crypto treasuries; real-world assets (tokenized stocks, commodities, ETFs); crypto news and coin insights; onchain DEX data via GeckoTerminal (pools, trending and new pools, token price by contract address, trades, liquidity events, holders, top traders); wallet balances, holdings or PnL for a wallet address, token transfers and wallet trades. Also use for questions about the CoinGecko API itself: endpoints, plans, API keys, rate limits, errors, WebSocket streams and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coingecko](https://clawhub.ai/user/coingecko)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to retrieve live CoinGecko market and onchain data and answer questions about API endpoints, plans, parameters, and limits using current documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet lookups disclose the queried address to the data provider and may consume API quota.

Mitigation: Only query addresses the user intends to share, and account for plan and rate limits.

Risk: An API key could be exposed if pasted into chat or embedded in commands or files.

Mitigation: Keep API keys in environment variables and send them only to the documented CoinGecko API hosts.

Risk: Global installation affects all agents, and an unpinned installer or repository revision can change over time.

Mitigation: Review installation scope and pin installer versions and repository commits.

## Reference(s):

- [CoinGecko Agent Skill documentation](https://docs.coingecko.com/ai-integration/agent-skill)
- [CoinGecko API documentation](https://docs.coingecko.com)
- [CoinGecko API endpoint overview (Paid)](https://docs.coingecko.com/reference/endpoint-overview.md)
- [CoinGecko API endpoint overview (Demo and Keyless)](https://docs.coingecko.com/demo/reference/endpoint-overview.md)
- [CoinGecko API errors and rate limits](https://docs.coingecko.com/docs/errors-and-rate-limits.md)
- [CoinGecko API pricing](https://www.coingecko.com/en/api/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, API query results, Shell commands, Configuration guidance]

**Output Format:** [Text and Markdown, including API results, explanations, and command or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data should come from live API calls; API access and limits depend on the selected plan.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
