## Description:

Paid professional price monitor for comparing Taobao, Pinduoduo, JD.com, and Amazon prices with scheduled monitoring, price-difference alerts, notifications, and price-history tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[since198905](https://clawhub.ai/user/since198905)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping automation agents use this skill to compare product prices across supported e-commerce platforms, monitor configured items hourly, review local price history, and receive optional Feishu or Telegram alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hourly monitoring can repeatedly query marketplace pages for every configured item.

Mitigation: Review references/config.yaml before use, remove sample products, and enable recurring scans only for products the user intends to monitor.

Risk: Notification settings may include Feishu webhooks or Telegram bot credentials.

Mitigation: Leave notification fields blank unless delivery is intended and treat configured webhook URLs, bot tokens, and chat identifiers as sensitive secrets.

Risk: Live marketplace price extraction may fail or produce incomplete results when pages change or block automated access.

Mitigation: Review generated price reports before acting on them and verify important purchases against the marketplace directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/since198905/skills/ec-price-monitor-pro-plus)
- [Configuration reference](artifact/references/config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-style text reports with price comparisons, alerts, and history summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local SQLite price history and send optional Feishu or Telegram notifications when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
