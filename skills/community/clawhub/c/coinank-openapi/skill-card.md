## Description: <br>
Helps an agent query CoinAnk OpenAPI market-data endpoints using the relevant OpenAPI reference files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[annata](https://clawhub.ai/user/annata) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to help an agent construct authenticated read-only CoinAnk market-data requests for cryptocurrency analytics, including K-line data, ETF data, open interest, long/short ratios, funding rates, liquidations, order flow, and related indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CoinAnk API key could be exposed in chat, generated curl commands, or logs. <br>
Mitigation: Use a dedicated COINANK_API_KEY, keep it in the environment rather than chat, and redact the key from commands and logs. <br>
Risk: User-supplied query parameters could produce malformed or unsafe shell commands. <br>
Mitigation: Validate required parameters against the selected OpenAPI reference and safely encode query values before constructing curl requests. <br>
Risk: Requests using stale example timestamps may fail or return misleading results. <br>
Mitigation: Generate current millisecond timestamps for time-sensitive endTime parameters unless the user explicitly supplies a valid timestamp. <br>


## Reference(s): <br>
- [CoinAnk homepage](https://coinank.com) <br>
- [CoinAnk OpenAPI base URL](https://open-api.coinank.com) <br>
- [ClawHub skill page](https://clawhub.ai/annata/coinank-openapi) <br>
- [ETF OpenAPI reference](references/ETF.openapi.json) <br>
- [K-line OpenAPI reference](references/K线.openapi.json) <br>
- [RSI screener OpenAPI reference](references/RSI选币器.openapi.json) <br>
- [HyperLiquid whale OpenAPI reference](references/hyperLiquid鲸鱼.openapi.json) <br>
- [Net long and net short OpenAPI reference](references/净多头和净空头.openapi.json) <br>
- [Long/short ratio OpenAPI reference](references/多空比.openapi.json) <br>
- [Large orders OpenAPI reference](references/大额订单.openapi.json) <br>
- [Coins and trading pairs OpenAPI reference](references/币种和交易对.openapi.json) <br>
- [Market-order statistics OpenAPI reference](references/市价单统计指标.openapi.json) <br>
- [Indicator data OpenAPI reference](references/指标数据.openapi.json) <br>
- [News flash OpenAPI reference](references/新闻快讯.openapi.json) <br>
- [Open interest OpenAPI reference](references/未平仓合约.openapi.json) <br>
- [Trending rankings OpenAPI reference](references/热门排行.openapi.json) <br>
- [Liquidation data OpenAPI reference](references/爆仓数据.openapi.json) <br>
- [Order book OpenAPI reference](references/订单本.openapi.json) <br>
- [Order flow OpenAPI reference](references/订单流.openapi.json) <br>
- [Capital flow OpenAPI reference](references/资金流.openapi.json) <br>
- [Funding rate OpenAPI reference](references/资金费率.openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline curl commands and JSON-oriented API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COINANK_API_KEY for authenticated read-only CoinAnk requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
