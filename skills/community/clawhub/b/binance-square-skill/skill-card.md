## Description:

Binance Square signal agent that scrapes Binance Square posts, detects bot-pushed narratives, optionally checks Coinglass on-chain signals, and produces directional LONG, SHORT, AVOID, or WATCH trading signal reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ru7superbeauty](https://clawhub.ai/user/ru7superbeauty)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Binance Square narratives, compare them with optional on-chain market signals, and generate concise crypto trading signal reports. It is a pattern-finding aid and does not provide financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Chromium with sandbox protections disabled.

Mitigation: Run the skill in a restricted account or container before trusting it on a primary workstation.

Risk: Telegram delivery can expose generated report contents to a configured chat.

Mitigation: Use scan:tg only with a trusted bot token and chat ID, and review report contents before sending.

Risk: The Telegram workflow uses a fixed /tmp report path in the skill instructions.

Mitigation: Prefer stdin or a secure mktemp-style file path for Telegram message handoff.

Risk: The release has no lockfile for the Puppeteer dependency.

Mitigation: Pin and review installed dependencies before use.

Risk: The security verdict is suspicious and requires review before installation.

Mitigation: Review the skill source and scanner summary before deploying it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ru7superbeauty/skills/binance-square-skill)
- [Binance markets coinInfo](https://www.binance.com/zh-CN/markets/coinInfo)
- [Telegram BotFather](https://t.me/BotFather)
- [Telegram userinfobot](https://t.me/userinfobot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands, saved Markdown reports, optional JSON scrape data, and optional Telegram message JSON confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telegram summaries are kept under 4000 characters; full reports are saved separately when the scan workflow runs.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
