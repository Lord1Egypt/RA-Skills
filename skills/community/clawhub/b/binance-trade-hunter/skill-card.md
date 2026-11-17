## Description:

Binance Trade Hunter helps agents analyze Binance spot markets, monitor price pumps, check balances and positions, and execute user-confirmed buy or sell actions through Telegram-facing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[june-kris](https://clawhub.ai/user/june-kris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Binance spot-market opportunities, receive pump alerts, inspect account balances and positions, and execute user-confirmed market buy or sell orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Binance spot trades when supplied with trading credentials.

Mitigation: Require explicit user confirmation for every trade, use a restricted Binance sub-account, and keep trade limits small.

Risk: The skill can reuse local Telegram credentials or discover chat details for notifications.

Mitigation: Prefer explicitly configured Telegram credentials and avoid automatic credential discovery unless the user accepts that access.

Risk: Background alert and push services can continue running after startup.

Mitigation: Start background services only on explicit request and use the service status and stop commands to monitor and terminate them.

Risk: Runtime dependencies and live market APIs affect behavior and availability.

Mitigation: Review and lock dependencies before deployment, and treat market analysis as decision support rather than financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/june-kris/skills/binance-trade-hunter)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Formatted text and Markdown-style command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live trading results, market analysis summaries, Telegram notification guidance, and background service status text.]

## Skill Version(s):

1.4.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
