## Description:

Fetches the current Bitcoin price from CoinGecko and sends Telegram notifications, with optional alerts when the price falls below a configured threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesusreb](https://clawhub.ai/user/jesusreb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check Bitcoin pricing and send price updates or threshold alerts to a Telegram chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Telegram bot token and chat ID, and sends BTC price messages through Telegram.

Mitigation: Install only when this credential use and Telegram delivery are acceptable; keep tokens in environment variables and rotate them if exposed.

Risk: The release evidence recommends updating the requests dependency before use.

Mitigation: Review and update the pinned requests dependency during deployment maintenance.

Risk: The README says no API keys are needed, while Telegram integration still requires Telegram credentials.

Mitigation: Treat that claim as applying to CoinGecko only and configure Telegram credentials explicitly before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesusreb/skills/btc-price-monitor)
- [Publisher profile](https://clawhub.ai/user/jesusreb)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Telegram message text and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Telegram bot token and chat ID environment variables; optional USD price threshold controls alert behavior.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
