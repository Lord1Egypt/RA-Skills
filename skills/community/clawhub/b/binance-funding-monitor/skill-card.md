## Description: <br>
币安资金费率监控是一个按次付费的 MCP skill，用于查询 Binance 合约账户总览、当前持仓、近 7 天资金费收入和完整监控报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyu812707-wq](https://clawhub.ai/user/yyu812707-wq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and crypto operations agents use this skill to monitor a Binance futures account, review positions, and summarize funding-fee income. It requires user-provided Binance API credentials and should be used for monitoring only unless the trading behavior is explicitly reviewed and accepted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says this monitoring skill includes undisclosed leveraged trading code. <br>
Mitigation: Review the artifact before installation and do not deploy it as monitoring-only unless the trading and rebalance code is removed or the publisher clearly reclassifies it as automated futures trading with explicit consent and risk controls. <br>
Risk: The skill asks for sensitive Binance exchange credentials. <br>
Mitigation: Use a dedicated Binance API key restricted to read-only or account-query access, keep trading and withdrawals disabled, and enable IP restrictions where possible. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Require manual security review before installation and ensure users understand the credential and futures-trading exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yyu812707-wq/binance-funding-monitor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yyu812707-wq) <br>
- [Binance Futures API endpoint](https://fapi.binance.com) <br>
- [SkillPay API endpoint](https://api.skillpay.me/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text MCP responses with account, position, funding income, and full-report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Binance API credentials and may require a SkillPay session identifier for paid calls.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
