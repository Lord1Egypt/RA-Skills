## Description:

Enables agents to query CoinAnk OpenAPI cryptocurrency market-data endpoints using a user-supplied API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a4205586](https://clawhub.ai/user/a4205586)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent retrieve CoinAnk cryptocurrency market data, including K-line data, ETF flows, open interest, long-short ratios, funding rates, liquidations, order books, order flow, news, and related indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a CoinAnk API key and injects it into API request headers.

Mitigation: Store the key only in COINANK_API_KEY, treat it as sensitive, and avoid pasting it into prompts, logs, or generated examples.

Risk: The skill sends outbound requests to CoinAnk's OpenAPI service.

Mitigation: Install it only when external CoinAnk market-data queries are intended and network access to open-api.coinank.com is acceptable.

Risk: CoinAnk endpoints may require specific VIP access levels and current millisecond timestamps.

Mitigation: Validate required parameters against the selected OpenAPI definition and generate fresh millisecond timestamps for time-bound requests.

Risk: Most source documentation is Chinese, which can make endpoint behavior harder to review for some users.

Mitigation: Review the relevant README section and selected OpenAPI file before enabling requests for unfamiliar endpoint categories.

## Reference(s):

- [CoinAnk homepage](https://coinank.com)
- [CoinAnk OpenAPI endpoint](https://open-api.coinank.com)
- [ClawHub skill page](https://clawhub.ai/a4205586/skills/coinank-openapi-skill)
- [CoinAnk ETF OpenAPI definition](artifact/references/ETF.openapi.json)
- [CoinAnk K-line OpenAPI definition](artifact/references/K线.openapi.json)
- [CoinAnk RSI selector OpenAPI definition](artifact/references/RSI选币器.openapi.json)
- [CoinAnk HyperLiquid whale OpenAPI definition](artifact/references/hyperLiquid鲸鱼.openapi.json)
- [CoinAnk net long and net short OpenAPI definition](artifact/references/净多头和净空头.openapi.json)
- [CoinAnk long-short ratio OpenAPI definition](artifact/references/多空比.openapi.json)
- [CoinAnk large orders OpenAPI definition](artifact/references/大额订单.openapi.json)
- [CoinAnk coins and trading pairs OpenAPI definition](artifact/references/币种和交易对.openapi.json)
- [CoinAnk market-order statistics OpenAPI definition](artifact/references/市价单统计指标.openapi.json)
- [CoinAnk indicator data OpenAPI definition](artifact/references/指标数据.openapi.json)
- [CoinAnk news OpenAPI definition](artifact/references/新闻快讯.openapi.json)
- [CoinAnk open interest OpenAPI definition](artifact/references/未平仓合约.openapi.json)
- [CoinAnk popular rankings OpenAPI definition](artifact/references/热门排行.openapi.json)
- [CoinAnk liquidation data OpenAPI definition](artifact/references/爆仓数据.openapi.json)
- [CoinAnk order book OpenAPI definition](artifact/references/订单本.openapi.json)
- [CoinAnk order flow OpenAPI definition](artifact/references/订单流.openapi.json)
- [CoinAnk capital flow OpenAPI definition](artifact/references/资金流.openapi.json)
- [CoinAnk funding rate OpenAPI definition](artifact/references/资金费率.openapi.json)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COINANK_API_KEY and sends GET requests to https://open-api.coinank.com.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
