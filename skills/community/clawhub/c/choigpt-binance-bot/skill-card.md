## Description:

Automates Binance futures trading with the Sweepzone V1 strategy, real-time market scanning, risk management, and Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexchoi21](https://clawhub.ai/user/alexchoi21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to configure, run, and monitor a Binance Futures trading bot for live trading, backtesting, market scanning, dashboard monitoring, and Telegram-based status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate as a real Binance Futures auto-trading bot.

Mitigation: Use restricted, IP-limited Binance API keys without withdrawal permission and verify testnet or dry-run behavior before any live run.

Risk: Telegram access control may expose trading controls or account information.

Mitigation: Require an explicit Telegram chat allowlist before enabling Telegram commands or notifications.

Risk: Account balances, positions, chat history, and trade performance may be sent to Google Gemini.

Mitigation: Rotate or remove the embedded Gemini key and disable or review AI context sharing before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexchoi21/skills/choigpt-binance-bot)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands with textual trading status, signals, reports, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate live trading, backtesting, market scanning, dashboard monitoring, and Telegram notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
