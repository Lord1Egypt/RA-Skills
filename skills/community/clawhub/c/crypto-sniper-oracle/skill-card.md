## Description:

Institutional-grade quantitative market oracle with Order Book Imbalance (OBI), VWAP analysis, automated reports, and Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to fetch public cryptocurrency market data, calculate order book and VWAP signals, and generate manual or scheduled market reports. Optional Telegram delivery can send generated summaries and anomaly alerts to a configured chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot credentials may be exposed if stored in shell profile files, browser URLs, shared terminals, or logs.

Mitigation: Provide credentials only through a secure runtime secret mechanism, rotate any exposed bot token, and avoid persisting real tokens in ~/.bashrc or ~/.profile.

Risk: Automated reports and alerts can present trading-style recommendations that may be mistaken for verified financial advice.

Mitigation: Treat all generated signals as informational only and require independent review before making trading or investment decisions.

Risk: Scheduled cron runs can repeatedly write reports and logs under /workspace and optionally send them to Telegram.

Mitigation: Enable cron and Telegram delivery only after reviewing destination, retention, and workspace storage expectations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georges91560/skills/crypto-sniper-oracle)
- [Publisher Profile](https://clawhub.ai/user/georges91560)
- [Homepage](https://github.com/georges91560/crypto-sniper-oracle)
- [Repository](https://github.com/georges91560/crypto-sniper-oracle)
- [Binance Public Market Data API](https://api.binance.com/api/v3/*)
- [Telegram Bot API](https://api.telegram.org/bot*)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON market data, Markdown reports, and concise command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes cache, report, and log files under /workspace; optional Telegram delivery requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.]

## Skill Version(s):

3.3.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
