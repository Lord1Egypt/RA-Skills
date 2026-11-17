## Description:

Query token details by keyword, contract address, or chain, including metadata, social links, real-time market data, and K-Line candlestick charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viktor-huang](https://clawhub.ai/user/viktor-huang)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to search tokens across BSC, Base, and Solana, retrieve project metadata and market metrics, and request candlestick data for token research and charting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token names, contract addresses, chain choices, and chart parameters are queried against Binance Web3 and the K-Line provider.

Mitigation: Avoid wallet-private or strategy-sensitive searches unless the user accepts that those lookup terms may leave the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viktor-huang/skills/binance-query-token)
- [Binance Web3 token search endpoint](https://web3.binance.com/bapi/defi/v5/public/wallet-direct/buw/wallet/market/token/search)
- [Binance Web3 token metadata endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/meta/info)
- [Binance Web3 token dynamic data endpoint](https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info)
- [K-Line candlestick endpoint](https://dquery.sintral.io/u-kline/v1/k-line/candles)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON]

**Output Format:** [Markdown with API endpoint details, curl examples, and JSON response schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public token lookup parameters such as keyword, contract address, chain ID, platform, interval, limit, and timestamp range.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
