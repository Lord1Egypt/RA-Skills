## Description:

1m-trade is an on-chain operations hub for BlockBeats market intelligence, Hyperliquid DEX trading through hl1m, wallet setup, and optional autonomous trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eycuit](https://clawhub.ai/user/eycuit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect crypto market/news signals, configure a Hyperliquid trading wallet, run hl1m market and order commands, and optionally schedule autonomous trading reports and actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable persistent unattended real-money crypto trading authority.

Mitigation: Use testnet first and do not enable autonomous cron trading until independent max notional, leverage, daily loss, allowed asset, expiration, and removal controls are in place.

Risk: Wallet signing credentials are required for trading workflows.

Mitigation: Avoid pasting private keys into chat, never use a master wallet key, use only delegated or proxy keys, and keep encrypted key fields in local state.

Risk: The release was flagged suspicious by the authoritative security evidence.

Mitigation: Install only when agent-controlled crypto trading is intentional, pin and verify the 1m-trade CLI, and review the trading setup before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eycuit/skills/1m-trade)
- [Publisher profile](https://clawhub.ai/user/eycuit)
- [1M-Trade wallet and account site](https://www.1m-trade.com)
- [BlockBeats Pro API](https://api-pro.theblockbeats.info)
- [1m-trade DEX reference](artifact/skills/1m-trade-dex/reference.md)
- [1m-trade news skill](artifact/skills/1m-trade-news/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands, configuration guidance, and JSON or human-readable CLI results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call BlockBeats APIs and hl1m commands; trading workflows require local credentials and should not print secrets.]

## Skill Version(s):

1.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
