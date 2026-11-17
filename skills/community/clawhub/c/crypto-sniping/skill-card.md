## Description:

Automated Binance trading bot that scans BTC, ETH, and SOL markets with technical indicators and whale tracking to generate signals, place trades, and report status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorjenorbulim](https://clawhub.ai/user/dorjenorbulim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and crypto operators use this skill to configure and run a Binance-focused trading assistant that scans market data, surfaces signals, tracks large-market activity, and can execute automated trades when enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Binance trades automatically.

Mitigation: Start without live trading and use a dedicated restricted Binance API key with no withdrawal permission.

Risk: Advertised stop-loss and take-profit behavior may not provide reliable live exit protection.

Mitigation: Do not rely on those controls until live exit-order behavior and paper-mode credential handling are reviewed and fixed.

Risk: Telegram alerts may reveal trading activity.

Mitigation: Use Telegram notifications only with a trusted bot token and chat, and treat alert content as sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dorjenorbulim/skills/crypto-sniping)
- [Publisher Profile](https://clawhub.ai/user/dorjenorbulim)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, YAML configuration, and text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place Binance orders and send Telegram alerts when configured for live operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
