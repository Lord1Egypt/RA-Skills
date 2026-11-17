## Description:

Crypto Fear & Greed Index reporter that fetches the current market sentiment index, combines it with BTC price movement, and provides simple analysis for market sentiment checks and daily updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyiyuleyuli-cloud](https://clawhub.ai/user/yuyiyuleyuli-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-focused agents use this skill to fetch current or 30-day crypto Fear & Greed Index data, combine it with BTC price movement, and produce a brief market sentiment report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the skill suspicious because each invocation creates a 0.001 USDT SkillPay billing request and uses a payment API key.

Mitigation: Install only when the paid billing behavior is acceptable, keep SKILLPAY_API_KEY in a protected environment variable, and require explicit approval before an agent runs either script.

Risk: Market sentiment and BTC price reports can be mistaken for investment advice.

Mitigation: Present outputs as informational market sentiment summaries and have users review current market data before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyiyuleyuli-cloud/skills/fear-greed-index)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yuyiyuleyuli-cloud)
- [Alternative.me Crypto Fear & Greed Index API](https://alternative.me/crypto/fear-and-greed-index/)
- [Alternative.me Fear & Greed API Endpoint](https://api.alternative.me/fng/?limit=2)
- [Alternative.me Bitcoin Ticker API Endpoint](https://api.alternative.me/v2/ticker/bitcoin/?convert=USD)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include sentiment score, classification, recent trend, BTC price movement, and simple market commentary.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
