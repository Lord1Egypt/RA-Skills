## Description:

Fetches current forex buy and sell rates from supported major Chinese banks by bank name and currency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhmcn](https://clawhub.ai/user/lhmcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve public forex rates from supported Chinese banks for selected currencies and return normalized JSON for comparison or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to public Chinese bank sites, so results can be unavailable, delayed, stale, or affected by upstream page and API changes.

Mitigation: Treat returned rates as informational and confirm against the relevant bank source before using them for high-value financial decisions.

Risk: The code enables a legacy TLS compatibility option for bank fetches.

Mitigation: Install and run the skill only in environments where that TLS behavior is acceptable, and review outbound network destinations before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lhmcn/skills/chinese-bank-forex-rates)
- [Agricultural Bank of China exchange-rate source](https://ewealth.abchina.com/app/data/api/DataService/ExchangeRateV2)
- [Bank of Communications exchange-rate source](https://www.bankcomm.com/SITE/queryExchangeResult.do)
- [Bank of China exchange-rate source](https://www.boc.cn/sourcedb/whpj/)
- [China Construction Bank exchange-rate source](https://www1.ccb.com/cn/home/news/jshckpj_new2.xml)
- [China Merchants Bank exchange-rate source](https://fx.cmbchina.com/api/v1/fx/rate)
- [Industrial and Commercial Bank of China exchange-rate source](https://papi.icbc.com.cn/exchanges/ns/getLatest)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object with bankName, updateTime, and rates entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rates include currencyName, buyPrice, and sellPrice; numeric prices are standardized to CNY per 100 units of foreign currency and rounded to two decimal places.]

## Skill Version(s):

0.1.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
