## Description: <br>
Calls CoinAnk OpenAPI endpoints to retrieve cryptocurrency market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a4205586](https://clawhub.ai/user/a4205586) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to select relevant CoinAnk OpenAPI definitions, validate required parameters, and construct authenticated market-data API calls for crypto analytics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a CoinAnk API key to CoinAnk OpenAPI endpoints. <br>
Mitigation: Use a dedicated CoinAnk key in COINANK_API_KEY and avoid logging commands or headers that expose the key. <br>
Risk: Improper query construction can produce incorrect requests or expose unsafe shell input. <br>
Mitigation: Validate required parameters against the OpenAPI definitions and safely quote or URL-encode query parameters before execution. <br>


## Reference(s): <br>
- [CoinAnk](https://coinank.com) <br>
- [CoinAnk OpenAPI Base URL](https://open-api.coinank.com) <br>
- [ClawHub skill page](https://clawhub.ai/a4205586/coinank-openapi-skill) <br>
- [ETF OpenAPI reference](references/ETF.openapi.json) <br>
- [K-line OpenAPI reference](references/K线.openapi.json) <br>
- [RSI screener OpenAPI reference](references/RSI选币器.openapi.json) <br>
- [HyperLiquid whale OpenAPI reference](references/hyperLiquid鲸鱼.openapi.json) <br>
- [Net long and short OpenAPI reference](references/净多头和净空头.openapi.json) <br>
- [Long-short ratio OpenAPI reference](references/多空比.openapi.json) <br>
- [Large order OpenAPI reference](references/大额订单.openapi.json) <br>
- [Coins and trading pairs OpenAPI reference](references/币种和交易对.openapi.json) <br>
- [Market order statistics OpenAPI reference](references/市价单统计指标.openapi.json) <br>
- [Indicator data OpenAPI reference](references/指标数据.openapi.json) <br>
- [News flash OpenAPI reference](references/新闻快讯.openapi.json) <br>
- [Open interest OpenAPI reference](references/未平仓合约.openapi.json) <br>
- [Trending ranking OpenAPI reference](references/热门排行.openapi.json) <br>
- [Liquidation data OpenAPI reference](references/爆仓数据.openapi.json) <br>
- [Order book OpenAPI reference](references/订单本.openapi.json) <br>
- [Order flow OpenAPI reference](references/订单流.openapi.json) <br>
- [Fund flow OpenAPI reference](references/资金流.openapi.json) <br>
- [Funding rate OpenAPI reference](references/资金费率.openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands and JSON response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses COINANK_API_KEY for authenticated CoinAnk API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
