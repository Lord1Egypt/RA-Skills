## Description:

Provides BTC/ETH trading analysis, technical indicators, opening suggestions, and multi-platform alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thanatosmoe](https://clawhub.ai/user/thanatosmoe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate BTC/ETH technical-analysis reports with entry, target, stop-loss, and risk-reward suggestions. They can also push those reports to configured chat destinations for recurring market monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messaging credentials may be stored in a local configuration file.

Mitigation: Move real tokens and webhooks out of config.json where possible, restrict bot and webhook permissions, and rotate credentials if they are exposed.

Risk: Trading reports are sent to third-party chat services.

Mitigation: Verify every configured chat destination and install only when outbound network access to those services is acceptable.

Risk: Generated trading calls may be incorrect or misleading.

Mitigation: Treat outputs as analysis only, not investment advice, and review recommendations before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thanatosmoe/skills/btc-eth-ai-signal)
- [Publisher Profile](https://clawhub.ai/user/thanatosmoe)
- [CoinEx API](https://api.coinex.com/v1)
- [Gate.io Futures Ticker API](https://api.gateio.ws/api/v4/futures/usdt/tickers?contract=BTC_USDT)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown report with optional chat-message delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes BTC and ETH market summaries, indicator readings, trade direction suggestions, entry ranges, targets, stop-loss levels, and risk-reward notes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
