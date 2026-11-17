## Description:

Query token prices, market data, K-line charts, and smart money trading signals via Binance Web3 APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torchesfrms](https://clawhub.ai/user/torchesfrms)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search tokens, inspect market data, retrieve candlestick data, and review smart money trading signals on supported Web3 networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs such as token symbols, contract addresses, chain IDs, and wallet addresses are sent to Binance Web3 or the K-line API host.

Mitigation: Use the skill only when sharing those values is intended, and avoid submitting sensitive user-associated wallet addresses without consent.

Risk: Market and smart money results come from unauthenticated third-party API data.

Mitigation: Treat responses as informational signals and verify important trading or compliance decisions with authoritative sources.

Risk: The security review notes documentation and validation gaps.

Mitigation: Review scripts before deployment and add input validation or clearer operating guidance before broad use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/torchesfrms/skills/binance-web3)
- [Publisher Profile](https://clawhub.ai/user/torchesfrms)
- [Binance Web3 Token Search API](https://web3.binance.com/bapi/defi/v5/public/wallet-direct/buw/wallet/market/token/search)
- [Binance Web3 Token Dynamic Info API](https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info)
- [Binance Web3 Smart Money Signal API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money)
- [K-Line Candles API](https://dquery.sintral.io/u-kline/v1/k-line/candles)

## Skill Output:

**Output Type(s):** [shell commands, json, guidance]

**Output Format:** [Markdown guidance with shell commands that return JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is documented; scripts send supplied token symbols, contract addresses, chain IDs, and wallet addresses to external API hosts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
