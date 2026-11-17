## Description:

Crypto Scope helps agents query cryptocurrency prices, calculate technical indicators, and generate BUY, SELL, or HOLD trading signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imgolye](https://clawhub.ai/user/imgolye)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve cryptocurrency market data, inspect common indicators such as MA, RSI, MACD, and Bollinger Bands, and receive automated trading signal guidance. It is intended as analysis support only and not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The main documented workflow is inconsistent with the code and can perform automatic SkillPay billing using an embedded credential.

Mitigation: Review before installing; do not run the paid analyzer or setup scripts unless paid SkillPay billing is intended and trusted. The publisher should rotate the embedded key, remove hard-coded credentials, and add explicit per-charge confirmation.

Risk: Generated trading signals can be misleading if treated as financial advice.

Mitigation: Treat outputs as analysis support only, verify market data independently, and make trading decisions outside the skill.

## Reference(s):

- [Crypto Scope ClawHub page](https://clawhub.ai/imgolye/skills/crypto-scope)
- [Publisher profile](https://clawhub.ai/user/imgolye)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [CoinGecko coins list](https://coingecko.com/coins)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or plain text from CLI commands; documentation includes Markdown examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include live market data, calculated indicators, trading signals, confidence, risk level, billing status, and recharge links when SkillPay balance is insufficient.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
