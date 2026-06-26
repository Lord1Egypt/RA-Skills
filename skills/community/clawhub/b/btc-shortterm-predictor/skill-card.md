## Description: <br>
BTC 15分钟短线预测 - 技术指标分析，预测涨跌方向。每次调用0.005 USDT。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ffffff9331](https://clawhub.ai/user/ffffff9331) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users run this Node.js skill to retrieve a paid BTC/USDT 15-minute directional prediction based on Binance market data and technical indicators. The output is intended as informational trading analysis and includes a warning that it is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review describes the paid billing flow as under-scoped and unable to preserve a user's paid balance across runs. <br>
Mitigation: Review the SkillPay flow before use and require the publisher to document how balances are tied to a stable user identity. <br>
Risk: The security review reports an embedded billing key. <br>
Mitigation: Require the publisher to remove or rotate the embedded key and rely on a user-provided SKILLPAY_API_KEY. <br>
Risk: The security review warns that trading-performance claims need substantiation or a reduced claim. <br>
Mitigation: Treat predictions as informational only and require documented evaluation evidence before relying on claimed win rates or profitability. <br>
Risk: The security review calls for clearer SkillPay data-sharing documentation. <br>
Mitigation: Do not deposit funds until the publisher explains what payment and user data is shared with SkillPay. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ffffff9331/btc-shortterm-predictor) <br>
- [Publisher profile](https://clawhub.ai/user/ffffff9331) <br>
- [Binance API endpoint](https://api.binance.com) <br>
- [SkillPay service](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Console text with trading direction, confidence, indicator signals, stop loss, take profit, and market summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY for billing and network access to Binance and SkillPay services.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
