## Description:

Cross Funding Arb helps an agent operate a Hyperliquid and Binance perpetual-futures funding-rate arbitrage workflow with opportunity scanning, stability checks, order execution, health monitoring, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synththoughts](https://clawhub.ai/user/synththoughts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and operate a delta-neutral funding-rate arbitrage workflow across Hyperliquid and Binance Futures, including periodic ticks, status checks, and daily reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated live futures trading can place real orders using high-impact exchange credentials.

Mitigation: Use least-privilege exchange credentials with withdrawals disabled, prefer testnet or small explicit budgets first, and monitor initial runs closely.

Risk: Scheduled execution can repeatedly act on market signals and amplify configuration or runtime mistakes.

Mitigation: Review configuration before enabling cron, keep alerting enabled, and use status and report commands to confirm behavior after deployment.

Risk: Security guidance warns not to rely on the documented 50% budget limit until the implementation is fixed.

Mitigation: Set small explicit budgets and verify actual order sizing on testnet before using mainnet credentials.

Risk: Sourcing .env files in shell or cron can broaden credential exposure.

Mitigation: Use dedicated credential injection for exchange keys and notification tokens, and avoid reusing daemon credentials for notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/synththoughts/skills/cross-funding-arb)
- [README](README.md)
- [Funding arbitrage algorithm](references/funding-arb-algorithm.md)
- [Configuration defaults](references/config.json)
- [Entrypoint source](references/cross_funding.py)
- [Python requirements](references/requirements.txt)
- [VarFunding funding API](https://varfunding.xyz/api/funding?exchanges=hyperliquid,binance)
- [Binance signed endpoint security](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/public-api-definitions#signed-trade-and-user_data-endpoint-security)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/Python reference files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, exchange credentials, and optional notification credentials; ClawHub metadata lists darwin and linux support.]

## Skill Version(s):

2.8.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
