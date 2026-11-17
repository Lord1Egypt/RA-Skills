## Description:

Provides a crypto automated trading strategy package for OKX, Binance, Bybit, and Bitget, including five strategy implementations, risk-control guidance, Telegram alerts, and deployment instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-system operators use this skill as guidance for building or deploying automated crypto trading strategies with exchange integrations, risk controls, alerts, and process supervision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves automated crypto trading and may lead users to run a persistent bot with real exchange API keys.

Mitigation: Confirm paper-trading or testnet support before use, disable withdrawals, restrict API permissions, enable IP allowlisting where available, and avoid storing production secrets in repository configuration files.

Risk: Dependency and runtime setup may affect funds or account access if used without review.

Mitigation: Review and pin dependencies before deployment, inspect configuration values, and test behavior with non-production funds before any live trading.

Risk: Trading strategy material can be mistaken for investment advice.

Mitigation: Treat the output as educational and implementation guidance only; users should make independent trading and risk-management decisions.

## Reference(s):

- [Crypto Auto Trader Strategy on ClawHub](https://clawhub.ai/sg345662365-oss/skills/crypto-auto-trader-strategy)
- [Publisher profile: sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading-strategy and deployment guidance; users must supply and protect their own exchange credentials.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
