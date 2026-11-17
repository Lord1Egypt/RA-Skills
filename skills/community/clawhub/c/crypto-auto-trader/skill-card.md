## Description:

Provides an agent-facing crypto auto-trading strategy bundle with five trading strategies, deployment guidance, configurable risk controls, and Telegram alerting for exchanges such as OKX, Binance, Bybit, and Bitget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation users use this skill to have an agent explain, configure, and run crypto trading strategy code, exchange setup steps, risk controls, and alerting guidance. It is relevant for users evaluating automated strategies across supported crypto exchanges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves configuring exchange API keys for an automated trading bot.

Mitigation: Use exchange API keys with withdrawals disabled, minimal trading permissions, IP allowlisting where supported, and subaccounts isolated from primary funds.

Risk: The skill can support long-running automated trading against live crypto markets.

Mitigation: Test with paper trading or small capped balances first, define clear start and stop controls, and avoid running it on funds the user cannot afford to lose.

Risk: Dependency and runtime setup guidance is not enough on its own for live deployment.

Mitigation: Review dependency versions and lockfiles before execution, keep secrets out of tracked configuration files, and perform a manual security review before using real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/skills/crypto-auto-trader)
- [ClawHub publisher profile](https://clawhub.ai/user/sg345662365-oss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading bot configuration steps, exchange API key handling guidance, dependency installation commands, PM2 process commands, and risk-control recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
