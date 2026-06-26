## Description: <br>
Provides agent guidance for using CoinGecko and GeckoTerminal APIs to retrieve live cryptocurrency market, exchange, NFT, DeFi, and on-chain data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coingecko](https://clawhub.ai/user/coingecko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to construct live CoinGecko and GeckoTerminal API requests for crypto prices, market charts, exchanges, NFTs, DeFi metrics, liquidity pools, and related troubleshooting. It helps agents choose the right reference material, check credential and tier constraints, and avoid answering time-sensitive market questions from stale model knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may cause an agent to send requests to CoinGecko domains using a user-provided API key. <br>
Mitigation: Use only a CoinGecko API key the user is comfortable sharing with the agent, and expect outbound requests to CoinGecko and GeckoTerminal API domains. <br>
Risk: Wallet-level analytics, token links, and on-chain token data can be privacy-sensitive or unverified. <br>
Mitigation: Treat on-chain token links and wallet-level analytics as unverified or privacy-sensitive when sharing results. <br>
Risk: Market figures are time-sensitive and stale model knowledge can be misleading. <br>
Mitigation: Rely on successful live API responses for crypto prices, volumes, supply, TVL, exchange rates, and other current market figures. <br>


## Reference(s): <br>
- [CoinGecko API documentation](https://www.coingecko.com/en/api) <br>
- [CoinGecko Skill documentation](https://docs.coingecko.com/docs/skills) <br>
- [ClawHub CoinGecko API skill page](https://clawhub.ai/coingecko/coingecko-api) <br>
- [README](README.md) <br>
- [Core API reference](references/core.md) <br>
- [Common use cases](references/common-use-cases.md) <br>
- [Coins reference](references/coins.md) <br>
- [Coin history reference](references/coin-history.md) <br>
- [Exchanges reference](references/exchanges.md) <br>
- [NFTs reference](references/nfts.md) <br>
- [On-chain pools reference](references/onchain-pools.md) <br>
- [On-chain tokens reference](references/onchain-tokens.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline JSON, URL, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to use live API responses for time-sensitive market data and to surface credential, rate-limit, and API tier constraints before proceeding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
