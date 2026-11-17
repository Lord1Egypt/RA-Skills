## Description:

Crypto Arbitrage Monitor helps monitor BTC, ETH, SOL, XRP, and DOGE price spreads across major exchanges and send Feishu or Telegram alerts for potential arbitrage opportunities after estimated fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceanking57](https://clawhub.ai/user/oceanking57)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and trading operations teams can use this skill to configure and run a crypto price-spread monitor across Binance, OKX, Bybit, and related exchanges. It is intended for market monitoring and alerting, not as investment advice or an automated trading guarantee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messaging secrets may be placed directly in source code and could be exposed through committed files or persistent logs.

Mitigation: Configure Feishu and Telegram credentials through environment variables or a secret manager, keep arb_monitor.log out of version control, and rotate any token that may have been shared.

Risk: Dependencies are version-ranged rather than pinned, which can change runtime behavior over time.

Mitigation: Install in an isolated virtual environment and pin reviewed dependency versions before production use.

Risk: Crypto spread alerts can become stale quickly and do not account for all trading, withdrawal, liquidity, or execution constraints.

Mitigation: Use alerts as monitoring input only, validate liquidity and fees independently, and avoid treating the tool as investment advice or automated execution approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oceanking57/skills/crypto-arb-monitor)
- [Publisher profile](https://clawhub.ai/user/oceanking57)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring setup guidance and alert configuration details; runtime script output includes console/file logs and Feishu or Telegram alert messages.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
