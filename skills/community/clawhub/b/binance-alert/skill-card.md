## Description: <br>
BinanceAlert monitors Binance price changes, new listings, Alpha airdrop opportunities, and HODLer announcements, then sends Telegram alerts without requiring a Binance API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnwpdb](https://clawhub.ai/user/cnwpdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, automation operators, and developers use this skill to configure Telegram alerts for public Binance market events and recurring checks. It supports one-off price/change alerts plus scheduled monitoring for listings, Alpha opportunities, and announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically reads Telegram credentials from a shared Freqtrade secrets file when present. <br>
Mitigation: Provide TG_BOT_TOKEN and TG_CHAT_ID through a dedicated skill-specific environment and use a dedicated Telegram bot/chat. <br>
Risk: Cron or systemd scheduling can create ongoing Telegram alerts and repeated external requests. <br>
Mitigation: Only configure recurring scheduling when continuous monitoring is intended, and review alert frequency and state-file permissions before deployment. <br>
Risk: Market, listing, and airdrop alerts may be mistaken for financial advice. <br>
Mitigation: Treat alerts as informational signals only and review Binance data directly before acting on them. <br>


## Reference(s): <br>
- [BinanceAlert on ClawHub](https://clawhub.ai/cnwpdb/binance-alert) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>
- [BinanceAlert script](artifact/scripts/binance_alert.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; script commands emit JSON status or Telegram alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus TG_BOT_TOKEN and TG_CHAT_ID; can send Telegram messages and persist local alert state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
