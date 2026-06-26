## Description: <br>
Query token details by keyword, contract address, or chain, including metadata, social links, real-time market data, and K-Line candlestick charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viktor-huang](https://clawhub.ai/user/viktor-huang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search tokens, retrieve token metadata, inspect public market data, and request candlestick chart data across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token queries may reveal private portfolio strategy or unrelated sensitive details. <br>
Mitigation: Limit prompts and API parameters to public token identifiers and avoid including private trading plans or sensitive personal context. <br>
Risk: Public market data can be stale, incomplete, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Verify important prices, liquidity, holder data, and chart outputs against trusted sources before acting on them. <br>
Risk: Publisher and endpoint provenance is limited because no server-resolved GitHub import provenance is available. <br>
Mitigation: Review the publisher profile and referenced endpoints before deploying the skill in a workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/viktor-huang/binance-query-token) <br>
- [Binance Web3 token search endpoint](https://web3.binance.com/bapi/defi/v5/public/wallet-direct/buw/wallet/market/token/search) <br>
- [Binance Web3 token metadata endpoint](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/meta/info) <br>
- [Binance Web3 token dynamic data endpoint](https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info) <br>
- [K-Line candlestick endpoint](https://dquery.sintral.io/u-kline/v1/k-line/candles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with API request examples and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public token metadata, market metrics, holder data, liquidity values, and OHLCV candlestick arrays.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
