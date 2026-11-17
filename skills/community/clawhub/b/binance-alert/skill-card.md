## Description:

BinanceAlert monitors Binance price changes, new listings, Alpha airdrop opportunities, and HODLer announcements, then sends alerts through Telegram without requiring a Binance API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnwpdb](https://clawhub.ai/user/cnwpdb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to configure Binance market and announcement checks and receive Telegram notifications for target symbols, listings, Alpha opportunities, and HODLer announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram credentials and chat routing control where market alerts are sent.

Mitigation: Use a dedicated Telegram bot token and chat ID for this skill, verify the target chat before scheduled use, and avoid sharing unrelated secrets in the same environment file.

Risk: Alert symbols, thresholds, notes, and timestamps may be sent to Telegram.

Mitigation: Avoid placing sensitive notes in alert configuration and review Telegram retention and access controls for the configured chat.

Risk: Market and airdrop alerts can be mistaken for trading or investment advice.

Mitigation: Treat alerts as informational signals and review market conditions independently before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cnwpdb/skills/binance-alert)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus TG_BOT_TOKEN and TG_CHAT_ID; alerts may be delivered to the configured Telegram chat.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
