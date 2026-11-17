## Description:

Set and manage cryptocurrency price alerts and receive notifications when targets are reached.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto users and trading-focused agents use this skill to add, list, remove, and check local price alerts for cryptocurrency pairs. It helps monitor target prices without requiring the user to watch charts continuously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local alert records may reveal the user's cryptocurrency interests and target prices.

Mitigation: Review access to the local OpenClaw workspace data path before use, and avoid sharing the stored alert file.

Risk: Price checks contact Binance, which can disclose requested market pairs to an external service.

Mitigation: Use the skill only when contacting Binance for ticker data is acceptable for the user and deployment environment.

Risk: Telegram and Discord notification behavior is under-documented in the release evidence.

Mitigation: Confirm what notification data is sent and how accounts are linked before enabling external notifications.

## Reference(s):

- [Crypto Price Alerts on ClawHub](https://clawhub.ai/dagangtj/skills/crypto-price-alerts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts are stored locally, and price checks contact Binance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
