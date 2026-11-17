## Description:

BTC 15分钟短线预测 - 技术指标分析，预测涨跌方向。每次调用0.005 USDT。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ffffff9331](https://clawhub.ai/user/ffffff9331)

### License/Terms of Use:

MIT

## Use Case:

External users run this agent skill to fetch BTC market data, calculate short-term technical indicators, and receive a 15-minute direction forecast with confidence, stop-loss, and take-profit guidance. The skill charges 0.005 USDT per invocation through SkillPay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a paid remote billing service during invocation.

Mitigation: Install only after confirming that SkillPay billing, user consent, and expected per-call charges are acceptable.

Risk: A bundled SkillPay key should be treated as exposed.

Mitigation: Use a reviewer-controlled SKILLPAY_API_KEY and rotate any exposed billing credentials before deployment.

Risk: The advertised win-rate and automated-trading claims may mislead users.

Mitigation: Treat predictions as informational analysis only and validate performance independently before relying on the output.

Risk: History and auto commands may run before the billing behavior is fully validated.

Mitigation: Avoid history or auto modes until charging behavior has been reviewed and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ffffff9331/skills/btc-shortterm-predictor)
- [Binance API endpoint](https://api.binance.com)
- [SkillPay billing endpoint](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Console text with BTC price, prediction direction, confidence, technical indicators, trading guidance, and 24-hour market summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY for billing; help output documents history and auto commands as development-stage modes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
